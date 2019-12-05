import unittest
from unittest.mock import MagicMock

from datacoco_db.pg_tools import PGInteraction


class TestPGInteraction(unittest.TestCase):
    def test_bulk_dictionary_insert(self):
        testClass = PGInteraction(
            dbname="db_name",
            host="host",
            user="user",
            password="password",
            port="port",
            schema="public",
        )
        testClass.cur = MagicMock()
        testClass.bulk_dictionary_insert("table_name", {"key": "value"})
