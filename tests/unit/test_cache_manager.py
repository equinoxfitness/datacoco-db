import unittest
from unittest import mock

import datetime

from codb.cache_manager import CacheManager
from cocore.config import Config

SQL_DATA_RECORD_1 = [
                {'cdc_id': 1096771458, 'activityid': 6092932, 'modified_date': datetime.datetime(2047, 1, 1, 0, 0),
                 'roleid': '1002965250', 'changetype': 'Purchase'},

                {'cdc_id': 1096771459, 'activityid': 6092932, 'modified_date': datetime.datetime(2047, 1, 1, 0, 0),
                 'roleid': '1002965250', 'changetype': 'Purchase'}
            ]


class TestCacheManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testClass = CacheManager()

    @mock.patch('redis.StrictRedis')
    @mock.patch('codb.mssql_tools.MSSQLInteraction')
    def test_cache_sql_long(self, mock_strict_redis, mock_mssql_interaction):
        print('--------------test_cache_sql_long')
        # Redis
        mock_strict_redis.return_value = mock_strict_redis(host='server', port=6379, db='db')
        self.testClass.setup_cache('server', 6379, 'db')

        self.testClass.sqldb = mock_mssql_interaction(dbname='db_name', host='server', user='user',
                                                      password='password')
        self.testClass.sqldb.fetch_sql.return_value = SQL_DATA_RECORD_1

        self.testClass.cache_sql_long("select * from dbo.cdc_activity", 'cdc_id', 'cdc_id', 'cdc_id', TTL=5)

    @mock.patch('redis.StrictRedis')
    @mock.patch('codb.mssql_tools.MSSQLInteraction')
    def test_cache_sql(self, mock_strict_redis, mock_mssql_interaction):
        print('--------------test_cache_sql')
        mock_strict_redis.return_value = mock_strict_redis(host='server', port=6379, db='db')
        self.testClass.setup_cache('server', 6379, 'db')

        self.testClass.sqldb = mock_mssql_interaction(dbname='db_name', host='server', user='user',
                                                      password='password')
        self.testClass.sqldb.fetch_sql.return_value = SQL_DATA_RECORD_1

        self.testClass.cache_sql("select * from dbo.cdc_activity", 'cdc_id', TTL=5)

    @mock.patch('redis.StrictRedis')
    @mock.patch('codb.mssql_tools.MSSQLInteraction')
    def test_update_cache_from_sql(self, mock_strict_redis, mock_mssql_interaction):
        print('--------------test_update_cache_from_sql')
        mock_strict_redis.return_value = mock_strict_redis(host='server', port=6379, db='db')
        self.testClass.setup_cache('server', 6379, 'db')

        self.testClass.sqldb = mock_mssql_interaction(dbname='db_name', host='server', user='user',
                                                      password='password')
        self.testClass.sqldb.fetch_sql.return_value = SQL_DATA_RECORD_1

        self.testClass.update_cache_from_sql("select * from dbo.cdc_activity", '', 'cdc_id', TTL=5)

    @mock.patch('redis.StrictRedis')
    @mock.patch('codb.mssql_tools.MSSQLInteraction')
    def test_cache_multiple_records_to_field(self, mock_strict_redis, mock_mssql_interaction):
        print('--------------test_cache_multiple_records_to_field')
        mock_strict_redis.return_value = mock_strict_redis(host='server', port=6379, db='db')
        self.testClass.setup_cache('server', 6379, 'db')

        self.testClass.sqldb = mock_mssql_interaction(dbname='db_name', host='server', user='user',
                                                      password='password')
        self.testClass.sqldb.fetch_sql.return_value = SQL_DATA_RECORD_1

        self.testClass.cache_multiple_records_to_field([{"test_field": {"test_field": "test_value"}}], 'test_field', TTL=5)

    def test_append_multiple_records(self):
        print('--------------test_append_multiple_records')
        result = self.testClass.append_multiple_records([{"test_field": {"test_field": "test_value"}}], "test_field")
        print(result)
        self.assertEqual(True, result is not None)
