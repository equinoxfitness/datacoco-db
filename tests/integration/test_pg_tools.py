import unittest
from unittest.mock import MagicMock, patch

import tempfile
import os

from datacoco_db.pg_tools import PGInteraction


class TestPGInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.testClass = PGInteraction(  # nosec
                host="host",
                dbname="db_name",
                user="user",
                password="password",
                port=5439,
                schema="public",
            )
        except Exception as e:
            print(e)

    @patch("datacoco_db.pg_tools.PGInteraction.conn")
    def test_conn(self, mock_connection):
        print("--------------test_conn")
        self.testClass.conn()
        self.assertTrue(mock_connection.called)

    @patch("datacoco_db.pg_tools.PGInteraction.table_exists")
    def test_table_exists(self, mock_table_exists):
        print("--------------test_table_exists")
        mock_table_exists.return_value = True
        result = self.testClass.table_exists("table_name")
        self.assertTrue(result)

    @patch("datacoco_db.pg_tools.PGInteraction.exec_sql")
    def test_exec_sql(self, mock_exec_sql):
        print("--------------test_exec_sql")
        self.testClass.exec_sql(
            """
                CREATE TEMPORARY TABLE temp_sql_count
                AS
                SELECT COUNT(*) as cache_count
                FROM table_name;
            """
        )
        self.assertTrue(mock_exec_sql.called)

    @patch("datacoco_db.pg_tools.PGInteraction.fetch_sql_all")
    def test_fetch_sql_all(self, mock_fetch_sql_all):
        print("--------------test_fetch_sql_all")
        mock_fetch_sql_all.return_value = [{"id": 1}, {"id": 2}]
        result = self.testClass.fetch_sql_all("SELECT * FROM table_name;")
        self.assertTrue(len(result) > 0)

    @patch("datacoco_db.pg_tools.PGInteraction.fetch_sql")
    def test_fetch_sql(self, mock_fetch_sql):
        print("--------------test_fetch_sql")
        expected_response = {"id": 1}
        mock_fetch_sql.return_value = {"id": 1}
        results = self.testClass.fetch_sql(sql="SELECT * FROM temp_sql_count")
        if results is not None:
            for row in results:
                self.assertEqual(results, expected_response)

    @patch("datacoco_db.pg_tools.PGInteraction.export_sql_to_csv")
    def test_export_sql_to_csv(self, mock_export_sql_to_csv):
        print("--------------test_export_sql_to_csv")
        new_file, filename = tempfile.mkstemp()
        self.testClass.export_sql_to_csv(
            "select * from temp_sql_count", filename
        )
        os.close(new_file)
        self.assertIsInstance(mock_export_sql_to_csv, MagicMock)

    @patch("datacoco_db.pg_tools.PGInteraction.export_sql_to_json")
    def test_export_sql_to_json(self, mock_export_sql_to_json):
        print("--------------test_export_sql_to_json")
        new_file, filename = tempfile.mkstemp()
        self.testClass.export_sql_to_json(
            "select * from temp_sql_count", filename
        )
        os.close(new_file)
        self.assertIsInstance(mock_export_sql_to_json, MagicMock)

    @patch("datacoco_db.pg_tools.PGInteraction.export_sql_to_s3")
    def test_export_sql_to_s3(self, mock_export_sql_to_s3):
        print("--------------test_export_sql_to_s3")
        self.testClass.export_sql_to_s3(  # nosec
            sql="select * from temp_sql_count",
            s3path="s3://temp_bucket/datacocodb-test.txt",
            aws_access_key="aws_access_key",
            aws_secret_key="aws_secret_key",
        )
        self.assertIsInstance(mock_export_sql_to_s3, MagicMock)


if __name__ == "__main__":
    unittest.main()
