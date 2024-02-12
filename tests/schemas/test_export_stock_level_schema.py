import pytest
from api.schemas.export_stock_level import ExportStockLevelSchema
from api.middlewares.base_validator import ValidationError
from tests.mocks.stock_count import STOCK_LEVEL_DATA, STOCK_LEVEL_DATA_INCORRECT


class TestExportStockLevelSchema:
    """
    Test export stock level schema.
    """

    def test_export_stock_level_schema_with_valid_data_passes(self, init_db):
        """Test stock level when valid data.
        Should pass when valid stock level data is supplied
        Args:
            init_db (func): Initialises the database
        Returns:
            None
        """

        schema = ExportStockLevelSchema()
        serialized_data = schema.load_object_into_schema(STOCK_LEVEL_DATA)
        assert serialized_data['name'] == STOCK_LEVEL_DATA['name']
        assert serialized_data['stock_count'] == STOCK_LEVEL_DATA[
            'stock_count']

    def test_export_stock_level_schema_with_invalid_name_fails(self, init_db):
        """Test stock level when invalid data.
        Should fail with invalid resource data
        Args:
            init_db (func): Initialises the database
        Returns:
            None
        """

        schema = ExportStockLevelSchema()
        with pytest.raises(ValidationError):
            schema.load_object_into_schema(STOCK_LEVEL_DATA_INCORRECT)
