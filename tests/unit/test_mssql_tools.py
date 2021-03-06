import unittest
from unittest.mock import MagicMock

from datacoco_db.mssql_tools import MSSQLInteraction, MSSQLInteractionPyodbc


class TestMSSQLInteraction(unittest.TestCase):
    def test_exec_sql(self):
        testCls = MSSQLInteraction(  # nosec
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port="3306",
        )

        testCls = MSSQLInteraction(  # nosec
            host="host", dbname="db_name", user="user", password="password",
        )  # Default port test

        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.exec_sql(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
        )

    def test_fetch_sql_all(self):
        testCls = MSSQLInteraction(  # nosec
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port="3306",
        )
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.fetch_sql_all(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
        )

    def test_fetch_sql_one(self):
        testCls = MSSQLInteraction(  # nosec
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port="3306",
        )
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.fetch_sql_one(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
        )

    def test_get_table_columns(self):
        testCls = MSSQLInteraction(  # nosec
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port="3306",
        )
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.get_table_columns("my_db.mytable")


class TestMSSQLInteractionPyodbc(unittest.TestCase):
    def test_exec_sql(self):
        testCls = MSSQLInteractionPyodbc(  # nosec
            host="host",
            driver="driver",
            dbname="db_name",
            user="user",
            password="password",
        )
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.exec_sql(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
        )

    def test_fetch_sql_one(self):
        testCls = MSSQLInteractionPyodbc(  # nosec
            host="host",
            driver="driver",
            dbname="db_name",
            user="user",
            password="password",
        )
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.fetch_sql_one(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
        )

    def test_get_table_columns(self):
        testCls = MSSQLInteractionPyodbc(  # nosec
            host="host",
            driver="driver",
            dbname="db_name",
            user="user",
            password="password",
        )
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.get_table_columns("my_db.mytable")


if __name__ == "__main__":
    unittest.main()
