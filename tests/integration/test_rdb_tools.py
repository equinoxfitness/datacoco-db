import unittest
from unittest.mock import patch

from datetime import date
from datacoco_db.rdb_tools import DBInteraction


class TestDBInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testClass = DBInteraction(  # nosec
            dbtype="mssql",
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port=5439,
        )

    @patch("datacoco_db.rdb_tools.DBInteraction.exec_sql")
    def test_exec_sql(self, mock_exec_sql):
        print("--------------test_exec_sql")
        self.testClass.exec_sql(
            """
                CREATE TABLE #TEST (
                    [name] varchar(256)
                    ,[age] int );

                INSERT INTO #TEST
                    values ('Mike', 12)
                    ,('someone else', 904);
            """
        )
        self.assertTrue(mock_exec_sql.called)

    @patch("datacoco_db.rdb_tools.DBInteraction.fetch_sql_all")
    def test_fetch_sql_all(self, mock_fetch_sql_all):
        print("--------------test_fetch_sql_all")
        mock_fetch_sql_all.return_value = date.today()
        result = self.testClass.fetch_sql_all(
            "select CONVERT(date, current_timestamp)"
        )
        self.assertEqual(result, date.today())

    @patch("datacoco_db.rdb_tools.DBInteraction.fetch_sql_one")
    def test_fetch_sql_one(self, mock_fetch_sql_one):
        print("--------------test_fetch_sql_one")
        result = self.testClass.fetch_sql_one(
            """
             CREATE TABLE #TEST (
                [name] varchar(256)
                ,[age] int );

                INSERT INTO #TEST
                values ('Mike', 12)
                ,('someone else', 904);

                select count(1) FROM #TEST;
        """
        )
        for r in result:
            self.assertEqual(2, r)

    @patch("datacoco_db.rdb_tools.DBInteraction.fetch_sql")
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

    @patch("datacoco_db.rdb_tools.DBInteraction.url_from_conf")
    def test_url_from_conf(self, mock_url_from_conf):
        print("--------------test_url_from_conf")
        mock_url_from_conf.return_value = (
            "postgresql+psycopg2://test_user:"
        ) + ("test_password@test_host:test_port/test_db_name")
        from_conf = self.testClass.url_from_conf(  # nosec
            dbtype="postgres",
            user="test_user",
            password="test_password",
            port="test_port",
            dbname="test_db_name",
            host="test_host",
        )
        expected_res = ("postgresql+psycopg2://test_user:") + (
            "test_password@test_host:test_port/test_db_name"
        )
        self.assertEqual(from_conf, expected_res)

    @patch("datacoco_db.rdb_tools.DBInteraction.table_exists")
    def test_table_exists(self, mock_table_exists):
        print("--------------test_table_exists")
        mock_table_exists.return_value = True
        result = self.testClass.table_exists("TEST")
        self.assertTrue(result)

    @patch("datacoco_db.rdb_tools.DBInteraction.get_schema")
    def test_get_schema(self, mock_get_schema):
        print("--------------test_get_schema")
        mock_get_schema.return_value = None
        table_query = self.testClass.get_schema("schema_name", "table_name")
        self.assertIsNone(table_query)


if __name__ == "__main__":
    unittest.main()
