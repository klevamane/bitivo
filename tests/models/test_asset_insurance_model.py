""" Tests for request model """

from api.models import AssetInsurance


class TestAssetInsuranceModel:
    """ Test asset insurance model"""

    def test_new_asset_insurance(self, init_db, new_asset_insurance):
        """Should create a new asset insurance

        Args:
            init_db (object): Fixture to initialize the test database operations.
            new_asset_insurance (object): Fixture to create a new asset insurance
        """
        assert new_asset_insurance == new_asset_insurance.save()

    def test_update_asset_insurance(self, new_asset_insurance, new_user,
                                    request_ctx,
                                    mock_request_two_obj_decoded_token):
        """Should update an asset insurance

        Args:
            new_asset_insurance (object): Fixture to create a new asset insurance
        """
        new_user.save()
        new_asset_insurance.save()
        new_asset_insurance.update_(company='The Chainsmokers')
        assert AssetInsurance.get(
            new_asset_insurance.id).company == 'The Chainsmokers'

    def test_get(self, new_asset_insurance):
        """Should retrieve a asset insurance

        Args:
            new_asset_insurance (object): Fixture to create a new asset insurance
        """
        assert AssetInsurance.get(
            new_asset_insurance.id) == new_asset_insurance

    def test_query(self, new_asset_insurance):
        """Should get a list of available asset insurances

        Args:
            new_asset_insurance (object): Fixture to create a new asset insurance
        """
        asset_insurance_query = new_asset_insurance.query_()
        assert isinstance(asset_insurance_query.all(), list)

    def test_delete(self, new_asset_insurance, request_ctx,
                    mock_request_two_obj_decoded_token, new_user):
        """Should delete a asset insurance

        Args:
            new_asset_insurance (object): Fixture to create a new asset insurance
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context
        """
        new_user.save()
        new_asset_insurance.delete()
        assert AssetInsurance.get(new_asset_insurance.id) is None

    def test_request_model_string_representation(self, new_asset_insurance):
        """ Should compute the string representation of a asset insurance

        Args:
            new_asset_insurance (object): Fixture to create a new asset insuranc
        """
        company = new_asset_insurance.company
        start_date = new_asset_insurance.start_date.strftime("%Y-%m-%d")
        end_date = new_asset_insurance.end_date.strftime("%Y-%m-%d")
        assert repr(new_asset_insurance) == \
            f'<AssetInsurance {company} ({start_date} - {end_date})>'
