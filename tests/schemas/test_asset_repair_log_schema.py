import pytest

from api.middlewares.base_validator import ValidationError
from api.schemas.asset_repair_log import AssetRepairLogSchema
from tests.mocks.asset_repair_log import INVALID_ASSET_REPAIR_LOG_DATA


class TestAssetRepairLogSchema:
    """
    Test AssetsRepairLogSchema
    """

    def test_asset_repair_schema_with_valid_data_succeeds(
            self, init_db, new_asset_repair_log):
        """
        Test AssetRepairLogSchema with valid data

        init_db (Fixture): initialize db
        new_asset_repair_log(object): fixture to create a new asset repair log
        """
        new_asset_repair_log = new_asset_repair_log.save()
        new_asset_repair_data = AssetRepairLogSchema().dump(
            new_asset_repair_log).data

        assert new_asset_repair_log.id == new_asset_repair_data['id']
        assert new_asset_repair_log.status.value == new_asset_repair_data[
            'status']
        assert new_asset_repair_log.issue_description == new_asset_repair_data[
            'issueDescription']

    def test_asset_repair_schema_with_invalid_data_fails(self, init_db):
        """
        Test AssetRepairLogSchema with invalid data

        init_db (Fixture): initialize db
        """
        with pytest.raises(ValidationError):
            AssetRepairLogSchema().load_object_into_schema(
                INVALID_ASSET_REPAIR_LOG_DATA)
