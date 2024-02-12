# Utilities
from api.utilities.json_parse_objects import json_parse_objects

# Mocks
from tests.mocks.requests import VALID_ATTACHMENTS, VALID_JSON_ATTACHMENTS


class TestJsonParseObjects:
    def test_json_parser_function_loads_valid_json_elements(self):
        """Tests that the parser function returns valid json elements
        on loads"""
        assert json_parse_objects(
            VALID_ATTACHMENTS, 'loads') == VALID_JSON_ATTACHMENTS

    def test_json_parser_function_dumps_valid_string_elements(self):
        """Tests that the parser function returns valid string elements
        on dumps"""
        assert json_parse_objects(
            VALID_JSON_ATTACHMENTS) == VALID_ATTACHMENTS
