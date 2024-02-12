import json

from api.schemas.stock_count import StockCountSchema
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
URL = f'{BASE_URL}/stock-count/'


class TestDeleteStockCount:
    """Tests for the delete stock-count endpoint"""

    def test_delete_the_stock_count_succeeds(self, init_db, client,
                                             save_stock_count, auth_header):
        """Deletes a stock count

        Args:
            init_db (func): Initialize test database
            client (func): Flask test client
            save_stock_count (func): Save stock count records
            auth_header (func): Authentication token

        Returns:
            None
        """
        schema = StockCountSchema()
        stock = schema.dump(save_stock_count[0])
        stock_count_id = stock[0]['id']
        new_url = URL + stock_count_id
        response = client.delete(new_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["deleted"].format(
            "Stock count")

    def test_delete_the_stock_count_with_invalid_id_fails(
            self, init_db, client, save_stock_count, auth_header):
        """Checks for invalid stock count id

        Check that delete operations should not be implemented when an
        invalid id is passed as the stock count id fails

        Args:
               init_db (func): Initialize test database
               client (func): Flask test client
               save_stock_count (func): Save stock count records
               auth_header (func): Authentication token

        Returns:
            None
        """

        new_url = URL + '-LTXlotWg1IKsIiiIIii'
        response = client.delete(new_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            "not_found"].format("Stock count")
