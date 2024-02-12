#Pytest
import pytest

# Schemas
from api.schemas.stock_count import StockCountSchema

#Errors
from api.middlewares.base_validator import ValidationError


class TestStockCountSchema:
    """Test stock count schema """

    def test_stock_count_schema_with_valid_data_passes(self, init_db,
                                                       stock_count_data):
        """Should pass when valid stock count data is supplied

        Args:
             init_db (object): Fixture used to create the database structure using the models
             stock_count_data (object): Fixture to create a new stock count
        """
        schema = StockCountSchema(
            context={
                'asset_category_id_set': set(),
                'week_list': [entry['week'] for entry in [
                    stock_count_data,
                ]]
            })
        serialized_data = schema.load_object_into_schema(stock_count_data)
        assert serialized_data['week'] == stock_count_data['week']

    def test_stock_count_schema_with_invalid_data_fails(self, init_db):
        """Should fail when invalid stock count data is supplied

        Args:
             init_db (object): Fixture used to create the database structure using the models
        """
        data = {}
        schema = StockCountSchema()
        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data)
