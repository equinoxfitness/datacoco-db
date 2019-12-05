import unittest

from datetime import date
from datacoco_db.rdb_tools import DBInteraction


class TestDBInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testClass = DBInteraction(
            dbtype="mssql",
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port="port",
        )

    def test_fetch_sql_all(self):
        print("--------------test_fetch_sql_all")
        result = self.testClass.fetch_sql_one(
            "select CONVERT(date, current_timestamp)"
        )
        self.assertEqual(result[0], date.today())

    def test_fetch_sql_one_empty_string(self):
        print("--------------test__fetch_sql_one")
        result = self.testClass.fetch_sql_one("SELECT ''")
        self.assertEqual(result[0], "")

    def test_mssql_fetch_sql_one(self):
        print("--------------test_cosmo_fetch_sql_one")
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

    def test_exec_sql(self):
        print("--------------test_exec_sql")
        self.testClass.exec_sql(
            """
                        CREATE TABLE #TEST (
                            [name] varchar(256)
                            ,[age] int );
                """
        )

        self.testClass.exec_sql(
            """
                        INSERT INTO #TEST
                            values ('Mike', 12)
                            ,('someone else', 904);
                """
        )

        result = self.testClass.fetch_sql_one(
            """
                        SELECT count(1) from #TEST;
                """
        )
        for r in result:
            print(r)

    def test_url_from_conf(self):
        print("--------------test_url_from_conf")
        from_conf = self.testClass.url_from_conf(
            dbtype="postgres",
            user="test_user",
            password="test_password",
            port="test_port",
            dbname="test_db_name",
            host="test_host",
        )
        print(from_conf)
        expected_res = ("postgresql+psycopg2://test_user:") + (
            "test_password@test_host:test_port/test_db_name"
        )
        self.assertEqual(True, from_conf == expected_res)

        from_conf = self.testClass.url_from_conf(
            dbtype="mssql",
            user="test_user",
            password="test_password",
            host="test_server",
            dbname="test_db_name",
            port="1433",
        )
        print(from_conf)
        expected_res = ("mssql+pytds://test_user:") + (
            "test_password@test_server:1433/test_db_name"
        )
        self.assertEqual(True, from_conf == expected_res)
