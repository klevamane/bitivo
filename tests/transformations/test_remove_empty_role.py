import pytest
from api.utilities.helpers.asset_transformer import remove_empty_row

class TestRemoveEmptyRow:
    def test_for_remove_empty_row_with_content(self):
        """ Test to validate that the function returns
        row if it has content
        """
        data=['value']
        row = remove_empty_row(data)

        assert row == data

    def test_for_remove_empty_row_without_content(self):
        """ Test to validate that the function returns
        False if row is empty
        """
        data=[]
        row = remove_empty_row(data)

        assert row == False

