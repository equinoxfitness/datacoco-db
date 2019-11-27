
import unittest
import tempfile

from codb.mssql_tools import MSSQLInteraction
from codb.helper.config import config


class TestMSSQLInteraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mssql_conf = config(conf_path='db.test.cfg')['mssql']
        cls.testClass = MSSQLInteraction(host=mssql_conf['server'], dbname=mssql_conf['db_name'],
                                          user=mssql_conf['user'], password=mssql_conf['password'])

    def test_database(self):
        print('--------------test_database')
        self.testClass.conn()

        self.testClass.batch_open()

        self.testClass.exec_sql(
            """
                IF OBJECT_ID('#TEST', 'U') IS NOT NULL
                DROP TABLE #TEST;
            """
        )

        self.testClass.exec_sql("""
                       CREATE TABLE #TEST (
                        [name] varchar(256)
                        ,[age] int )

                        INSERT INTO #TEST
                        values ('Mike', 12)
                        ,('someone else', 904)
                    """)

        result = self.testClass.fetch_sql_all('select * from #TEST')
        self.assertEqual(True, len(result) > 0)

        result = self.testClass.fetch_sql_all('select count(*) from dbo.cdc_activity')
        print(result)

        # get table columns
        result = self.testClass.get_table_columns('dbo.cdc_activity')
        self.assertEqual(True, len(result) > 0)

        # export sql to csv
        new_file, filename = tempfile.mkstemp()
        print('filename csv: ' + filename)
        result = self.testClass.export_sql_to_csv('select * from #TEST', filename)
        print(result)

        self.testClass.batch_close()