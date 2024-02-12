"""
Module of tests for space endpoints
"""
from flask import json

# messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors, filter_errors)

# mocks
from tests.mocks.space import create_space_data

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1
URL = f"{AppConfig.API_BASE_URL_V1}/spaces"


class TestSpaceEndpoints:
    """
    Tests for space endpoints
    """

    def test_add_space_with_valid_request_succeeds(
            self, client, init_db, auth_header_two, new_space_types, new_spaces):
        """
        Should return a 201 status code and space data if
        authentication successful

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces

        Returns:
            None
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="First Floor",
                centerId=centers[0].id,
                spaceTypeId=space_types[1].id,
                parentId=spaces[0].id))

        response = client.post(URL, headers=auth_header_two, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'added_to_center'].format('First Floor', centers[0].name)
        assert response_json['data']["id"] != ""
        assert response_json['data']["name"] == "First Floor"
        assert response_json['data']["centerId"] == centers[0].id
        assert response_json['data']["parentId"] == spaces[0].id
        assert response_json['data']['spaceType']['id'] == space_types[1].id

    def test_add_space_with_invalid_ids_fails(self, client, init_db,
                                              auth_header):
        """
        Should return a 400 status code if the ids provided have invalid
        syntax

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """

        invalid_ids = ['', 'Ca^a4#527*bba', '-LLctsJpwb697X_@t5ji']

        data = json.dumps(
            create_space_data(
                name="First Floor",
                centerId=invalid_ids[0],
                spaceTypeId=invalid_ids[1],
                parentId=invalid_ids[2]))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['centerId'][0] == \
            serialization_errors['invalid_id_field']
        assert response_json['errors']['spaceTypeId'][0] == \
            serialization_errors['invalid_id_field']
        assert response_json['errors']['parentId'][0] == \
            serialization_errors['invalid_id_field']

    def test_add_space_with_incomplete_data_fails(
            self, client, init_db, auth_header, new_space_types):
        """
        Should return a 400 status code and error message if required
        fields are not provided

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
        """

        space_types = new_space_types

        data = json.dumps({
            "name": "Second Floor",
            "parentId": space_types[0].id
        })

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['centerId'][0] == \
            serialization_errors['field_required']
        assert response_json['errors']['spaceTypeId'][0] == \
            serialization_errors['field_required']

    def test_add_space_with_existing_name_and_same_center_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 409 status code and error message if space already
        exist in the same center

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Left Wing",
                centerId=centers[0].id,
                spaceTypeId=space_types[2].id,
                parentId=spaces[1].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format('Space')

    def test_add_space_with_existing_name_but_diff_center_succeeds(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 201 status code and space data if request data is valid
        and if name already exists but on a different center

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Fourth Floor",
                centerId=centers[1].id,
                spaceTypeId=space_types[1].id,
                parentId=spaces[4].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'added_to_center'].format('Fourth Floor', centers[1].name)
        assert response_json['data']["id"] != ""
        assert response_json['data']["name"] == "Fourth Floor"
        assert response_json['data']["centerId"] == centers[1].id
        assert response_json['data']["parentId"] == spaces[4].id

    def test_add_space_with_non_existent_center_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 404 status code and error message if specified
        center cannot be found

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId="non_existent_center_id",
                spaceTypeId=space_types[2].id,
                parentId=spaces[1].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Center')

    def test_add_space_with_non_existent_parent_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 404 status code and error message if specified
        parent space cannot be found

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId=centers[0].id,
                spaceTypeId=space_types[2].id,
                parentId="non_existent_parent_id"))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Parent space')

    def test_add_space_with_non_existent_space_type_fails(
            self, client, init_db, auth_header, new_spaces):
        """
        Should return a 404 status code and error message if specified
        space type cannot be found

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId=centers[0].id,
                spaceTypeId="non_existent_space_type_id",
                parentId=spaces[1].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Space type')

    def test_add_space_with_wrong_parent_type_fails_1(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 400 status code and error message if specified
        parent space is incompatible with the space being created

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId=centers[0].id,
                spaceTypeId=space_types[2].id,
                parentId=spaces[2].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'cannot_have_parent_type'].format('wing')

    def test_add_space_with_wrong_parent_type_fails_2(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 400 status code and error message if specified
        parent space is incompatible with the space being created

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId=centers[0].id,
                spaceTypeId=space_types[3].id,
                parentId=spaces[0].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'cannot_have_parent_type'].format('building')

    def test_add_space_with_parent_from_another_center_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 400 status code and error message if specified
        parent space is from another center

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Second Floor",
                centerId=centers[0].id,
                spaceTypeId=space_types[1].id,
                parentId=spaces[4].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'centers_not_match']

    def test_add_space_with_unexpected_parent_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 400 status code and error message if a
        parent space is provided for a space that doesn't need it

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Skynet Building",
                centerId=centers[0].id,
                spaceTypeId=space_types[0].id,
                parentId=spaces[1].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'cannot_have_parent_space']

    def test_add_space_with_orphan_space_without_parent_succeeds(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 201 status code and space data if
        authentication successful

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Fun Tower",
                centerId=centers[0].id,
                spaceTypeId=space_types[0].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'added_to_center'].format('Fun Tower', centers[0].name)
        assert response_json['data']["id"] != ""
        assert response_json['data']["name"] == "Fun Tower"
        assert response_json['data']["centerId"] == centers[0].id
        assert response_json['data']['spaceType']['id'] == space_types[0].id

    def test_add_space_with_expected_parent_missing_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 400 status code and error message if parent space
        is not provided for a space that needs it

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Second Floor",
                centerId=centers[0].id,
                spaceTypeId=space_types[1].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'must_have_parent_space']

    def test_add_space_with_no_provided_token_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """
        Should return a 409 status code and error message if space already
        exist in the same center

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId=centers[0].id,
                spaceTypeId=space_types[2].id,
                parentId=spaces[1].id))

        response = client.post(URL, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_add_space_with_invalid_token_fails(self, client, init_db,
                                                new_space_types, new_spaces):
        """
        Should return a 409 status code and error message if space already
        exist in the same center

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_space_types (BaseModel): fixture for creating a space types
            new_spaces (BaseModel): fixture for creating a spaces
        """

        centers = new_spaces['centers']
        spaces = new_spaces['spaces']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Right Wing",
                centerId=centers[0].id,
                spaceTypeId=space_types[2].id,
                parentId=spaces[1].id))

        response = client.post(
            URL,
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            },
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_all_spaces_succeeds(self, client, init_db, auth_header):
        """
        Test that all spaces are returned when a request is made to the
        '/spaces' url

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """

        expected_space_fields = [
            "centerId", "name", "parentId", "spaceType", "childrenCount", "id"
        ]

        response = client.get(URL, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        data = response_json['data']
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Spaces')
        assert isinstance(response_json['spaceTypes'], list)
        assert isinstance(data, dict)
        assert 'spaces' in data
        assert 'wings' in data
        assert 'floors' in data
        assert 'buildings' in data
        assert isinstance(data['buildings'], list)
        assert isinstance(data['wings'], list)
        assert isinstance(data['floors'], list)
        assert isinstance(data['spaces'], list)
        assert len(expected_space_fields) == len(data['buildings'][0].keys())
        assert set(expected_space_fields) == set(data['buildings'][0].keys())

    def test_get_all_spaces_with_no_provided_token_fails(
            self, client, init_db):
        """
        Test that a 401 is returned when a request is made to the
        '/spaces' url with no token

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
        """

        response = client.get(URL)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_all_spaces_with_invalid_token_fails(self, client, init_db):
        """
        Test that a 401 is returned when a request is made to the
        '/spaces' url with invalid token

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
        """

        response = client.get(
            URL,
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_get_all_spaces_under_a_center_succeeds(self, client, init_db,
                                                    auth_header, new_spaces):
        """Test get spaces in a center

        Should return all spaces in a center are returned when a 
        request is made to the '/spaces?centerId=<centyer_id>' url

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_spaces (dict): collection of spaces and centers
        """

        centers = new_spaces['centers']
        response = client.get(
            f'{URL}?centerId={centers[0].id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        data = response_json['data']

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Spaces')
        assert isinstance(response_json['spaceTypes'], list)
        assert isinstance(response_json['data'], dict)
        assert data['buildings'][0]['centerId'] == centers[0].id
        assert data['floors'][0]['centerId'] == centers[0].id

    def test_get_all_spaces_under_a_center_with_invalid_query_fails(
            self, client, init_db, auth_header):
        """
        Test that an error is returned when a request is made to get the
        spaces under a center with invalid query

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """

        response = client.get(f'{URL}?center=xxx', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_COLUMN'].format('center')

    def test_get_all_spaces_under_an_invalid_center_fails(
            self, client, init_db, auth_header):
        """
        Test that an error is returned when a request is made to get the
        spaces under a center with invalid center id

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """

        response = client.get(f'{URL}?centerId=xxx', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'Center not found'

    def test_get_all_spaces_with_invalid_query_key_fails(
            self, client, init_db, auth_header):
        """
        Test that an error is returned when a request is made to get all
        spaces with invalid query

        Parameters:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        """

        response = client.get(f'{URL}?inclu=children', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_COLUMN'].format('inclu')

    def test_get_all_spaces_under_a_building_succeeds(self, client, init_db,
                                                      auth_header, new_spaces):
        """Test get spaces in a building
         Should return all spaces in a building are returned when a 
        request is made to the '/spaces?buildingId=<building_id>' url
         Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_spaces (dict): collection of spaces
        """

        buildings = new_spaces['spaces']
        response = client.get(
            f'{URL}?buildingId={buildings[0].id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        data = response_json['data']
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['fetched'].format(
            'Spaces')
        assert isinstance(response_json['spaceTypes'], list)
        assert isinstance(response_json['data'], dict)
        assert data['buildings'][0]['id'] == buildings[0].id
        assert data['floors'][0]['parentId'] == buildings[0].id


class TestGetSingleSpace:
    """
    Tests for getting a single space
    """

    def test_get_space_with_valid_id_should_succeed(
            self, client, init_db, auth_header, new_spaces, new_space_types):
        """
        Test that space details are successfully returned
        """
        space = new_spaces['spaces'][0]
        space_type = new_space_types[0]
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/{space.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        space_data = response_json['data']
        space_type_data = space_data['spaceType']
        assert space_data['id'] == space.id
        assert space_data['name'] == space.name
        assert space_data['parentId'] == space.parent_id
        assert space_type_data['id'] == space_type.id
        assert space_type_data['type'] == space_type.type
        assert space_type_data['color'] == space_type.color
        assert 'children' not in response_json['data']
        assert response_json['status'] == 'success'

    def test_get_space_with_invalid_id_should_fail(self, client, auth_header):
        """
        Test that an error message is returned when the space_id is invalid
        """
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/-LL9k%^$fdJT3IHl8&*!',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_get_space_with_nonexistent_id_should_fail(self, client,
                                                       auth_header):
        """
        Test that an error message is returned when the space is not found
        """
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/-LL9kPKSfdJT3IHl8ABC',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Space')

    def test_get_space_with_no_token_should_fail(self, client):
        """
        Test that an error message is returned when no token is provided
        """
        response = client.get(f'{API_V1_BASE_URL}/spaces/-LL9kPKSfdJT3IHl8ABC')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_space_with_invalid_query_param_should_fail(
            self, client, auth_header):
        """
        Test that an error message is returned when the include
        query parameter is not 'children'
        """
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/-LL9kPKSfdJT3IHl8ABC?include=child',
            headers=auth_header)

        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['status'] == 'error'
        assert json_response['message'] == serialization_errors[
            'invalid_query']

    def test_get_space_with_empty_include_query_should_fail(
            self, client, auth_header):
        """
        Test that an error message is returned when the include query
        value is empty
        """
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/-LL9kPKSfdJT3IHl8ABC?include=',
            headers=auth_header)

        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['status'] == 'error'
        assert json_response['message'] == serialization_errors[
            'invalid_query']

    def test_get_space_with_incomplete_query_should_fail(
            self, client, auth_header):
        """
        Test that an error message is returned when the include query string
        is not assigned a value
        """
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/-LL9kPKSfdJT3IHl8ABC?include',
            headers=auth_header)

        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['status'] == 'error'
        assert json_response['message'] == serialization_errors[
            'invalid_query']

    def test_get_space_with_invalid_query_field_should_fail(
            self, client, auth_header):
        """
        Test that an error message is returned when the query string
        does not contain a valid field
        """
        response = client.get(
            f'{API_V1_BASE_URL}/spaces/-LL9kT3IHl8ABC?name=anaeze&sex=male',
            headers=auth_header)

        json_response = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert json_response['status'] == 'error'
        assert json_response['message'] == serialization_errors[
            'invalid_query']

    def test_add_duplicate_space_name_to_the_same_center_fails(
            self, client, init_db, auth_header, new_space_types, new_spaces):
        """Should return a 409 status code and an error message if the space already exists

        Args:
            client (FlaskClient): Fixture to get flask test client.
            init_db (SQLAlchemy): Fixture to initialize the test database.
            auth_header (dict): Fixture to get token.
            new_space_types (BaseModel): Fixture for creating a space types.
            new_spaces (BaseModel): Fixture for creating a spaces.
        """

        centers = new_spaces['centers']
        space_types = new_space_types

        data = json.dumps(
            create_space_data(
                name="Fun towEr",
                centerId=centers[0].id,
                spaceTypeId=space_types[0].id))

        response = client.post(URL, headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format('Space')

    def test_get_soft_deleted_spaces_succeeds(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token,
            auth_header_two, new_user, new_space_two):
        """
        Test get users inclusive of soft deleted users

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token
            new_user (object): Fixture to create a new user
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context

        """
        new_space_two.save()
        new_user.save()
        new_space_two.delete()

        get_spaces = client.get(
            f'{API_V1_BASE_URL}/spaces', headers=auth_header_two)

        people_data = json.loads(get_spaces.data.decode(CHARSET))

        response = client.get(
            f'{API_V1_BASE_URL}/spaces?include=deleted', headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        assert response_json['status'] == 'success'
