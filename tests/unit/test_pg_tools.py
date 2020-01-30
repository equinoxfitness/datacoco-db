import unittest
from unittest.mock import MagicMock
import json
from datacoco_db.pg_tools import PGInteraction


class TestPGInteraction(unittest.TestCase):
    def test_bulk_dictionary_insert(self):
        testClass = PGInteraction(  # nosec
            dbname="db_name",
            host="host",
            user="user",
            password="password",
            port="port",
            schema="public",
        )
        testClass.cur = MagicMock()
        testClass.bulk_dictionary_insert("table_name", {"key": "value"})

    def test_validate_schema(self):
        testClass = PGInteraction(  # nosec
            dbname="db_name",
            host="host",
            user="user",
            password="password",
            port="port",
            schema="public",
        )
        schema = {
            "type": "object",
            "properties": {
                "price": {"type": "number"},
                "name": {"type": "string"},
            },
        }

        testClass.cur = MagicMock()
        testClass.validate_json_scheme(
            json.dumps({"name": "Eggs", "price": 34.99}), schema
        )


if __name__ == "__main__":
    unittest.main()
