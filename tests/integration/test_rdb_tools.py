import unittest

from codb.rdb_tools import DBInteraction
from cocore.config import Config


class TestDBInteraction(unittest.TestCase):

    def test_fetch_sql_all(self):
        print('--------------test_fetch_sql_all')
        mssql_conf = Config(conf_path='db.test.cfg')['mssql']
        self.testClass = DBInteraction(config=mssql_conf)
        result = self.testClass.fetch_sql_all('select current_timestamp')

    def test_fetch_sql_one_empty_string(self):
        print('--------------test__fetch_sql_one')
        mssql_conf = Config(conf_path='db.test.cfg')['mssql']
        self.testClass = DBInteraction(config=mssql_conf)
        result = self.testClass.fetch_sql_one('')

    def test_mssql_fetch_sql_one(self):
        print('--------------test_cosmo_fetch_sql_one')
        mssql_conf = Config(conf_path='db.test.cfg')['mssql']
        self.testClass = DBInteraction(config=mssql_conf)
        result = self.testClass.fetch_sql_one('''
             CREATE TABLE #TEST (
                [name] varchar(256)
                ,[age] int );

                INSERT INTO #TEST
                values ('Mike', 12)
                ,('someone else', 904);

                select count(1) FROM #TEST;
        ''')
        for r in result:
            self.assertEqual(2, r)

    def test_exec_sql(self):
        print('--------------test_exec_sql')
        mssql_conf = Config(conf_path='db.test.cfg')['mssql']
        self.testClass = DBInteraction(config=mssql_conf)
        self.testClass.exec_sql('''
                        CREATE TABLE #TEST (
                            [name] varchar(256)
                            ,[age] int );
                ''')

        self.testClass.exec_sql('''
                        INSERT INTO #TEST
                            values ('Mike', 12)
                            ,('someone else', 904);
                ''')

        result = self.testClass.fetch_sql_one('''
                        SELECT count(1) from #TEST;
                ''')
        for r in result:
            print(r)

    def test_url_from_conf(self):
        mssql_conf = Config(conf_path='db.test.cfg')['mssql']
        self.testClass = DBInteraction(config=mssql_conf)
        print('--------------test_url_from_conf')
        conf = {'type': 'postgres', 'user': 'test_user', 'password': 'test_password', 'port': 'test_port',
                'db_name': 'test_db_name', 'host': 'test_host'}
        from_conf = self.testClass.url_from_conf(conf)
        print(from_conf)
        self.assertEqual(True,
                         from_conf == 'postgresql+psycopg2://test_user:test_password@test_host:test_port/test_db_name')

        conf = {'type': 'mssql', 'user': 'test_user', 'password': 'test_password', 'server': 'test_server',
                'db_name': 'test_db_name'}
        from_conf = self.testClass.url_from_conf(conf)
        print(from_conf)
        self.assertEqual(True, from_conf == 'mssql+pytds://test_user:test_password@test_server:1433/test_db_name')
