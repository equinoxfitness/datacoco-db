import unittest
import tempfile
import os

from codb.pg_tools import PGInteraction
from codb.helper.config import config


class TestPGInteraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            test_conf = config(conf_path='db.test.cfg')['redshift']
            cls.testClass = PGInteraction(dbname=test_conf['db_name'],
                host=test_conf['host'],
                user=test_conf['user'],
                password=test_conf['password'],
                port=test_conf['port'],
                schema='public')
        except Exception as e:
            print(e)


    @unittest.skip("enable this for integration testing. use tests/test_data/db.test.cfg")
    def test_database(self):
        print('--------------test_database')
        self.testClass.conn()
        self.testClass.batch_open()
        exists = self.testClass.table_exists('edw_landing.cache_trainer_performance')
        print('edw_landing.cache_trainer_performance: ' + str(exists))
        self.assertEqual(True, exists[0])
        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_sql_count;
            """
        )
        self.testClass.exec_sql('commit;')
        self.testClass.exec_sql("""
                CREATE TEMPORARY TABLE temp_sql_count
                AS
                SELECT COUNT(*) as cache_count
                FROM edw_landing.cache_trainer_performance;
            """)
        self.testClass.batch_commit();
        self.testClass.bulk_dictionary_insert('temp_sql_count', {'cache_count': 0})
        results = self.testClass.fetch_sql('select * from temp_sql_count')
        for result in results:
            print(result)

        # export to csv
        new_file, filename = tempfile.mkstemp()
        print('filename csv: ' + filename)
        self.testClass.export_sql_to_csv('select * from temp_sql_count', filename)
        os.close(new_file)

        # export to json
        new_file, filename = tempfile.mkstemp()
        print('filename json: ' + filename)
        self.testClass.export_sql_to_json('select * from temp_sql_count', filename)
        os.close(new_file)

        # export to s3
        aws_conf = config(conf_path='db.test.cfg')['aws']
        general_conf = config(conf_path='db.test.cfg')['general']
        self.testClass.export_sql_to_s3(
            sql='select * from temp_sql_count',
            s3path='s3://' + general_conf["temp_bucket"] + '/datacocodb-test.txt',
            aws_access_key=aws_conf['aws_id'],
            aws_secret_key=aws_conf['aws_key']
        )

        self.testClass.batch_close()
