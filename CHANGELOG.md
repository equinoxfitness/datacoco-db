# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.10] - 2020-09-23
### Changed
    - Add dynamointeraction

## [0.1.9] - 2020-08-25
### Changed
    - Add mongointeraction

## [0.1.8] - 2020-07-07
### Changed
    - Fixed substr not found error

## [0.1.7] - 2020-03-11
### Changed
    - Fix exception handling when calling exec_sql() using stored proc queries.

## [0.1.6] - 2020-02-21
### Added
    - Add .readthedocs.yaml
    - Add contact information to Code of Conduct
    - Update Tests

## [0.1.5] - 2020-02-04
### Added
    -

## [0.1.4] - 2020-01-28
### Changed
    - Updated mssql_tools.py to add support for pyodbc
    - Various codacy fixes
    - Added deploy to test pypi step in Jenkinsfile

## [0.1.3] - 2020-01-07
### Changed
    - Mssql default port added - 1433

## [0.1.2] - 2019-12-18
### Changed
    - up version to 0.1.2 due to build error in 0.1.1

## [0.1.1] - 2019-12-18
### Changed
    - json schema added to setup.py

## [0.1.0] - 2019-12-17
### Added
    - Port datacoco3.db fix on jsonschema validation
    - Add json serialization/validation to pg_tools
    - Add sqlite_tools: SQLiteInteraction
    - Add client_id for sf api connections
    - sf_tools: upsert support
    - Retry connection attempts (3) added for sf_runner. If connection cannot be made, create new.
    - sf_tools: redis connection bug fix
    - sf_tools: session management update
    - opensource update, refactored and mock testing (does not require config)
    - fixed bug in sf_tools and added extra logging for salesforce bulk query fetch
    - sf tools to support encoding for utf-8
    - Allow mssql tools to connect to db's with slashes in host name
    - added sf upload functions in sf_tools
    - updated psycopg2 to version 2.7.7
    - Add get_description in SFInteraction
    - Add RedisInteraction
    - Updated SFInteraction to use Redis for saving/retrieving session credentials
    - Increase pytds login_timout param in mssql_tools
    - updated RDB tools to support fetch via generator to reduce memory
    - updated RDB tools to include utility functions for getting schema and checking table existence
    - Add SF Interaction
    - improve error message fetch_sql_one rdb
    - mssql sql_fetch_one fix on multiple statements
    - add test to support multiline test on mssql fetch_one

[0.1.10]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.9...0.1.10
[0.1.9]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.8...0.1.9
[0.1.8]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.7...0.1.8
[0.1.7]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.6...0.1.7
[0.1.6]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.5...0.1.6
[0.1.5]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.4...0.1.5
[0.1.4]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.3...0.1.4
[0.1.3]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.2...0.1.3
[0.1.2]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/equinoxfitness/datacoco-db/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/equinoxfitness/datacoco-db/releases/tag/0.1.0

