"""
    SQLiteInteraction
"""
import sqlite3
from sqlite3 import Error
from cocore.Logger import Logger

LOG = Logger()

def _result_iter(cursor, arraysize):
    """
    An iterator that uses fetchmany to keep memory usage down
    """
    count = 0
    while True:
        results = cursor.fetchmany(arraysize)
        count += len(results)
        if not results:
            LOG.l("no rows to process")
            break
        LOG.l("%s rows processed" % count)
        for result in results:
            yield result

class SQLiteInteraction:
    
    def __init__(self, db_file):

        self.db_file = db_file
        self.con = None
        self.cur = None

    def conn(self):
        """
        Open a connection
        """
        try:
            self.con = sqlite3.connect(self.db_file)
        except Error as e:
            LOG.l(e)

    def batch_open(self):
        self.cur = self.con.cursor()

    def batch_commit(self):
        self.con.commit()

    def batch_close(self):
        self.con.close()

    def fetch_sql_all(self, sql):
        """
        :param sql:
        :return:
        """
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
        except Error as e:
            LOG.l(e)
        return results

    def fetch_sql(self, sql, blocksize=1000):
        """
        :param sql:
        :param blocksize:
        :return:
        """
        try:
            self.cur.execute(sql)
            results = _result_iter(self.cur, blocksize)
        except Error as e:
            LOG.l(e)
        return results

    def fetch_sql_one(self, sql):
        """
        :param sql:
        :return:
        """
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
        except Error as e:
            LOG.l(e)
        return result

    def exec_sql(self, sql, auto_commit=True):
        """
        :param sql:
        :param auto_commit:
        """
        try:
            self.cur.execute(sql)
            if auto_commit:
                self.con.commit()
        except Error as e:
            LOG.l(e)
