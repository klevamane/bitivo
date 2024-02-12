"""
Module of tests for permission endpoints
"""
# system imports
import json

# models
from api.models import History, Asset

# mocks
from tests.mocks.history import histories
from tests.mocks.asset import ASSET_NO_CUSTOM_ATTRS

# Constants
from api.utilities.constants import CHARSET, MIMETYPE

# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES, HISTORY_MESSAGES
from api.utilities.messages.error_messages import jwt_errors, query_errors

# App config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestHistoryEndpoints:
    """Tests for history endpoints
    """

    def test_get_history_valid_request_should_succeed(self, client, init_db,
                                                      auth_header, new_user):
        """Should return a 200 status code and history data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """
        new_user.save()
        History.bulk_create(histories)

        response = client.get(f'{BASE_URL}/history', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) >= 4

    def test_get_history_with_deleted_params_succeeds(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token,
            auth_header, new_user):
        """Should return a 200 status code and history data

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """
        new_user.save()
        History.bulk_create(histories)
        history_ = History.query_().first()
        history_.delete()

        response = client.get(
            f'{BASE_URL}/history?include=deleted', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) >= 4
        for history in response_json['data']:
            assert 'deleted' in history.keys()
            assert not history['deleted'] or history['deleted']
            assert history['actor']['name'] == history_.actor.name
            assert history['actor']['tokenId'] == history_.actor.token_id

    def test_get_history_of_created_asset_should_succeed(
            self, client, init_db, auth_header, new_user, test_asset_category):
        """Test history is generated when new asset is created

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_spaces (BaseModel): fixture for creating a new spaces
            test_asset_category (BaseModel): fixture for creating a asset category
        """
        new_user.save()
        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS["assigneeId"] = new_user.token_id
        ASSET_NO_CUSTOM_ATTRS["assigneeType"] = 'user'
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)

        asset_response = client.post(
            f'{BASE_URL}/assets', headers=auth_header, data=data)
        asset_id = json.loads(
            asset_response.data.decode(CHARSET))['data']['id']

        history = History.query_().filter_by(resource_id=asset_id).first()

        assert history.resource_id == asset_id

        response = client.get(
            f'{BASE_URL}/history?resourceId={asset_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert isinstance(response_json['data'], list)
        assert response_json['data'][0]['activity'] == \
            HISTORY_MESSAGES['added_resource']

    def test_get_history_with_invalid_resource_query_fail(
            self, client, init_db, auth_header):
        """Test get history for single resource with invalid

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        Query Example:
            /?resourceIds={{resourceId}}&resourceTypes={{resourceType}}
        """
        response = client.get(
            f'{BASE_URL}/history?resourceIds=-LID&resourceTypes=asset',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == \
            query_errors['invalid_query_non_existent_column']\
            .format('resource_ids', 'History')

    def test_get_history_with_edit_on_asset_should_succeed(
            self, client, init_db, auth_header_two, new_spaces):
        """Test get history for single resource with invalid

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token
            new_spaces (fixture): fixture to create new spaces

        """

        asset = Asset.query_().first()
        new_space = new_spaces.get('spaces')[0].save()
        ac_key = asset.asset_category.attributes.first()._key

        data = json.dumps(
            dict(
                tag='AND/TMZ/001',
                assigneeType='space',
                assigneeId=new_space.id,
                centerId=new_space.center_id,
                customAttributes={ac_key: "test"}))

        client.patch(
            f'{BASE_URL}/assets/{asset.id}', headers=auth_header_two, data=data)

        response = client.get(
            f'{BASE_URL}/history?resourceId={asset.id}', headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert json.loads(data)['tag'] in response_json['data'][0]['activity']

    def test_get_history_with_reassigne_asset_should_succeed(
            self, client, init_db, auth_header, new_spaces):
        """Test get history for single resource with invalid

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_spaces (fixture): fixture to create new spaces

        """

        asset = Asset.query_().first()

        space = new_spaces.get('spaces')[1].save()

        data = json.dumps(
            dict(
                assigneeType='space',
                assigneeId=space.id,
                centerId=space.center_id))

        client.patch(
            f'{BASE_URL}/assets/{asset.id}', headers=auth_header, data=data)

        response = client.get(
            f'{BASE_URL}/history?resourceId={asset.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert space.name in response_json['data'][0]['activity']

    def test_get_history_with_edit_asset_assignee_should_succeed(
            self, client, init_db, auth_header, new_user, new_spaces):
        """Test get history for single resource with invalid

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_spaces (fixture): fixture to create new spaces

        """

        asset = Asset.query_().first()
        new_user.save()
        new_spaces.get('spaces')[0].save()

        data = json.dumps(
            dict(assigneeType='user', assigneeId=new_user.token_id))

        client.patch(
            f'{BASE_URL}/assets/{asset.id}', headers=auth_header, data=data)

        response = client.get(
            f'{BASE_URL}/history?resourceId={asset.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert new_user.name in response_json['data'][0]['activity']

    def test_get_history_with_invalid_token_fails(self, client, init_db):
        """Should return an 401 status code if the provided token is not valid

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_permissions(BaseModel): fixture for creating a permissions
        """

        response = client.get(
            f'{BASE_URL}/history',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_history_with_no_token_fails(self, client, init_db):
        """Should return an 401 status code if a token is not provided

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.get(f'{BASE_URL}/history')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_history_with_delete_on_asset_should_succeed(
            self, client, init_db, auth_header):
        """Test get history for single resource with invalid

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """

        asset = Asset.query_().first()

        client.delete(f'{BASE_URL}/assets/{asset.id}', headers=auth_header)

        response = client.get(
            f'{BASE_URL}/history?resourceId={asset.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('History')
        assert HISTORY_MESSAGES['removed_resource'] in\
            response_json['data'][0]['activity']
