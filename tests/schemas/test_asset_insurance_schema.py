# Third parties
import pytest

# Middlewares
from api.middlewares.base_validator import ValidationError

# Schemas
from api.schemas.asset_insurance import AssetInsuranceSchema

# Test mocks
from tests.mocks.asset_insurance import INVALID_ASSET_INSURANCE

# Messages
from api.utilities.messages.error_messages import serialization_errors


class TestAssetInsuranceSchema:
    """ Test asset insurance schema """

    def test_asset_insurance_schema_with_invalid_data_fails(self, init_db):
        """Tests validation fails if invalid data is supplied to the schema
         Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
        """
        with pytest.raises(ValidationError) as e:
            AssetInsuranceSchema().load_object_into_schema(INVALID_ASSET_INSURANCE)
        error = e.value.error
        assert error['errors']['company'][0] == serialization_errors[
            'field_required']
        assert error['errors']['assetId'][0] == serialization_errors[
            'invalid_id_field']
        assert error['message'] == 'An error occurred'
        assert error['status'] == 'error'

    def test_asset_insurance_schema_with_valid_data_succeeds(self, init_db,
                                                     new_asset_insurance):
        """Tests validation fails if invalid data is supplied to the schema
         Args:
            init_db(SQLAlchemy): Fixture to initialize the test database actions
            new_asset_insurance (object): Fixture to create a new asset insurance
        """
        asset_insurance = new_asset_insurance.save()
        insurance_data = AssetInsuranceSchema().dump(asset_insurance).data

        assert asset_insurance.company == insurance_data['company']
        assert asset_insurance.start_date.strftime("%Y-%m-%d") == \
               insurance_data['startDate']
        assert asset_insurance.end_date.strftime("%Y-%m-%d") == \
               insurance_data['endDate']
