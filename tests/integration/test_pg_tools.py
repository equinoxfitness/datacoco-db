import unittest
import tempfile
import os

from datacoco_db.pg_tools import PGInteraction


class TestPGInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.testClass = PGInteraction(
                host="host",
                dbname="db_name",
                user="user",
                password="password",
                port=5439,
                schema="public",
            )
        except Exception as e:
            print(e)

    @unittest.skip("enable this for integration testing, modify connection")
    def test_database(self):
        print("--------------test_database")
        self.testClass.conn()
        self.testClass.batch_open()
        exists = self.testClass.table_exists("table_name")
        print("table_name: " + str(exists))
        self.assertEqual(True, exists[0])
        self.testClass.exec_sql(
            """
                DROP TABLE IF EXISTS temp_sql_count;
            """
        )
        self.testClass.exec_sql("commit;")
        self.testClass.exec_sql(
            """
                CREATE TEMPORARY TABLE temp_sql_count
                AS
                SELECT COUNT(*) as cache_count
                FROM table_name;
            """
        )
        self.testClass.batch_commit()
        self.testClass.bulk_dictionary_insert(
            "temp_sql_count", {"cache_count": 0}
        )
        results = self.testClass.fetch_sql("select * from temp_sql_count")
        for result in results:
            print(result)

        # export to csv
        new_file, filename = tempfile.mkstemp()
        print("filename csv: " + filename)
        self.testClass.export_sql_to_csv(
            "select * from temp_sql_count", filename
        )
        os.close(new_file)

        # export to json
        new_file, filename = tempfile.mkstemp()
        print("filename json: " + filename)
        self.testClass.export_sql_to_json(
            "select * from temp_sql_count", filename
        )
        os.close(new_file)

        # export to s3 (modify connection)
        self.testClass.export_sql_to_s3(
            sql="select * from temp_sql_count",
            s3path="s3://temp_bucket/datacocodb-test.txt",
            aws_access_key="aws_access_key",
            aws_secret_key="aws_secret_key",
        )

        self.testClass.batch_close()


if __name__ == "__main__":
    unittest.main()
