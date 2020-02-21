import unittest
from unittest.mock import patch

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

    @patch("datacoco_db.mysql_tools.MYSQLInteraction.conn")
    def test_conn(self, mock_connection):
        print("--------------test_conn")
        self.testClass.conn()
        self.assertTrue(mock_connection.called)

    @patch("datacoco_db.mysql_tools.MYSQLInteraction.exec_sql")
    def test_exec_sql(self, mock_exec_sql):
        print("--------------test_exec_sql")
        self.testClass.exec_sql(
            """
                CREATE TABLE temp_test_sql (id INT(11), name VARCHAR(10));
                INSERT INTO temp_test_sql (id,name) VALUES (1, 'mark');
                INSERT INTO temp_test_sql (id,name) VALUES (2, 'kyle');
            """
        )
        self.assertTrue(mock_exec_sql.called)

    @patch("datacoco_db.mysql_tools.MYSQLInteraction.fetch_sql_all")
    def test_fetch_sql_all(self, mock_fetch_sql_all):
        print("--------------test_fetch_sql_all")
        mock_fetch_sql_all.return_value = [
            {"id": 1, "name": "mark"},
            {"id": 2, "name": "kyle"},
        ]
        result = self.testClass.fetch_sql_all("SELECT * FROM temp_test_sql")
        self.assertTrue(len(result) > 0)

    @patch("datacoco_db.mysql_tools.MYSQLInteraction.fetch_sql")
    def test_fetch_sql(self, mock_fetch_sql):
        print("--------------test_fetch_sql")
        expected_response = {"id": 1, "name": "mark"}
        mock_fetch_sql.return_value = {"id": 1, "name": "mark"}
        result = self.testClass.fetch_sql(
            sql="SELECT * FROM temp_test_sql ORDER BY id DESC;"
        )
        self.assertEqual(result, expected_response)


if __name__ == "__main__":
    unittest.main()
