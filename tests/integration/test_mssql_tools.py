import unittest
import tempfile
import os

from datacoco_db.mssql_tools import MSSQLInteraction


class TestMSSQLInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testClass = MSSQLInteraction(
            host="host",
            dbname="db_name",
            user="user",
            password="password",
            port=1433,
        )

    def test_database(self):
        print("--------------test_database")
        self.testClass.conn()

        self.testClass.batch_open()

        self.testClass.exec_sql(
            """
                IF OBJECT_ID('#TEST', 'U') IS NOT NULL
                DROP TABLE #TEST;
            """
        )

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

        result = self.testClass.fetch_sql_all("select * from #TEST")
        self.assertEqual(True, len(result) > 0)

        result = self.testClass.fetch_sql_all(
            "select count(*) from table_name"
        )
        print(result)

        # get table columns
        result = self.testClass.get_table_columns("table_name")
        self.assertEqual(True, len(result) > 0)

        # export sql to csv
        new_file, filename = tempfile.mkstemp()
        print("filename csv: " + filename)
        result = self.testClass.export_sql_to_csv(
            "select * from #TEST", filename
        )
        print(result)
        os.close(new_file)

        self.testClass.batch_close()


if __name__ == "__main__":
    unittest.main()
