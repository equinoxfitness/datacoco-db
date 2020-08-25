#!/usr/bin/env python
"""
    DBInteraction
"""

import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy.dialects import registry

registry.register("mssql.pytds", "sqlalchemy_pytds.dialect", "MSDialect_pytds")


# iter from old datacoco also suggested for sqlalchemy
# sqlalchemy has a stream_results execution option but only works for psycopg
def _result_iter(cursor, arraysize):
    "An iterator that uses fetchmany to keep memory usage down"
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result


class DBInteraction:
    """
    This module provides a simple wrapper on top of SqlAlchemy
    """

    def __init__(
        self,
        dbtype=None,
        dbname=None,
        host=None,
        user=None,
        password=None,
        port=None,
    ):
        if not dbname or not host or not user or password is None:
            raise RuntimeError("%s request all __init__ arguments" % __name__)

        self.url = DBInteraction.url_from_conf(
            dbtype, dbname, host, user, password, port
        )

        # Used for explicit connectionless execution
        self.con = sqlalchemy.create_engine(self.url)

        # Necessary for splitting common functions from each other
        self.db_type = dbtype

        part = self.url.split(":", 3)
        db = part[2].split("@")
        print(part[0], part[1], db[1])

    def fetch_sql(self, sql, blocksize=1000):
        try:
            cursor = self.con.execute(sql)
            results = _result_iter(cursor, arraysize=blocksize)
        except Exception as e:
            raise RuntimeError(e)
        return results

    def fetch_sql_all(self, sql):
        try:
            results = self.con.execute(sql)
        except Exception as e:
            raise e
        return results

    def fetch_sql_one(self, sql):
        try:
            statements = sql.strip().split(";")
            statements = list(
                map(lambda x: self.remove_comments(x), statements)
            )
            statements = list(filter(lambda x: x.strip() != "", statements))
            index = 0
            for statement in statements:
                if index != len(statements) - 1:
                    self.exec_sql(statement)
                else:  # Assuming last statement is a select query.
                    results = self.fetch_sql_all(statement)
                    for row in results:
                        return row

                index += 1

        except Exception as e:
            print(
                """
               Something is not right with the query, please check query
               1. Avoid comments at the start of the query, if you do use a
               comment at the start. add `;` at the end of the comment.
               2. Multi-line-statement is allowed, it's just that we make sure
               that select query is at the last statement
               3. Let's use this function for fetching.
            """
            )

            raise e

    def get_schema(self, schema_name, table_name):
        if self.db_type == "spectrum":
            metadata_sql = """
                select
                    columnname,
                    external_type,
                    columnnum,
                    part_key
                from pg_catalog.svv_external_columns
                where schemaname = lower('%s') and tablename = lower('%s')
                order by columnnum asc;
            """ % (  # nosec
                schema_name,
                table_name,
            )
        else:
            metadata_sql = """
                select
                    column_name,
                    data_type,
                    character_maximum_length,
                    numeric_precision,
                    numeric_scale
                from information_schema.columns
                where table_schema=lower('%s') and table_name=lower('%s')
                order by ordinal_position
            """ % (  # nosec
                schema_name,
                table_name,
            )

        results = self.fetch_sql_one(metadata_sql)
        return results

    def table_exists(self, schema_name, table_name):
        table_query = self.get_schema(schema_name, table_name)
        if table_query is None:
            return False
        else:
            return True

    def batch_close(self):
        self.con.close()

    @staticmethod
    def remove_comments(x):
        try:
            if x.strip().index("--") == 0:
                return x.replace(x[x.index("--") :], "")
        except Exception as err:
            pass
        return x

    def exec_sql(self, sql, params=None):
        """
        :param sql: The query you want run, which may require parameters
        :param params: The query parameters you should escape, may be None
        :return: None
        """
        try:
            # sqlalchemy does not require params to be tuple
            if params:
                if not isinstance(params, tuple):
                    raise ValueError(
                        "Passed in parameters must be in a tuple: %s", params
                    )
                results = self.con.execute(
                    text(sql).execution_options(autocommit=True), params
                )
            else:
                results = self.con.execute(
                    text(sql).execution_options(autocommit=True)
                )
            return results
        except Exception as e:
            raise e

    @staticmethod
    def url_from_conf(
        dbtype=None,
        dbname=None,
        host=None,
        user=None,
        password=None,
        port=None,
    ):
        if dbtype == "postgres":
            url = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
                user,
                password,
                host,
                port if port is not None else "5439",
                dbname,
            )
        elif dbtype == "mssql":
            url = "mssql+pytds://%s:%s@%s:%s/%s" % (
                user,
                password,
                host,
                port if port is not None else "1433",
                dbname,
            )
        elif dbtype == "mysql":
            url = "mysql+pymysql://%s:%s@%s:%s/%s" % (
                user,
                password,
                host,
                port if port is not None else "3306",
                dbname,
            )
        else:
            url = ""
        return url
