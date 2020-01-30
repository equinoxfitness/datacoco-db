import unittest

from datacoco_db.mysql_tools import MYSQLInteraction


class TestMYSQLInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.testClass = MYSQLInteraction(  # nosec
                host="host",
                dbname="db_name",
                user="user",
                password="password",
                port=3306,
            )
        except Exception as e:
            print(e)

    @unittest.skip("enable this for integration testing, modify connection")
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
        self.assertEqual(result1, {"id": 1, "name": "mark"})
        result2 = self.testClass.fetch_sql_all(
            """
                SELECT * FROM temp_test_sql ORDER BY id DESC;
            """
        )
        self.assertEqual(
            result2, [{"id": 1, "name": "mark"}, {"id": 1, "name": "kyle"}]
        )
        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_test_sql;
            """
        )
        self.testClass.batch_commit()
        self.testClass.batch_close()


if __name__ == "__main__":
    unittest.main()
