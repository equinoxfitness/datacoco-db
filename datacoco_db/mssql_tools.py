#!/usr/bin/env python
"""
    MSSQLInteraction
"""
import csv
import re
import pytds
import pyodbc

from datacoco_db.helper.deprecate import deprecated

NON_CSV_CHARS = re.compile(r"[\t\n]")


class MSSQLInteractionBase:
    def __csv_cleanup(self, raw_s):
        encoded = str(raw_s).encode("utf-8")
        return NON_CSV_CHARS.sub(" ", encoded.decode())

    def __result_iter_pytds(self, cursor, arraysize: int = None):
        "An iterator that uses fetchmany to keep memory usage down"
        count = 0
        while True:
            blocksize = 1
            if arraysize is not None:
                blocksize = arraysize
            results = cursor.fetchmany(blocksize)
            count += len(results)
            if not results or count < 1:
                print("no rows to process")
                break
            print("%s rows processed" % count)
            for result in results:
                yield result

    def __result_iter_pyodbc(
        self, cursor, arraysize: int = 1000, dict_cursor: bool = False
    ):
        "An iterator that uses fetchmany to keep memory usage down"
        count = 0
        while True:
            if dict_cursor:
                # Get the columns from cursor.description
                # since pyodbc fetchmany() only returns tuple.
                columns = [column[0] for column in cursor.description]
            blocksize = 1
            if arraysize is not None:
                blocksize = arraysize
            results = cursor.fetchmany(blocksize)
            count += len(results)
            if not results or count < 1:
                print("no rows to process")
                break
            print("%s rows processed" % count)
            for result in results:
                if dict_cursor:
                    yield dict(zip(columns, result))
                else:
                    yield result

    def batch_commit(self):
        self.con.commit()

    @deprecated("Use batch_open() instead")
    def batchOpen(self):
        self.batch_open()

    def batch_open(self):
        self.cur = self.con.cursor()

    @deprecated("Use batch_close() instead")
    def batchClose(self):
        self.batch_close()

    def batch_close(self):
        self.con.close()

    def export_sql_to_csv(
        self, sql, csv_filename, delimiter=",", headers=True, params=None
    ):
        result = self.fetch_sql(sql, params)
        try:
            f = open(csv_filename, "w", newline="")
            writer = csv.writer(f, delimiter=delimiter)
            if headers:
                # write headers if we have them
                writer.writerow([i[0] for i in self.cur.description])
            for row in result:
                writer.writerow([self.__csv_cleanup(s) for s in row])
            f.flush()
            f.close()
            return True
        except Exception as e:
            print(e)
            return False

    def exec_sql(self, sql, auto_commit=True):
        try:
            self.cur.execute(sql)
            self.cur.nextset()
            if auto_commit:
                self.con.commit()
        except Exception as e:
            print("exec_sql error: ", str(e))
            raise

    def fetch_sql_one(self, sql):
        statements = sql.strip().split(";")
        statements = list(filter(lambda x: x.strip() != "", statements))
        index = 0
        for statement in statements:
            if index != len(statements) - 1:
                self.exec_sql(statement)
            else:  # Assuming last statement is a select query.
                results = self.fetch_sql(statement)
                for row in results:
                    return row
            index += 1

    @deprecated("Use get_table_columns() instead")
    def getTableColumns(self, table_name):
        self.get_table_columns(table_name)


class MSSQLInteraction(MSSQLInteractionBase):
    """
    Simple class for interacting with MSSQL
    """

    def __init__(
        self, dbname=None, host=None, user=None, password=None, port=1433,
    ):
        if not dbname or not host or not user or not port or password is None:
            raise RuntimeError("%s request all __init__ arguments" % __name__)

        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port
        self.con = None
        self.cur = None

    def conn(self, dict_cursor=False):
        """Open a connection, should be done right before time of insert
        """
        if "\\" in self.host:
            self.con = pytds.connect(
                self.host,
                self.dbname,
                self.user,
                self.password,
                as_dict=dict_cursor,
                login_timeout=360,
            )
        else:
            self.con = pytds.connect(
                self.host,
                self.dbname,
                self.user,
                self.password,
                port=self.port,
                as_dict=dict_cursor,
                login_timeout=360,
            )

    def fetch_sql_all(self, sql, params=None):
        try:
            self.__execute_with_or_without_params(sql, params)
            results = self.cur.fetchall()
        except Exception as e:
            print(e)
            raise
        return results

    def fetch_sql(self, sql, blocksize=1000, params=None):
        """
        :param sql: The query you want run, which may require parameters
        :param blocksize: int
        :param params: tuple key value
        :return generator object
        """
        try:
            self.__execute_with_or_without_params(sql, params)
            results = self._MSSQLInteractionBase__result_iter_pytds(
                cursor=self.cur, arraysize=blocksize
            )
        except Exception as e:
            print(e)
            raise
        return results

    def get_table_columns(self, table_name):
        name_parts = table_name.split(".")
        schema = name_parts[0]
        table = name_parts[1]
        sql = """
          SELECT column_name
          FROM information_schema.columns
          WHERE table_schema = %s and table_name = %s;"""
        return self.fetch_sql_all(sql, params=(schema, table))

    def __execute_with_or_without_params(self, sql, params):
        """
        :param sql: The query you want run, which may require parameters
        :param params: The query parameters you should escape, may be None
        :return: None
        """
        if params is not None:
            if not isinstance(params, tuple):
                raise ValueError(
                    "Passed in parameters must be in a tuple: %s", params
                )
            self.cur.execute(sql, params)
        else:
            self.cur.execute(sql)


class MSSQLInteractionPyodbc(MSSQLInteractionBase):
    """
        simple class for interacting with MSSQL
    """

    def __init__(
        self,
        driver=None,
        dbname=None,
        host=None,
        user=None,
        password=None,
        connection=None,
        port=1433,
    ):

        if (
            not dbname
            or not driver
            or not host
            or not user
            or not port
            or password is None
        ):
            raise RuntimeError("%s request all __init__ arguments" % __name__)

        self.host = host
        self.user = user
        self.driver = driver
        self.password = password
        self.dbname = dbname
        self.port = port
        self.con = None
        self.cur = None

        # Default false, pyodbc will return in tuple format.
        self.dict_cursor = False

    def conn(self, dict_cursor: bool = False):
        """Open a connection, should be done right before time of insert
        """
        conf = (
            f"DRIVER={self.driver};SERVER={self.host};"
            f"DATABASE={self.dbname};UID={self.user};PWD={self.password};"
        )

        if "\\" not in self.host:
            conf += f"PORT={self.port}"

        # Tell pyodbc to return results in dict format
        if dict_cursor:
            self.dict_cursor = True
        self.con = pyodbc.connect(conf)

    @deprecated("Use fetch_sql() instead")
    def fetch_sql_all(self, sql, params=None):
        return self.fetch_sql(sql=sql, params=params)

    def fetch_sql(self, sql, blocksize=1000, params=None):
        """
        :param sql: The query you want run, which may require parameters
        :param blocksize: int
        :param params: tuple key value
        :return generator object
        """
        try:
            res = self.__execute_with_or_without_params(sql, params)
            results = self._MSSQLInteractionBase__result_iter_pyodbc(
                cursor=res, arraysize=blocksize, dict_cursor=self.dict_cursor
            )
            if self.dict_cursor:
                return [item for item in results]
            return results
        except Exception as e:
            print(e)
            raise

    def get_table_columns(self, table_name):
        name_parts = table_name.split(".")
        schema = name_parts[0]
        table = name_parts[1]
        sql = """
          SELECT column_name
          FROM information_schema.columns
          WHERE table_schema = ? and table_name = ?;"""
        results = self.fetch_sql(sql, params=(schema, table))
        return [item for item in results]

    def __execute_with_or_without_params(self, sql, params):
        """
        :param sql: The query you want run, which may require parameters
        :param params: The query parameters you should escape, may be None
        :return: None
        """
        if params is not None:
            if not isinstance(params, tuple):
                raise ValueError(
                    "Passed in parameters must be in a tuple: %s", params
                )
            return self.cur.execute(sql, params)
        else:
            return self.cur.execute(sql)
