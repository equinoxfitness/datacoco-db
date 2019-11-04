# Datacoco - DB

Equinox Common Code Utility for Python 3 for DB interactions!
There are currently interaction classes for the following DBs and Apps:

+ Postgres/Redshift
+ Mssql
+ SalesForce
+ Redis


## Development

### Getting Started

It is recommended to use the steps below to set up a virtual environment for development:


```
python3 -m venv <virtual env name>
source venv/bin/activate
pip install -r requirements-dev.txt
```

prepare `etl.cfg` at the root folder using key and values from `tests/test_data/db.test.cfg`

### Testing
prepare db.test.cfg at the root folder using key and values from `tests/test_data/db.test.cfg`

Run
- All tests
    python -m unittest discover tests
- Unit tests
    python -m unittest discover tests.unit
- Integration tests
    python -m unittest discover tests.integration

For coverage report, run `tox`
View the results in .tox/coverage/index.html