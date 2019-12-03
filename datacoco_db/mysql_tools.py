"""
    MYSQLInteraction
"""
import pymysql.cursors
import pymysql

from datacoco_db.helper.config import config

CONF = config()


class MYSQLInteraction:
    """
    Simple class for interacting with MYSSQL
    """

    def __init__(
        self,
        dbname=None,
        host=None,
        user=None,
        password=None,
        connection=None,
        port=3306,
    ):

        # if there is a connection, we will pull from config,
        # else we use the individual connection pararameters (this is really just for backward compatibility
        if connection:
            user = CONF[connection]["user"]
            password = CONF[connection]["password"]
            host = CONF[connection]["host"]
            dbname = CONF[connection]["db_name"]
            try:
                port = CONF[connection]["port"]
            except KeyError:
                port = 3306

        else:
            if not dbname or not host or not user or password is None:
                raise RuntimeError("%s request all __init__ arguments" % __name__)

        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.con = None
        self.cur = None
        self.dict_cursor = None

    def conn(self, dict_cursor=False):
        """

            Open a connection, should be done right before time of insert
        """
        try:
            options = {
                "host": self.host,
                "user": self.user,
                "password": self.password,
                "db": self.dbname,
                "charset": "utf8mb4",
            }
            if dict_cursor:
                options["cursorclass"] = pymysql.cursors.DictCursor
            self.con = pymysql.connect(**options)
            self.dict_cursor = dict_cursor
        except Exception as err:
            raise

    def batch_open(self):
        self.cur = self.con.cursor()

    def batch_commit(self):
        self.con.commit()

    def batch_close(self):
        self.con.close()

    def fetch_sql_all(self, sql):
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
        except Exception as e:
            raise
        return results

    def fetch_sql(self, sql):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
        except Exception as e:
            raise
        return result

    def exec_sql(self, sql, auto_commit=True):
        self.cur.execute(sql)
        if auto_commit:
            self.con.commit()
