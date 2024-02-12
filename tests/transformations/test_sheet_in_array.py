import pytest
import pyexcel as pe
from api.utilities.helpers.asset_transformer import sheet_in_array

class TestSheetInArray:
    def test_for_sheet_in_array(self):
        """ Test to validate that the function converts a pyexcel
            into a list and returns it
        """
        data=[['value1','value2','value3']]
        sheet= pe.Sheet(data)
        result = sheet_in_array(sheet)

        assert result == data
