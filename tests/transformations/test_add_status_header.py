import pytest
from api.utilities.helpers.asset_transformer import add_status_header


class TestAddStatusAndHeader:

    def test_for_status_and_header(self):
        """ Test to validate that the function converts a pyexcel
            into a list and returns it
        """
        header = ['value1', 'value2', 'value3', 'value4', 'Status']
        data = [['value1', 'value2', 'value3', 'value4'],
                ['value1', 'value2', 'value3', 'value4']]
        expected_result = [['value1', 'value2', 'value3', 'value4', 'Status'],
                           ['value1', 'value2', 'value3', 'value4', 'Assigned']]
        status_mapper = {}
        result = add_status_header(data, status_mapper, header)

        assert result == expected_result
