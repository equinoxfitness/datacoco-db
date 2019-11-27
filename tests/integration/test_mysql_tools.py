import unittest

from codb.mysql_tools import MYSQLInteraction
from codb.helper.config import config

class TestMYSQLInteraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            test_conf = config(conf_path='db.test.cfg')['mysql']
            cls.testClass = MYSQLInteraction(dbname=test_conf['db_name'],
                host=test_conf['host'],
                user=test_conf['user'],
                password=test_conf['password'],
                connection='mysql',
                port=test_conf['port'])
        except Exception as e:
            print(e)

    @unittest.skip("mysql config must be included")
    def test_database(self):
        self.testClass.conn(dict_cursor=True)
        self.testClass.batch_open()
        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_test_sql;
            """
        )
        self.testClass.exec_sql(
            """
                CREATE TABLE temp_test_sql (id INT(11), name VARCHAR(10));
            """
        )
        self.testClass.batch_commit()
        self.testClass.exec_sql(
            """
                INSERT INTO temp_test_sql (id,name) VALUES (1, 'mark');
            """
            )
        self.testClass.exec_sql(
            """
                INSERT INTO temp_test_sql (id,name) VALUES (1, 'kyle')
            """
            )
        self.testClass.batch_commit()
        result1 = self.testClass.fetch_sql(
            """
                SELECT * FROM temp_test_sql ORDER BY id DESC;
            """
            )
        self.assertEqual(result1, {'id': 1, 'name': 'mark'})
        result2 = self.testClass.fetch_sql_all(
            """
                SELECT * FROM temp_test_sql ORDER BY id DESC;
            """
            )
        self.assertEqual(result2, [{'id': 1, 'name': 'mark'}, {'id': 1, 'name': 'kyle'}])
        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_test_sql;
            """
        )
        self.testClass.batch_commit()
        self.testClass.batch_close()
