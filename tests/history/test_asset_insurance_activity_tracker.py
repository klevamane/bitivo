"""
Module of tests for  asset insurance activity tracker
"""
# system imports
import json

# App config
from config import AppConfig

# models
from api.models import History

# Constant
from api.utilities.constants import CHARSET

# mock data
from tests.mocks.asset_insurance import (VALID_ASSET_INSURANCE,
                                         UPDATE_ASSET_INSURANCE_POLICY_WITH_COMPANY_ONLY)


API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetInsuranceActivityTracker:
    """Tests for asset insurance activity tracker
    """

    def test_create_asset_insurance_activity_tracker_succeed(
            self, client, init_db, auth_header, new_user, new_asset):
        """Test history is generated when new asset insurance is created

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_user (dict): fixture to create a new asset
        """
        new_user.save()

        data = json.dumps(VALID_ASSET_INSURANCE)

        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_asset.id}/insurance', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        asset_insurance_id = response_json['data']['id']
        history = History.query_().filter_by(resource_id=asset_insurance_id).first()

        assert history.resource_id == asset_insurance_id
        assert history.action == 'Add'
        assert history.activity == 'Added to Activo'
        assert history.resource_type == 'AssetInsurance'

    def test_update_asset_insurance_activity_tracker_succeed(
            self, client, init_db, auth_header, new_user, new_asset_insurance):
        """Test history is generated when asset insurance is updated

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_asset_insurance: fixture for creating an asset insurance
        """
        new_user.save()
        asset_insurance = new_asset_insurance.save()
        asset_insurance_id = asset_insurance.id
        data = json.dumps(UPDATE_ASSET_INSURANCE_POLICY_WITH_COMPANY_ONLY)
        client.patch(
            f'{API_BASE_URL_V1}/insurance/{asset_insurance_id}', headers=auth_header, data=data)

        history = History.query_().filter_by(resource_id=asset_insurance_id).first()

        assert history.resource_id == asset_insurance_id
        assert history.action == 'Edit'
        assert history.activity == 'company changed from Some Company to Asus insurance'
        assert history.resource_type == 'AssetInsurance'
