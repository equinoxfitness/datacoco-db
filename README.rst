Datacoco - DB
=============

.. image:: https://api.codacy.com/project/badge/Grade/4d85afc6c49f40eab14f9aa60336ac64
    :target: https://www.codacy.com/manual/meikalei/datacoco-db?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-db&amp;utm_campaign=Badge_Grade

Equinox Common Code Utility for Python 3 for DB interactions! There are
currently interaction classes for the following DBs and Apps:

-  Postgres/Redshift
-  MSSQL
-  MySQL
-  SQLITE

Development
-----------

Getting Started
~~~~~~~~~~~~~~~

It is recommended to use the steps below to set up a virtual environment
for development:

::

    python3 -m venv <virtual env name>
    source venv/bin/activate
    pip install -r requirements-dev.txt

prepare ``etl.cfg`` at the root folder using key and values from
``tests/test_data/db.test.cfg``

Testing
~~~~~~~

prepare db.test.cfg at the root folder using key and values from
``tests/test_data/db.test.cfg``

Run - All tests python -m unittest discover tests - Unit tests python -m
unittest discover tests.unit - Integration tests python -m unittest
discover tests.integration

For coverage report, run ``tox`` View the results in
.tox/coverage/index.html
