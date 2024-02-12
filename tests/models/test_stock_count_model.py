# Pytest
import pytest

# Models
from api.models import StockCount


class TestStockCountModel:
    """Test stock count model """

    def test_new_stock_count(self, init_db, new_stock_count):
        """Should create and return a stock count

        Args:
            init_db (object): Fixture used to create the database structure using the models
            new_stock_count (object): Fixture to create a new stock count
        """
        stock_count = new_stock_count
        assert stock_count == new_stock_count.save()

    def test_query(self):
        """Should return the count of available stock counts """
        assert StockCount.query_().count() == 1

    def test_update_succeeds(
            self,
            new_stock_count,
            request_ctx,
            mock_request_two_obj_decoded_token,
    ):
        """Should update stock count

        Args:
            new_stock_count (object): a fixture to update stock count
        """
        new_stock_count.update_(count=60)
        assert new_stock_count.count == 60

    def test_stock_count_string_representation(self, new_stock_count):
        """Should compute the official string representation of stock count

        Args:
            new_stock_count (object): a fixture to update stock count
        """
        assert repr(
            new_stock_count
        ) == '<StockCount asset_category_id:{} count:{} week:{} >'.format(
            new_stock_count.asset_category_id, new_stock_count.count,
            new_stock_count.week)

    def test_delete(self, new_stock_count, request_ctx,
                    mock_request_two_obj_decoded_token):
        """Should remove a stock count when deleted

        Args:
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request object
            new_stock_count (object): Fixture to create a new stock count
        """
        new_stock_count.delete()
        assert StockCount.get(new_stock_count.id) is None
