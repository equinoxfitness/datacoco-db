import unittest

from codb.sqlite_tools import SQLiteInteraction


class TestSQLiteInteraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.testClass = SQLiteInteraction(db_file="test.db")
        except:
            pass

    def test_database(self):
        self.testClass.conn()
        self.testClass.batch_open()
        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_test_sql;
            """
        )

        self.testClass.exec_sql(
            """
                CREATE TABLE temp_test_sql (id INT, name TEXT);
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
                INSERT INTO temp_test_sql (id,name) VALUES (2, 'alex')
            """
            )
        self.testClass.batch_commit()

        result1 = self.testClass.fetch_sql(
            """
                SELECT * FROM temp_test_sql ORDER BY id ASC;
            """,
            blocksize=1)
        result1 = list(result1)
        self.assertEqual(result1[0], (1, 'mark'))

        result2 = self.testClass.fetch_sql_all(
            """
                SELECT * FROM temp_test_sql ORDER BY id ASC;
            """
            )
        self.assertEqual(result2, [(1, 'mark'), (2, 'alex')])

        result3 = self.testClass.fetch_sql_one(
            """
                SELECT * FROM temp_test_sql ORDER BY id ASC;
            """
            )
        self.assertEqual(result3, (1, 'mark'))

        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_test_sql;
            """
        )
        self.testClass.batch_commit()
        self.testClass.batch_close()
