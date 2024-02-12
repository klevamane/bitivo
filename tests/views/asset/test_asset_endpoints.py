"""module of tests for asset endpoints
"""
# Third-party libraries
from flask import json

# Enums
from api.utilities.enums import AssetStatus

# Constants
from api.utilities.constants import CHARSET

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   filter_errors, jwt_errors)

# Models
from api.models import Asset

# Mocks
from tests.mocks.asset import (
    ASSET_NO_CUSTOM_ATTRS, ASSET_NO_CUSTOM_ATTRS_TWO, ASSET_NO_TAG,
    ASSET_NONEXISTENT_CATEGORY, ASSET_INVALID_CATEGORY_ID, ASSET_TWO,
    ASSET_THREE, ASSET_FOUR, ASSET_FIVE, ASSET_NO_CUSTOM_ATTRS_THREE,
    UNRECONCILED_ASSETS)

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1


class TestAssetEndpoints:
    """Test class for asset endpoints"""

    def test_create_asset_with_unexisting_category_fails(
            self, client, init_db, auth_header, new_user):
        """
        Tests create asset if the supplied asset_category_id exists
        in the database
         """

        new_user.save()
        ASSET_NONEXISTENT_CATEGORY['assigneeId'] = new_user.token_id
        ASSET_NONEXISTENT_CATEGORY['assigneeType'] = 'user'
        data = json.dumps(ASSET_NONEXISTENT_CATEGORY)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_create_asset_with_ASSET_INVALID_CATEGORY_ID(
            self, client, init_db, auth_header):
        """
        Tests if a supplied asset_category_id is in the right format. If it is
        not in the right format, there is no need to make database call
        """

        data = json.dumps(ASSET_INVALID_CATEGORY_ID)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "This asset category id is invalid"

    def test_create_asset_with_missing_tag(self, client, init_db, auth_header,
                                           test_asset_category, new_user):
        """
        Tests if a standard attribute is missing in the supplied asset object.
        The asset cartegory does not have custom_attributes
        """

        new_user.save()
        ASSET_NO_TAG["assetCategoryId"] = test_asset_category.id
        ASSET_NO_TAG["assigneeId"] = new_user.token_id
        ASSET_NO_TAG["assigneeType"] = 'user'
        data = json.dumps(ASSET_NO_TAG)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['attribute_required'].format('tag')

    def test_create_asset_with_valid_data(self, client, init_db, auth_header,
                                          test_asset_category, new_user):
        """
        Test create asset with valid serial and tag for a
        cartegory with no custom attributes
        """

        new_user.save()
        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS["assigneeId"] = new_user.token_id
        ASSET_NO_CUSTOM_ATTRS["assigneeType"] = 'user'
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"

    def test_create_asset_without_asset_category_id_fails(
            self, client, init_db, auth_header, test_asset_category, new_user):
        """
        Test create asset without asset category id fails

        Should return a 400 response code

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            test_asset_category: fixture to get a test asset
            new_user: fixture to get a user to test with

        Returns:
            an error message
        """

        new_user.save()
        asset_without_category_id = dict(ASSET_NO_CUSTOM_ATTRS_TWO)
        asset_without_category_id["assigneeId"] = new_user.token_id
        asset_without_category_id["assigneeType"] = 'user'
        data = json.dumps(asset_without_category_id)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "assetCategoryId key not found"

    def test_create_asset_with_invalid_status_fails(
            self, client, init_db, auth_header, asset_with_invalid_status):
        """Should return an error response when invalid status is supplied

        Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
            asset_with_invalid_status (Asset): Fixture for getting test asset data
        """
        valid_status = AssetStatus.get_all()
        data = json.dumps(asset_with_invalid_status)

        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["status"][0] == serialization_errors[
            'asset_status'].format(asset_status=str(valid_status))

    def test_create_asset_without_custom_attr(
            self, client, init_db, auth_header, test_asset_category, new_user):
        """
        Test create asset when all standard attributes are supplied and no
        custom attribute is supplied
        """

        new_user.save()
        ASSET_TWO["assetCategoryId"] = test_asset_category.id
        ASSET_TWO["assigneeId"] = new_user.token_id
        ASSET_TWO["assigneeType"] = 'user'
        data = json.dumps(ASSET_TWO)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['attribute_required'].format('waranty')

    def test_create_asset_without_required_custom_attr(
            self, client, init_db, auth_header, test_asset_category, new_user):
        """
        Test create asset when the standard atributes and optional custom
        attributes are supplied but required custome attributes are not
        supplied
        """

        new_user.save()
        ASSET_THREE["assetCategoryId"] = test_asset_category.id
        ASSET_THREE["customAttributes"] = {"length": "15"}
        ASSET_THREE["assigneeId"] = new_user.token_id
        ASSET_THREE["assigneeType"] = 'user'
        data = json.dumps(ASSET_THREE)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['attribute_required'].format('waranty')

    def test_create_asset_with_all_custom_attr(
            self, client, init_db, auth_header, test_asset_category, new_user):
        """
        Test create asset when all standard and custom attributes are
        supplied
        """

        new_user.save()
        ASSET_THREE["assetCategoryId"] = test_asset_category.id
        ASSET_THREE["assigneeId"] = new_user.token_id
        ASSET_THREE["assigneeType"] = 'user'
        ASSET_THREE["customAttributes"] = {
            "waranty": "expired",
            "length": "100"
        }
        data = json.dumps(ASSET_THREE)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "Asset successfully created"

    def test_create_asset_without_optional_custom_attr(
            self, client, init_db, auth_header, test_asset_category, new_user):
        """
        Test create asset when standard attributes and required
        custom attribute is supplied. The asset is still created even
        though an optional custom attribute is missing
        """

        new_user.save()
        ASSET_TWO["assetCategoryId"] = test_asset_category.id
        ASSET_TWO["customAttributes"] = {"waranty": "expired"}
        ASSET_TWO["assigneeId"] = new_user.token_id
        ASSET_TWO["assigneeType"] = 'user'
        data = json.dumps(ASSET_TWO)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "Asset successfully created"

    def test_create_asset_with_unrelated_custom_attr(
            self, client, init_db, auth_header, test_asset_category, new_user):
        """
        Test asset creation with an attribute that is neither a standard
        attribute nor custom attribute of the asset category
        """

        ASSET_FOUR["assetCategoryId"] = test_asset_category.id
        ASSET_FOUR["assigneeId"] = new_user.token_id
        ASSET_FOUR["assigneeType"] = 'user'
        ASSET_FOUR["customAttributes"] = {
            "color": "indigo",
            "waranty": "expired"
        }
        data = json.dumps(ASSET_FOUR)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "The attribute color is not"\
            " related to this asset category"

    def test_create_asset_with_invalid_request_type(
            self, client, init_db, auth_header_text, test_asset_category):
        """
        Test create asset when all standard and custom attributes are
        supplied
        """

        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS["customAttributes"] = {
            "waranty": "expired",
            "length": "100"
        }
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header_text, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Content-Type should be " \
                                           "application/json"

    def test_create_asset_with_duplicate_tag(self, client, init_db, new_user,
                                             auth_header, new_asset_category):
        """
        Test creation of assets with duplicate tag.
        """
        new_user.save()
        new_asset_category.save()
        ASSET_FIVE["asset_category_id"] = new_asset_category.id
        ASSET_FIVE["assignee_id"] = new_user.token_id
        ASSET_FIVE["assignee_type"] = 'user'
        asset_object = Asset(**ASSET_FIVE)
        asset_object.save()
        del ASSET_FIVE["asset_category_id"]
        ASSET_FIVE["assetCategoryId"] = new_asset_category.id
        data = json.dumps(ASSET_FIVE)
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset with the tag Kinngg Macbook"\
            " already exists"

    def test_get_assets_endpoint(self, client, init_db, auth_header):
        response = client.get(f'{api_v1_base_url}/assets', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['data'], list)
        assert response_json['meta']['currentPage'] != ''
        assert response_json['meta']['firstPage'] != ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']

        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) <= 10

    def test_get_assets_endpoint_without_pagination_succeeds(
            self, client, init_db, auth_header):
        """Should return an error response when invalid status is supplied

        Args:
            client (object): Fixture to get flask test client
            auth_header (dict): Fixture to get token
            init_db (object): Fixture for initializing test database
        """
        response = client.get(
            f'{api_v1_base_url}/assets?pagination=false', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['data'], list)
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert response_json['meta'] is None

    def test_get_assets_endpoint_pagination(self, client, init_db,
                                            auth_header):
        """
        Should return paginated assets
        """
        response = client.get(
            f'{api_v1_base_url}/assets?page=1&limit=3', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json

        assert response_json['meta']['currentPage'] != ''
        assert response_json['meta']['firstPage'] != ''
        assert response_json['meta']['nextPage'] != ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']

        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) <= 3

    def test_get_assets_endpoint_pagination_with_invalid_limit_query_string(
            self, client, init_db, auth_header):  # noqa
        """
        Should fail when requesting for paginated assets
        with wrong query strings
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1@&limit=>>', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('limit', '>>')

    def test_get_assets_endpoint_pagination_with_invalid_page_query_string(
            self, client, init_db, auth_header):  # noqa
        """
        Should fail when requesting for paginated assets
        with wrong query strings
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1@&limit=1', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('page', '1@')

    def test_get_assets_endpoint_pagination_with_exceeded_page(
            self, client, init_db, auth_header):  # noqa
        """
        Should return the last page if the page provided exceed
        the total page counts
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1000&limit=1', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        page = response_json['meta']['page']
        assert response_json['meta']['currentPage'].endswith(
            f'page={page}&limit=1')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=1')
        assert response_json['meta']['nextPage'].endswith('')
        assert response_json['meta']['previousPage'].endswith(
            f'page={page-1}&limit=1')
        assert 'totalCount' in response_json['meta']
        assert 'message' in response_json['meta']
        assert response_json['meta']['message'] == serialization_errors[
            'last_page_returned']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_get_assets_endpoint_pagination_with_exceeded_limit(
            self, client, init_db, auth_header):  # noqa
        """
        Should return the all record if the limit provided exceed
        the total record counts
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1&limit=100', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json

        assert response_json['meta']['currentPage'].endswith(
            'page=1&limit=100')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=100')
        assert response_json['meta']['nextPage'].endswith('')
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_get_assets_endpoint_pagination_with_exceeded_page_and_limit(
            self, client, init_db, auth_header):  # noqa
        """
        Should return the last page and all records if the page provided exceed
        the total page counts and if limit exceed total record count
        """

        response = client.get(
            f'{api_v1_base_url}/assets?page=1000&limit=100',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        page = response_json['meta']['page']
        assert response_json['meta']['currentPage'].endswith(
            f'page={page}&limit=100')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=100')
        assert response_json['meta']['nextPage'].endswith('')
        assert response_json['meta']['previousPage'] == ''
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_search_asset_endpoint(self, client, init_db, auth_header,
                                   new_asset_category, new_user):
        """
         Test that a list of asset is returned when a search query is provided
        """
        new_user.save()
        assets_data = [
            dict(
                tag='AND/345/EWH',
                custom_attributes={'warranty': '2017-11-09'},
                assignee_id=new_user.token_id,
                assignee_type='user'),
            dict(
                tag='AND/245/EkL',
                custom_attributes={'warranty': '2018-11-09'},
                assignee_id=new_user.token_id,
                assignee_type='user')
        ]
        assets = []

        for asset in assets_data:
            new_asset = Asset(**asset)
            new_asset_category.assets.append(new_asset)
            assets.append(new_asset)
        new_asset_category.save()

        url = f'''{api_v1_base_url}/assets/search?start=\
{(assets[0].created_at).date()}&end={(assets[1].created_at).date()}&\
warranty_start={assets[0].custom_attributes['warranty']}&\
warranty_end={assets[0].custom_attributes['warranty']}'''

        response = client.get(url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) > 0
        assert type(response_json['data']) == list

    def test_search_asset_with_invalid_column_name(self, client, auth_header):
        """
        Assert that the correct error message is returned when an invalid
        column is provided.
        """
        response = client.get(
            f'{api_v1_base_url}/assets/search?stat=2018-11-09',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_COLUMN'].format('stat')

    def test_delete_asset_succesfully(self, client, init_db, auth_header,
                                      new_asset_category, new_user):
        """
        Should return a 200 status code when an
        asset is deleted.
        """
        new_user.save()
        assets_data = dict(
            tag='AND/346/EWH',
            assignee_id=new_user.token_id,
            assignee_type='user',
            custom_attributes={'warranty': '2017-11-09'},
            created_by=new_user.token_id)
        new_asset = Asset(**assets_data)
        new_asset_category.assets.append(new_asset)
        new_asset_category.save()

        response_before = client.get(
            f'{api_v1_base_url}/assets', headers=auth_header)
        response_json_before = json.loads(response_before.data.decode(CHARSET))

        response = client.delete(
            f'{api_v1_base_url}/assets/{new_asset.id}', headers=auth_header)

        response_after = client.get(
            f'{api_v1_base_url}/assets', headers=auth_header)
        response_json_after = json.loads(response_after.data.decode(CHARSET))

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Asset')
        assert len(response_json_before['data']) > len(
            response_json_after['data'])

    def test_delete_should_fail_when_deleting_already_deleted_asset(
            self, client, init_db, auth_header, new_asset_category, new_user):
        """
        Should return a 404 status code when
        deleting an already deleted asset
        """
        new_user.save()
        assets_data = dict(
            tag='AND/348/EWH',
            assignee_id=new_user.token_id,
            assignee_type='user',
            custom_attributes={'warranty': '2017-11-09'},
            created_by=new_user.token_id)
        new_asset = Asset(**assets_data)
        new_asset_category.assets.append(new_asset)
        new_asset_category.save()

        response = client.delete(
            f'{api_v1_base_url}/assets/{new_asset.id}', headers=auth_header)
        response = client.delete(
            f'{api_v1_base_url}/assets/{new_asset.id}', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset')

    def test_delete_asset_should_fail_when_wrong_id_is_used(
            self, client, init_db, auth_header, new_asset_category):
        """
        Should return a 404(Not found) error code
        when deleting an asset with invalid id
        """
        new_asset_category.save()
        response = client.delete(
            f'{api_v1_base_url}/assets/{new_asset_category.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset')

    def test_delete_asset_should_fail_when_token_is_not_provided(
            self, client, init_db, new_asset_category):
        """
        Should return a 401 error code when
        deleting an asset without authorization
        """
        response = client.delete(
            f'{api_v1_base_url}/assets/{new_asset_category.id}')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_delete_asset_should_fail_when_invalid_id_is_provided(
            self, client, init_db, auth_header, new_asset_category):
        """
        Should return a 400 error code when
        deleting an asset without authorization
        """
        response = client.delete(
            f'{api_v1_base_url}/assets/123@#', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_create_asset_with_missing_category_id_field_in_request_fails(
            self, client, init_db, auth_header, new_user):
        """
        Tests create asset if the no assetCategoryId provided in request.

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get headers attribute value.
            new_user (object): Fixture to load new user obj
         """

        new_user.save()
        data = json.dumps({"tag": "Fred's Macbook"})
        response = client.post(
            f'{api_v1_base_url}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['key_error'].format('assetCategoryId')

    def test_get_unreconciled_assets_succeeds(self, client, init_db,
                                              new_asset_category,
                                              new_stock_count, auth_header):
        """
        Should return a 200 response code and list all unreconciled assets

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        data = response_json['data'][0]
        assert response.status_code == 200
        assert data['name'] == UNRECONCILED_ASSETS[0]['name']
        assert data['stockCount']['expectedBalance'] == UNRECONCILED_ASSETS[0][
            'stockCount']['expectedBalance']
        assert isinstance(response_json['data'], list)
        assert isinstance(data['stockCount'], dict)
        assert isinstance(data['stockCount']['actualBalance'], dict)

    def test_get_unreconciled_assets_succeeds_with_query_startDate_and_endDate(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """
             Should return a 200 response code when query unreconciled asset between
             a specify date using keyword startDate and endDate passed in url param

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?startDate=2018-01-01&endDate=2019-02-01',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        data = response_json['data'][0]
        assert response.status_code == 200
        assert data['name'] == UNRECONCILED_ASSETS[0]['name']
        assert isinstance(response_json['data'], list)

    def test_get_unreconciled_assets_succeeds_with_query_startDate_and_endDate_with_limit_and_page_param(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """
             Should return a 200 response code when query unreconciled asset between
             a specify date using keyword startDate and endDate passed in url param

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?startDate=2018-01-01&endDate=2019-02-01&limit=1&page=1',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        data = response_json['data'][0]
        assert response.status_code == 200
        assert data['name'] == UNRECONCILED_ASSETS[0]['name']
        assert isinstance(response_json['data'], list)
        assert response_json['meta']['page'] == 1
        assert response_json['meta']['totalCount'] == 2
        assert response_json['meta']['pagesCount'] == 2

    def test_get_unreconciled_assets_succeeds_with_query_startDate(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """
             Should return a 200 response code when query unreconciled asset from
             a specify date using keyword startDate passed in url param

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?startDate=2018-01-01',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        data = response_json['data'][0]
        assert response.status_code == 200
        assert data['name'] == UNRECONCILED_ASSETS[0]['name']
        assert isinstance(response_json['data'], list)

    def test_get_unreconciled_assets_succeeds_with_query_with_endDate_only(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """
             Should return a 200 response code when query unreconciled asset to a
             a specify date using keyword endDate passed in url param

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?&endDate=2019-02-01',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        data = response_json['data'][0]
        assert response.status_code == 200
        assert data['name'] == UNRECONCILED_ASSETS[0]['name']
        assert isinstance(response_json['data'], list)

    def test_get_unreconciled_assets_with_wrong_query_key_param_fails(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """
            Should return a 400 response code when a wrong keyword is passed in url
            param

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?star',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['invalid_param_key'].format( ('startDate', 'endDate', 'page', 'limit'))

    def test_get_unreconciled_assets_fail_with_wrong_date_format(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """

        Should return a 400 response code when a wrong date format is passed
        the in startDate/endDate param in url

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?&endDate=2019-23-02',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['invalid_date'].format('2019-23-02')

    def test_get_unreconciled_assets_with_blank_param_value_fails(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """

        Test when startDate param or endDate param is not assigned any date value
        i.e blank

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        # endDate without value test
        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?&endDate',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'missing_entry'].format('endDate')

        # second test startDate without value
        response_2 = client.get(
            f'{api_v1_base_url}/assets/reconciliation?&startDate',
            headers=auth_header)
        response_2_json = json.loads(response_2.data.decode(CHARSET))
        assert response_2_json["status"] == "error"
        assert response_2_json["message"] == serialization_errors[
            'missing_entry'].format('startDate')

    def test_get_unreconciled_assets_one_of_either_param_is_blank_fails(
            self, client, init_db, new_asset_category, new_stock_count,
            auth_header):
        """

        Test when one of the param is not assigned and date when both are param are
        passed in the url for query

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_asset_category(dict): fixture for new asset_category
            new_stock(dict): fixture the stock_count

        """

        # test when startDate is assigned date but the endDate hasn't been

        new_stock_count.save()
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/assets/reconciliation?&startDate=2018-01-01&endDate',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'missing_entry'].format('endDate')

        # test when startDate hasn't been assigned any value but the endDate has been assigned
        response_2 = client.get(
            f'{api_v1_base_url}/assets/reconciliation?&startDate&endDate=2019-02-01',
            headers=auth_header)
        response_2_json = json.loads(response_2.data.decode(CHARSET))
        assert response_2_json["status"] == "error"
        assert response_2_json["message"] == serialization_errors[
            'missing_entry'].format('startDate')
