datacoco-db
===========

.. image:: https://badge.fury.io/py/datacoco-db.svg
    :target: https://badge.fury.io/py/datacoco-db
    :alt: PyPI Version

.. image:: https://readthedocs.org/projects/datacocodb/badge/?version=latest
    :target: https://datacocodb.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/4d85afc6c49f40eab14f9aa60336ac64
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-db?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-db&amp;utm_campaign=Badge_Grade
    :alt: Code Quality Grade

.. image:: https://api.codacy.com/project/badge/Coverage/4d85afc6c49f40eab14f9aa60336ac64
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-db?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-db&amp;utm_campaign=Badge_Coverage
    :alt: Coverage

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
    :target: https://github.com/equinoxfitness/datacoco-db/blob/master/CODE_OF_CONDUCT.rst
    :alt: Code of Conduct

Equinox Common Code Utility for Python 3 for DB interactions! There are
currently interaction classes for the following DBs and Apps:

-  MSSQL
-  MySQL
-  SQLite
-  Postgres
-  Redshift

Quick Start
-----------

Sample Usage

::

    from datacoco_db import MSSQLInteraction

    mssql = MSSQLInteraction(dbname="db_name",
                            host="server",
                            user="user",
                            password="password",
                            port=1433)

    mssql.conn() # open a connection

    mssql.batch_open() # cursor

    results = mssql.fetch_sql_one("SELECT * FROM MyTable") # fetch one

    print(results)

    mssql.batch_close() # close cursor

The example above makes use of mssql_tools.
All tools follows the same pattern in terms of usage.

Installation
------------

datacoco-db requires Python 3.6+

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install datacoco-db

Development
-----------

Getting Started
~~~~~~~~~~~~~~~

It is recommended to use the steps below to set up a virtual environment for development:

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install -r requirements.txt

Pyodbc Dependency Installation
------------------------------

Installing the Microsoft ODBC Driver for SQL Server on Linux and macOS
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15


Testing
~~~~~~~

::

    pip install -r requirements-dev.txt

Modify the connection configuration for integration testing.

To run the testing suite, simply run the command: ``python -m unittest discover tests``

For coverage report, run ``tox`` View the results in
.tox/coverage/index.html

Contributing
~~~~~~~~~~~~

Contributions to datacoco\_db are welcome!

Please reference guidelines to help with setting up your development
environment
`here <https://github.com/equinoxfitness/datacoco-db/blob/master/CONTRIBUTING.rst>`__.