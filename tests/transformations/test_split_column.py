import pytest
from api.utilities.helpers.asset_transformer import split_column

class TestSplitColumn:
    def test_for_split_column_succeed(self):
        """ Test to validate that the function returns
        the required columns
        """
        data = [['value1','value2','value3']]
        result = split_column(data, 1)

        assert result == [['value2','value3']]
