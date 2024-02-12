"""Tests for endpoints to get users"""
from flask import json

# Mocks
from tests.mocks.user import USER_LIST

# Constants
from api.utilities.constants import CHARSET

# Error messages
from api.utilities.messages.error_messages import (
    serialization_errors, query_errors, jwt_errors, filter_errors)

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetUserDetails:
    """Test for the get user details endpoint"""

    def test_get_user_details_with_valid_id_should_succeed(
            self, client, init_db, auth_header, new_user):
        """
        Test that user details are successfully returned when a valid
        person id is provided
        """
        new_user.save()
        response = client.get(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert (response.status_code, response_json['status']) == (200,
                                                                   'success')
        user_data = response_json['data']
        assert user_data['id'] == new_user.id
        assert user_data['name'] == new_user.name
        assert user_data['email'] == new_user.email
        assert user_data['status'] == new_user.status.name
        assert user_data['role']['id'] == new_user.role.id
        assert user_data['role']['title'] == new_user.role.title
        assert user_data['role']['description'] == new_user.role.description

    def test_get_user_details_with_invalid_id_should_fail(
            self, client, init_db, auth_header, new_user):
        """
        Test that an error message is returned when an invalid person_id is
        provided
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people/-LL9kPK4vZeD9ANm%$%',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_get_user_details_with_no_token_should_fail(
            self, client, new_user):
        """
        Test that an error is returned when no token is provided
        """
        response = client.get(f'{API_V1_BASE_URL}/people/{new_user.token_id}')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_user_details_with_nonexistent_user_should_fail(
            self, client, auth_header):
        """
        Test that an error is returned when a valid but nonexistent id is
        provided
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people/-xxxxxxxxx', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('User')

    def test_get_user_with_valid_include_query_succeeds(
            self, client, init_db, auth_header, user_with_role):
        """Test successfully getting user details along with user permissions.

        Args:
            self (Instance): GetUserDetails class instance.
            client (FlaskClient): fixture to get flask test client.
            init_db (SQLAlchemy): fixture to initialize the test database.
            auth_header (dict): fixture to get token.
            user_with_role (BaseModel): fixture to create new user with role.

        Returns:
            None
        """
        new_user_with_role, role_id = user_with_role
        new_user_with_role.save()
        response = client.get(
            f'{API_V1_BASE_URL}/people/{new_user_with_role.token_id}'
            f'?include=permissions',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['data']['role']['resourceAccessLevels']
        resource_access = response_json['data']['role']['resourceAccessLevels']
        assert len(resource_access[0]['permissions']) > 0
        assert resource_access[0]['permissions'][0]['type'] == 'Add'

    def test_get_user_without_pagination_succeeds(self, client, init_db,
                                                  auth_header, user_with_role):
        """Test successfully getting user details along with user permissions.

        Args:
            self (Instance): GetUserDetails class instance.
            client (FlaskClient): fixture to get flask test client.
            init_db (SQLAlchemy): fixture to initialize the test database.
            auth_header (dict): fixture to get token.
            user_with_role (BaseModel): fixture to create new user with role.

        Returns:
            None
        """
        new_user_with_role, role_id = user_with_role
        new_user_with_role.save()
        response = client.get(
            f'{API_V1_BASE_URL}/people?pagination=false', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['meta'] is None

    def test_get_user_with_invalid_query_key_should_fail(
            self, client, init_db, auth_header, new_user):
        """Test get user details & permissions with invalid query key.

        Args:
            self (Instance): GetUserDetails class instance.
            client (FlaskClient): fixture to get flask test client.
            init_db (SQLAlchemy): fixture to initialize the test database.
            auth_header (dict): fixture to get token.
            new_user (BaseModel): fixture for creating new user with role.

        Returns:
            None
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}'
            f'?incl=permissions',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors['INVALID_COLUMN']\
            .format('incl')

    def test_get_user_with_invalid_include_query_should_fail(
            self, client, init_db, auth_header, new_user):
        """Test get user details & permissions with invalid query value.

        Args:
            self (Instance): GetUserDetails class instance.
            client (FlaskClient): fixture to get flask test client.
            init_db (SQLAlchemy): fixture to initialize the test database.
            auth_header (dict): fixture to get token.
            new_user (BaseModel): fixture for creating new user with role.

        Returns:
            None
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}'
            f'?include=xxx',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_query_strings']\
            .format('include', 'xxx')


class TestGetPeople:
    """Tests for endpoint to retrieve paginated list of users"""

    def test_search_users_with_no_token_fails(self, client, init_db):
        """
        Should return error message when an no token is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people?name=anaeze&email=andela')

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_get_users_success_without_query_string(self, client, init_db,
                                                    user_details, auth_header):
        """
        Should return default paginated users in array without query
        string applied

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        response = client.get(f'{API_V1_BASE_URL}/people', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['data'], list)

        assert response_json['meta']['firstPage'].endswith('page=1&limit=10')
        assert 'page' not in response_json['meta']['currentPage']
        assert 'limit' not in response_json['meta']['currentPage']
        assert response_json['meta']['nextPage'] == ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']
        assert len(response_json['data']) <= 10

    def test_get_users_with_pagination_succeeds(self, client, init_db,
                                                auth_header):
        """
        Should return paginated users based on pagination query parameters

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people?page=1&limit=3', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json

        assert response_json['meta']['firstPage'].endswith('page=1&limit=3')
        assert response_json['meta']['currentPage'].endswith('page=1&limit=3')
        assert response_json['meta']['nextPage'].endswith('page=2&limit=3')
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert response_json['meta']['pagesCount'] > 1
        assert response_json['meta']['totalCount'] >= 5

        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) <= 3

    def test_search_paginated_users_with_invalid_limit_query_fails(
            self, client, init_db, auth_header):  # noqa
        """
        Should fail when requesting for paginated users with wrong
        'limit' query strings

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_V1_BASE_URL}/people?page=1&limit=>>', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('limit', '>>')

    def test_get_paginated_users_with_invalid_page_query_fails(
            self, client, init_db, auth_header):  # noqa
        """
        Should fail when requesting for paginated users with invalid page query

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_V1_BASE_URL}/people?page=1@&limit=1', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('page', '1@')

    def test_get_users_pagination_with_exceeded_page_succeeds(
            self, client, init_db, auth_header):
        """
        Should return the last page if the page provided exceed
        the total page counts

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_V1_BASE_URL}/people?page=1000&limit=1', headers=auth_header)
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

    def test_get_people_endpoint_pagination_with_exceeded_limit_succeeds(
            self, client, init_db, auth_header):
        """
        Should return the all record if the limit provided exceed
        the total record counts

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_V1_BASE_URL}/people?page=1&limit=100', headers=auth_header)
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

    def test_get_paginated_people_with_exceeded_page_and_limit_succeeds(
            self, client, init_db, auth_header):
        """
        Should return the last page and all records if the page provided exceed
        the total page counts and if limit exceed total record count

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        response = client.get(
            f'{API_V1_BASE_URL}/people?page=1000&limit=100',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        page = response_json['meta']['page']
        assert response_json['meta']['currentPage'].endswith(
            f'page={page}&limit=100')
        assert response_json['meta']['firstPage'].endswith('page=1&limit=100')
        assert response_json['meta']['nextPage'] == ''
        assert response_json['meta']['previousPage'] == ''
        assert response_json['meta']['page'] == 1
        assert response_json['meta']['pagesCount'] == 1
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)


class TestSearchUsers:
    """Tests for user search/filter by querystring"""

    def test_search_users_with_invalid_column_query_fails(
            self, client, auth_header):
        """
        Should return error message when an invalid column is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
        """
        response = client.get(
            f'{API_V1_BASE_URL}/people?king=2018-11-09&name=john',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == query_errors[
            'invalid_query_non_existent_column'].format('king', 'User')

    def test_search_users_will_succeed_with_pagination(self, client, init_db,
                                                       auth_header):
        """
        Should apply pagination to valid search result

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?name=Nsofforiz&page=1&limit=1'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert response_json['meta']['totalCount'] == 2
        assert response_json['meta']['page'] == 1
        assert response_json['meta']['pagesCount'] == 2

    def test_search_users_will_return_expected_count(self, client, init_db,
                                                     auth_header):
        """
        Should return expected number of users when valid query is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?name=Nsofforized'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert response_json['meta']['totalCount'] == 2

    def test_valid_multiple_query_succeeds(self, client, init_db, auth_header):
        """
        Should find matching user(s) when multiple valid queries are provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        name = 'name=seun'
        email = 'email=seun'
        status = 'status=disabled'
        request_url = f'{API_V1_BASE_URL}/people?{name}&{email}&{status}'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert response_json['meta']['totalCount'] == 1
        assert response_json['data'][0]['name'] == USER_LIST[4]['name']

    def test_search_users_by_name_succeeds(self, client, init_db, auth_header):
        """
        Should return expected user(s) when valid search query is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?name=Anaeze Nsofforized'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) == 1
        assert isinstance(response_json['data'], list)
        assert response_json['data'][0]['name'] == USER_LIST[0]['name']

    def test_search_users_by_unexisting_name_succeeds(self, client, init_db,
                                                      auth_header):
        """
        Should return empty array when searched by `name` which does
        not exist in user table

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?name=orob*(oscata'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert not response_json['data']
        assert isinstance(response_json['data'], list)

    def test_search_users_by_email_succeeds(self, client, init_db,
                                            auth_header):
        """
        Should return expected user(s) when valid `email` query is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?email=okoro'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) == 1
        assert isinstance(response_json['data'], list)
        assert response_json['data'][0]['email'] == USER_LIST[2]['email']

    def test_search_users_by_unexisting_email_succeeds(self, client, init_db,
                                                       auth_header):
        """
        Should return empty array when searched by `email` which does
        not exist in user table

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?email=periplaneta'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert not response_json['data']
        assert isinstance(response_json['data'], list)

    def test_search_users_by_center_id_succeeds(self, client, init_db,
                                                user_details, auth_header):
        """
        Should return expected user(s) when valid `centerId` query is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            user_details(dict): fixture to get details of bulk created users
        """
        center_id = user_details['center_id']
        request_url = f'{API_V1_BASE_URL}/people?centerId={center_id}'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) == 5
        assert isinstance(response_json['data'], list)

    def test_search_users_by_unexisting_center_id_succeeds(
            self, client, init_db, auth_header):
        """
        Should return empty array when searched by `centerId` which does
        not exist in user table

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?centerId=xxxxx'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert not response_json['data']
        assert isinstance(response_json['data'], list)

    def test_search_users_by_role_id_succeeds(self, client, init_db,
                                              user_details, auth_header):
        """
        Should return expected user(s) when valid `roleId` query is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            user_details(dict): fixture to get details of bulk created users
        """
        role_id = user_details['role_id']
        request_url = f'{API_V1_BASE_URL}/people?roleId={role_id}'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) == 5
        assert isinstance(response_json['data'], list)
        assert response_json['data'][0]['role']['id'] == user_details[
            'role_id']

    def test_search_users_by_unexisting_role_id_succeeds(
            self, client, init_db, auth_header):
        """
        Should return empty array when searched by `roleId` which does
        not exist in user table

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?roleId=xxxxx'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert not response_json['data']
        assert isinstance(response_json['data'], list)

    def test_search_users_by_status_succeeds(self, client, init_db,
                                             auth_header):
        """
        Should return expected user(s) when valid `status` query is provided

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """
        request_url = f'{API_V1_BASE_URL}/people?status=disabled'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) == 3
        assert isinstance(response_json['data'], list)
        assert response_json['data'][0]['status'] == 'disabled'

    def test_search_users_by_invalid_status_fails(self, client, init_db,
                                                  auth_header):
        """
        Should fail when searching for users with invalid `status` query

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
        """

        request_url = f'{API_V1_BASE_URL}/people?status=xxxxx'
        response = client.get(request_url, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert 'meta' not in response_json
        assert response_json['status'] == 'error'
        assert response_json['message'] == query_errors[
            'invalid_query_wrong_value'].format('status', 'xxxxx')


class TestsGetSoftDeletedUsers:
    """Tests for endpoint to retrieve list of users inclusive of soft deleted users"""

    def test_get_soft_deleted_users_succeeds(
            self, client, init_db, auth_header_two, new_user_two):
        """
        Test get users inclusive of soft deleted users

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token
            new_user_two (object): Fixture to create a new user
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request client context

        """
        new_user_two.save()
        new_user_two.delete()
        get_people = client.get(f'{API_V1_BASE_URL}/people', headers=auth_header_two)

        people_data = json.loads(get_people.data.decode(CHARSET))

        response = client.get(
            f'{API_V1_BASE_URL}/people?include=deleted', headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data']

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_data) > len(people_data['data'])
