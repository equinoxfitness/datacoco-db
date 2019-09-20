import unittest
from unittest.mock import MagicMock

from codb.mssql_tools import MSSQLInteraction
from cocore.config import Config


class TestMSSQLInteraction(unittest.TestCase):

    def test_exec_sql(self):
        testCls = MSSQLInteraction(host='host', dbname='db_name',
                                              user='user', password='password')
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.exec_sql(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
    )

    def test_fetch_sql_all(self):
        testCls = MSSQLInteraction(host='host', dbname='db_name',
                                   user='user', password='password')
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.fetch_sql_all(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
    )

    def test_fetch_sql_all(self):
        testCls = MSSQLInteraction(host='host', dbname='db_name',
                                   user='user', password='password')
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.fetch_sql_all(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
    )

    def test_fetch_sql_one(self):
        testCls = MSSQLInteraction(host='host', dbname='db_name',
                                   user='user', password='password')
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.fetch_sql_one(
            """
               IF OBJECT_ID('#TEST', 'U') IS NOT NULL
               DROP TABLE #TEST;
           """
        )

    def test_get_table_columns(self):
        testCls = MSSQLInteraction(host='host', dbname='db_name',
                                   user='user', password='password')
        testCls.cur = MagicMock()
        testCls.con = MagicMock()
        testCls.get_table_columns('my_db.mytable')
