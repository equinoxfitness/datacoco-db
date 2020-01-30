import unittest

from datacoco_db.mssql_tools import MSSQLInteraction


class TestMSSQLInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testClass = MSSQLInteraction(  # nosec
            host="host",
            dbname="db_name",
            user="username",
            password="password",
        )

        print("--------------setup_test_table")
        cls.testClass.conn()

        cls.testClass.batch_open()

        # Drop table TEST if exists
        cls.testClass.exec_sql(
            """
                IF OBJECT_ID('#TEST', 'U') IS NOT NULL
                DROP TABLE #TEST;
            """
        )

        # Create table TEST
        cls.testClass.exec_sql(
            """
                       CREATE TABLE #TEST (
                        [name] varchar(256)
                        ,[age] int )

                        INSERT INTO #TEST
                        values ('Mike', 12)
                        ,('someone else', 904)
                    """
        )

    def test_get_table_columns(self):
        # get table columns
        result = self.testClass.get_table_columns("dbo.cdc_activity")
        self.assertEqual(True, len(result) > 0)

    def test_fetch_one(self):
        results = self.testClass.fetch_sql(
            sql="select * from #TEST where name = ?", params=("Mike",)
        )
        if results is not None:
            for row in results:
                name, age = row
                self.assertEqual("Mike", name)

    def test_fetch_sql_one(self):
        result = self.testClass.fetch_sql_one(sql="select * from #TEST;")
        name, age = result
        self.assertEqual("Mike", name)

    def test_fetch_all(self):
        result = self.testClass.fetch_sql_all("select * from #TEST")
        self.assertEqual(True, len(result) > 0)

    @classmethod
    def tearDownClass(cls):
        print("--------------tear down")
        cls.testClass.batch_close()


if __name__ == "__main__":
    unittest.main()
