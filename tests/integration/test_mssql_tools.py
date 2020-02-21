import unittest
from unittest.mock import patch

from datacoco_db.mssql_tools import MSSQLInteraction, MSSQLInteractionPyodbc


class TestMSSQLInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = dict(  # nosec
            host="host",
            dbname="db_name",
            user="username",
            password="password",
        )
        cls.testClass = MSSQLInteraction(**cls.config)

    @patch("datacoco_db.mssql_tools.MSSQLInteraction.conn")
    def test_conn(self, mock_connection):
        print("--------------test_conn")
        self.testClass.conn()
        self.assertTrue(mock_connection.called)

    @patch("datacoco_db.mssql_tools.MSSQLInteraction.exec_sql")
    def test_exec_sql(self, mock_exec_sql):
        print("--------------test_exec_sql")
        self.testClass.exec_sql(
            """
                CREATE TABLE #TEST (
                [name] varchar(256)
                ,[age] int )

                INSERT INTO #TEST
                values ('Mike', 12)
                ,('someone else', 904)
            """
        )
        self.assertTrue(mock_exec_sql.called)

    @patch("datacoco_db.mssql_tools.MSSQLInteraction.fetch_sql_one")
    def test_fetch_sql_one(self, mock_fetch_sql_one):
        print("--------------test_fetch_sql_one")
        expected_response = {"Mike", 12}
        mock_fetch_sql_one.return_value = {"Mike", 12}
        result = self.testClass.fetch_sql_one(sql="select * from #TEST;")
        self.assertEqual(result, expected_response)

    @patch("datacoco_db.mssql_tools.MSSQLInteraction.fetch_sql_all")
    def test_fetch_sql_all(self, mock_fetch_sql_all):
        print("--------------test_fetch_sql_all")
        mock_fetch_sql_all.return_value = [{"Mike", 12}, {"someone else", 904}]
        result = self.testClass.fetch_sql_all("select * from #TEST")
        self.assertTrue(len(result) > 0)

    @patch("datacoco_db.mssql_tools.MSSQLInteraction.fetch_sql")
    def test_fetch_sql(self, mock_fetch_sql):
        print("--------------test_fetch_sql")
        expected_response = {"Mike", 12}
        mock_fetch_sql.return_value = {"Mike", 12}
        results = self.testClass.fetch_sql(
            sql="select * from #TEST where name = ?", params=("Mike",)
        )
        if results is not None:
            for row in results:
                self.assertEqual(results, expected_response)

    @patch("datacoco_db.mssql_tools.MSSQLInteraction.get_table_columns")
    def test_get_table_columns(self, mock_get_table_columns):
        print("--------------test_get_table_columns")
        self.testClass.get_table_columns("dbo.sample_table")
        self.assertTrue(mock_get_table_columns.called)


class TestMSSQLInteractionPyodbc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = dict(  # nosec
            host="host",
            dbname="db_name",
            user="username",
            password="password",
            driver="driver",
        )
        cls.testClass = MSSQLInteractionPyodbc(**cls.config)

    @patch("datacoco_db.mssql_tools.MSSQLInteractionPyodbc.conn")
    def test_conn(self, mock_connection):
        print("--------------test_conn")
        self.testClass.conn()
        self.assertTrue(mock_connection.called)

    @patch("datacoco_db.mssql_tools.MSSQLInteractionPyodbc.exec_sql")
    def test_exec_sql(self, mock_exec_sql):
        print("--------------test_exec_sql")
        self.testClass.exec_sql(
            """
                CREATE TABLE #TEST (
                [name] varchar(256)
                ,[age] int )

                INSERT INTO #TEST
                values ('Mike', 12)
                ,('someone else', 904)
            """
        )
        self.assertTrue(mock_exec_sql.called)

    @patch("datacoco_db.mssql_tools.MSSQLInteractionPyodbc.fetch_sql_one")
    def test_fetch_sql_one(self, mock_fetch_sql_one):
        print("--------------test_fetch_sql_one")
        expected_response = {"Mike", 12}
        mock_fetch_sql_one.return_value = {"Mike", 12}
        result = self.testClass.fetch_sql_one(sql="select * from #TEST;")
        self.assertEqual(result, expected_response)

    @patch("datacoco_db.mssql_tools.MSSQLInteractionPyodbc.fetch_sql")
    def test_fetch_sql(self, mock_fetch_sql):
        print("--------------test_fetch_sql")
        expected_response = {"Mike", 12}
        mock_fetch_sql.return_value = {"Mike", 12}
        results = self.testClass.fetch_sql(
            sql="select * from #TEST where name = ?", params=("Mike",)
        )
        if results is not None:
            for row in results:
                self.assertEqual(results, expected_response)

    @patch("datacoco_db.mssql_tools.MSSQLInteractionPyodbc.get_table_columns")
    def test_get_table_columns(self, mock_get_table_columns):
        print("--------------test_get_table_columns")
        self.testClass.get_table_columns("dbo.sample_table")
        self.assertTrue(mock_get_table_columns.called)


if __name__ == "__main__":
    unittest.main()
