"""
Module of tests for roles endpoints
"""
from flask import json

# models
from api.models import Role

# constants
from api.utilities.constants import CHARSET

# messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors,
                                                   jwt_errors, database_errors)
from api.middlewares.permission_required import Resources
# mocks
from tests.mocks.role import (
    VALID_ROLE_DATA, ROLE_DATA_WITH_EMPTY_TITLE,
    ROLE_DATA_WITH_EMPTY_DESCRIPTION, ROLE_DATA_WITH_INVALID_TITLE,
    ROLE_DATA_WITH_INVALID_DESCRIPTION, VALID_ROLE_DATA_TWO,
    VALID_UPDATE_ROLE_DATA_DUPLICATED, VALID_ROLE_WITHOUT_TITLE,
    VALID_ROLE_DATA_THREE, VALID_ROLE_DATA_TO_MUTATE,
    VALID_ROLE_DATA_TO_MUTATE_TWO, VALID_ROLE_DATA_FOUR,
    ROLE_DATA_WITH_RESOURCE_ACCESS_LEVEL, VALID_ROLE_DATA_TITLE,
    VALID_DESCRIPTION, VALID_ROLE_TITLE_DESCRIPTION_TWO,
    VALID_ROLE_TITLE_DESCRIPTION_THREE,
    ROLE_WITH_INVALID_RESOURCE_ACCESS_LEVEL)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1

VALID_ROLE_ENCODED = json.dumps(VALID_ROLE_DATA_TITLE)


class TestRoleEndpoints:
    """
    Role endpoints test
    """

    def test_get_role_endpoint(self, client, init_db, auth_header, new_roles):  # pylint: disable=W0613
        """
        Should return a 200 response code and a list of roles
        """
        for role in new_roles:
            role.save()
        response = client.get(f'{BASE_URL}/roles', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)

    def test_get_role_with_resources_query_succeeds(
            self, client, init_db, auth_header, new_resources):
        """
                Should return a 200 response code and a list of roles with resources

                Args:
                        client (FlaskClient): fixture to get flask test client
                        init_db (SQLAlchemy): fixture to initialize the test database
                        auth_header (dict): fixture to get token
            new_resources (Resource): fixture for creating resource

                Returns:
                        None
                """

        for resource in new_resources:
            resource.save()

        response = client.get(
            f'{BASE_URL}/roles?include=resources', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'resources' in response_json
        assert 'permissions' not in response_json
        assert isinstance(response_json['resources'], list)
        assert response_json['resources'][0]['name'] == Resources.STOCK_COUNT
        assert response_json['resources'][1]['name'] == Resources.ROLES
        assert response_json['resources'][2][
            'name'] == Resources.ASSET_CATEGORIES
        assert response_json['resources'][3]['name'] == Resources.HISTORY
        assert response_json['resources'][4]['name'] == Resources.SPACES
        assert response_json['resources'][5]['name'] == Resources.PEOPLE
        assert response_json['resources'][6]['name'] == Resources.REQUEST_TYPES
        assert response_json['resources'][7]['name'] == Resources.REQUESTS
        assert response_json['resources'][8]['name'] == Resources.PERMISSIONS
        assert response_json['resources'][9]['name'] == Resources.CENTERS
        assert response_json['resources'][10]['name'] == Resources.ASSETS

    def test_get_role_with_upper_case_resources_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a list of roles with resources

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        Returns:
            None
        """

        response = client.get(
            f'{BASE_URL}/roles?include=RESOURCES', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'resources' in response_json
        assert 'permissions' not in response_json
        assert isinstance(response_json['resources'], list)

    def test_get_role_with_permissions_query_succeeds(self, client, init_db,
                                                      auth_header):
        """
        Should return a 200 response code and a list of roles with permissions

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        Returns:
            None
        """

        response = client.get(
            f'{BASE_URL}/roles?include=permissions', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'resources' not in response_json
        assert 'permissions' in response_json
        assert isinstance(response_json['permissions'], list)

    def test_get_role_with_permissions_and_resources_query_succeeds(
            self, client, init_db, auth_header, new_resources):
        """
        Should return a 200 response code and a list of roles
        sided-loaded with resources and permissions

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        Returns:
            None
        """

        response = client.get(
            f'{BASE_URL}/roles?include=permissions&include=resources',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'resources' in response_json
        assert 'permissions' in response_json
        assert isinstance(response_json['permissions'], list)
        assert isinstance(response_json['resources'], list)
        assert response_json['resources'][0]['name'] == Resources.STOCK_COUNT
        assert response_json['resources'][1]['name'] == Resources.ROLES
        assert response_json['resources'][2][
            'name'] == Resources.ASSET_CATEGORIES
        assert response_json['resources'][3]['name'] == Resources.HISTORY
        assert response_json['resources'][4]['name'] == Resources.SPACES
        assert response_json['resources'][5]['name'] == Resources.PEOPLE
        assert response_json['resources'][6]['name'] == Resources.REQUEST_TYPES
        assert response_json['resources'][7]['name'] == Resources.REQUESTS
        assert response_json['resources'][8]['name'] == Resources.PERMISSIONS
        assert response_json['resources'][9]['name'] == Resources.CENTERS
        assert response_json['resources'][10]['name'] == Resources.ASSETS

    def test_get_role_with_unsupported_queries_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a success response even with unsupported queries

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token

        Returns:
            None
        """

        response = client.get(
            f'{BASE_URL}/roles?include=xpermissions&include=yresources',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'data' in response_json
        assert 'xpermissions' not in response_json
        assert 'yresources' not in response_json
        assert isinstance(response_json['data'], list)

    def test_get_role_endpoint_with_user_count(self, client, init_db,
                                               auth_header, user_with_role):
        """
        Test getting roles with users count

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            user_with_role (BaseModel): fixture for creating new user with role
        """

        new_user_with_role, role_id = user_with_role
        new_user_with_role.save()

        role = Role.query_().first()

        response = client.get(f'{BASE_URL}/roles', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'][0]['userCount'], int)
        assert response_json['data'][0]['userCount'] == role.user_count

    def test_create_role_without_title_fails(self, client, auth_header,
                                             init_db):  # pylint: disable=W0613
        """
        Test that creating a role without a title fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
        """

        role = json.dumps(VALID_ROLE_WITHOUT_TITLE)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['title'][0] == serialization_errors[
            'field_required']

    def test_create_role_without_description_fails(self, client, auth_header,
                                                   init_db):  # pylint: disable=W0613
        """
        Test that creating a role without a description fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
        """

        role = json.dumps(VALID_ROLE_DATA_TWO)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['description'][
            0] == serialization_errors['field_required']

    def test_create_role_with_resource_access_levels_succeeds(
            self, client, auth_header, init_db, new_resource, new_permission,
            new_permissions):  # pylint: disable=W0613
        """
        Test that creating a role with resource access levels succeeds

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
            new_permission (object): fixture for a new permission
            new_permissions (List): fixture with all permission objects
        """

        new_resource.save()
        new_permission.save()
        resource_id = new_resource.id
        permission_id = new_permission.id

        resource_access_levels = [{
            "resourceId": resource_id,
            "permissionIds": [permission_id]
        }]

        VALID_ROLE_DATA_TO_MUTATE[
            "resourceAccessLevels"] = resource_access_levels
        role = json.dumps(VALID_ROLE_DATA_TO_MUTATE)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["created"].format(
            "Role")
        assert len(response_json['data']['resourceAccessLevels']) == 1
        assert response_json['data']['resourceAccessLevels'][0]['resource'][
            'id'] == new_resource.id
        assert response_json['data']['resourceAccessLevels'][0]['resource'][
            'name'] == new_resource.name
        assert len(response_json['data']['resourceAccessLevels'][0]
                   ['permissions']) == 1
        assert response_json['data']['resourceAccessLevels'][0]['permissions'][
            0]['id'] == new_permission.id
        assert response_json['data']['resourceAccessLevels'][0]['permissions'][
            0]['type'] == new_permission.type

    def test_create_role_with_non_list_resource_access_levels_fails(
            self,
            client,
            auth_header,
            init_db,
    ):  # pylint: disable=W0613
        """
        Test creating a role when no resource access levels always succeeds.

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
        """

        role = json.dumps(ROLE_WITH_INVALID_RESOURCE_ACCESS_LEVEL)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['resourceAccessLevels'][
            0] == serialization_errors["invalid_resource_access_levels_list"]

    def test_create_role_without_resource_access_levels_fails(
            self,
            client,
            auth_header,
            init_db,
    ):  # pylint: disable=W0613
        """
        Test creating a role when no resource access levels always succeeds.

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
        """

        VALID_ROLE_DATA_TO_MUTATE["title"] = "Another Role"
        VALID_ROLE_DATA_TO_MUTATE.pop("resourceAccessLevels")
        role = json.dumps(VALID_ROLE_DATA_TO_MUTATE)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            "required_field"].format("resourceAccessLevels payload")

    def test_create_role_with_duplicate_permission_id_succeeds(
            self, client, auth_header, init_db, new_resource, new_permission,
            new_permissions):  # pylint: disable=W0613
        """
        Test creating a role with duplicate permission ids succeeds

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
            new_permission (object): fixture for a new permission
            new_permissions (List): fixture with all permission objects
        """

        resource_id = new_resource.id
        permission_id = new_permission.id
        # permissions sent in with same permission ids
        resource_access_levels = [{
            "resourceId":
            resource_id,
            "permissionIds": [permission_id, permission_id]
        }]

        VALID_ROLE_DATA_TO_MUTATE_TWO[
            "resourceAccessLevels"] = resource_access_levels
        role = json.dumps(VALID_ROLE_DATA_TO_MUTATE_TWO)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["created"].format(
            "Role")
        assert len(response_json['data']['resourceAccessLevels']) == 1
        assert response_json['data']['resourceAccessLevels'][0]['resource'][
            'id'] == new_resource.id
        assert response_json['data']['resourceAccessLevels'][0]['resource'][
            'name'] == new_resource.name
        assert len(response_json['data']['resourceAccessLevels'][0]
                   ['permissions']) == 1
        assert response_json['data']['resourceAccessLevels'][0]['permissions'][
            0]['id'] == new_permission.id
        assert response_json['data']['resourceAccessLevels'][0]['permissions'][
            0]['type'] == new_permission.type

    def test_create_role_with_full_access_permission_id_and_extra_id_fails(
            self, client, auth_header, init_db, new_resource, new_permission,
            new_permissions):  # pylint: disable=W0613
        """
        Test creating a role with full access permission id and an extra permission id fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
            new_permission (object): fixture for a new permission
            new_permissions (objects): fixture containing all the permission instances
        """

        resource_id = new_resource.id
        permission_id = new_permission.id
        full_access_permission_id = new_permissions[3].save().id

        # permissions sent in with same permission ids
        resource_access_levels = [{
            "resourceId":
            resource_id,
            "permissionIds": [permission_id, full_access_permission_id]
        }]

        VALID_ROLE_DATA_TO_MUTATE_TWO["title"] = "Yet another role"
        VALID_ROLE_DATA_TO_MUTATE_TWO[
            "resourceAccessLevels"] = resource_access_levels

        role = json.dumps(VALID_ROLE_DATA_TO_MUTATE_TWO)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['permissionIds'][
            0] == serialization_errors['single_permission'].format(
                "Full Access")

    def test_create_role_with_invalid_resource_access_level_type_fails(
            self, client, auth_header, init_db, new_resource, new_permission,
            new_permissions):  # pylint: disable=W0613
        """
        Test creating a role with invalid resource access levels fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
            new_permission (object): fixture for a new permission
            new_permissions (objects): fixture containing all the permission instances
        """

        # resource_access_levels of an invalid type
        resource_access_levels = {}
        VALID_ROLE_DATA_TO_MUTATE_TWO["title"] = "Yet again another role"
        VALID_ROLE_DATA_TO_MUTATE_TWO[
            "resourceAccessLevels"] = resource_access_levels

        role = json.dumps(VALID_ROLE_DATA_TO_MUTATE_TWO)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['resourceAccessLevels'][
            0] == serialization_errors["invalid_resource_access_levels_list"]

    def test_create_role_with_non_existing_resource_id_fails(
            self, client, auth_header, init_db):  # pylint: disable=W0613
        """
        Test creating a role using a non-existing resource id fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
            new_permission (object): fixture for a new permission
        """

        resource_access_levels = [{
            "resourceId": "-L456ai",
            "permissionIds": []
        }]

        VALID_ROLE_DATA_THREE["resourceAccessLevels"] = resource_access_levels

        role = json.dumps(VALID_ROLE_DATA_THREE)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['resourceId'][
            0] == serialization_errors['not_found'].format("Resource")

    def test_create_role_with_duplicate_resource_id_fails(
            self, client, auth_header, init_db, new_resource):  # pylint: disable=W0613
        """
        Test creating a role with duplicate resource id fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
        """

        resource_access_levels = [{
            "resourceId": new_resource.id,
            "permissionIds": []
        }, {
            "resourceId": new_resource.id,
            "permissionIds": []
        }]

        VALID_ROLE_DATA_THREE["resourceAccessLevels"] = resource_access_levels
        role = json.dumps(VALID_ROLE_DATA_THREE)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['1']['resourceId'][
            0] == serialization_errors['duplicate_found'].format('resource id')

    def test_create_role_with_non_existing_permission_id_fails(
            self, client, auth_header, init_db, new_resource):  # pylint: disable=W0613
        """
        Test creating a role using a non-existing permission id fails

        Args:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            init_db (object): fixture to initialize the test database
            new_resource (object): fixture for a new resource
        """

        resource_access_levels = [{
            "resourceId": new_resource.id,
            "permissionIds": ["-L456ai"]
        }]

        VALID_ROLE_DATA_FOUR["resourceAccessLevels"] = resource_access_levels
        role = json.dumps(VALID_ROLE_DATA_FOUR)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['permissionIds'][
            0] == serialization_errors["not_found"].format("Permission")

    def test_create_role_with_invalid_permission_id_fails(
            self, client, auth_header, init_db, new_resource):  # pylint: disable=W0613
        """
        Test creating a role using an invalid permission id fails

        Args:
          client (object): fixture to get flask test client
          auth_header (dict): fixture to get token
          init_db (object): fixture to initialize the test database
          new_resource (object): fixture for a new resource
        """

        resource_access_levels = [{
            "resourceId": new_resource.id,
            "permissionIds": ["-&L456ai"]
        }]

        VALID_ROLE_DATA_FOUR["resourceAccessLevels"] = resource_access_levels
        role = json.dumps(VALID_ROLE_DATA_FOUR)

        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['permissionIds'][
            0] == serialization_errors['invalid_id_field']

    def test_create_role_with_invalid_resource_id_fails(
            self, client, auth_header, init_db):  # pylint: disable=W0613
        """
        Test creating a role using an invalid resource id fails

        Args:
          client (object): fixture to get flask test client
          auth_header (dict): fixture to get token
          init_db (object): fixture to initialize the test database
        """
        resource_access_levels = [{
            "resourceId": "-&L456ai",
            "permissionIds": []
        }]

        VALID_ROLE_DATA_FOUR["resourceAccessLevels"] = resource_access_levels
        role = json.dumps(VALID_ROLE_DATA_FOUR)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['resourceId'][
            0] == serialization_errors['invalid_id_field']

    def test_create_role_fails_with_existing_data(self, client, auth_header):
        """
        Test that an error is returned when
        creating an already existing role

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """
        role = json.dumps(ROLE_DATA_WITH_RESOURCE_ACCESS_LEVEL)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'exists'].format('Role')

    def test_create_role_fails_without_token(self, client):
        """
        Test that an error is returned when trying to
        create a role without a valid token

        Parameters:
            client (object): fixture to get flask test client
        """

        role = json.dumps(VALID_ROLE_DATA)
        response = client.post(f'{BASE_URL}/roles', data=role)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_create_role_fails_with_empty_title(self, client, auth_header):
        """
        Test that an error is returned when
        creating a role with empty data

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        role = json.dumps(ROLE_DATA_WITH_EMPTY_TITLE)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['title'][0] == serialization_errors[
            'not_empty']
        assert response_json['message'] == 'An error occurred'

    def test_create_role_fails_with_empty_description(self, client,
                                                      auth_header):
        """
        Test that an error is returned when
        creating a role with empty data

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        role = json.dumps(ROLE_DATA_WITH_EMPTY_DESCRIPTION)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['description'][
            0] == serialization_errors['not_empty']
        assert response_json['message'] == 'An error occurred'

    def test_create_role_fails_with_invalid_title(self, client, auth_header):
        """
        Test that an error is returned when
        creating a role with invalid title

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        role = json.dumps(ROLE_DATA_WITH_INVALID_TITLE)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['title'][0] == serialization_errors[
            'string_characters']
        assert response_json['message'] == 'An error occurred'

    def test_create_role_fails_with_invalid_description(
            self, client, auth_header):
        """
        Test that an error is returned when
        creating a role with invalid description

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        role = json.dumps(ROLE_DATA_WITH_INVALID_DESCRIPTION)
        response = client.post(
            f'{BASE_URL}/roles', data=role, headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['description'][
            0] == serialization_errors['string_characters']
        assert response_json['message'] == 'An error occurred'

    def test_role_updates_successfully_when_only_title_supplied(
            self, init_db, client, auth_header, new_role, new_user):
        """
        Test updates when only title supplied

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_role (object): fixture with a new role
        """

        new_role.title = "Operations Director"
        new_user.save()
        new_role.save()

        response = client.patch(
            f'{BASE_URL}/roles/{new_role.id}',
            data=VALID_ROLE_ENCODED,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["updated"].format(
            "Role")
        assert isinstance(response_json['data'], dict)
        assert response_json['data']['title'] == VALID_ROLE_DATA_TWO['title']

    def test_role_updates_successfully_when_only_description_supplied(
            self, init_db, client, auth_header, new_role):
        """
        Test update works when only a description is supplied

        Parameters:
                client (object): fixture to get flask test client
                auth_header (dict): fixture to get token
                new_role (object): fixture with a new role
        """

        response = client.patch(
            f'{BASE_URL}/roles/{new_role.id}',
            data=json.dumps(VALID_DESCRIPTION),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["updated"].format(
            "Role")
        assert isinstance(response_json['data'], dict)
        assert response_json['data'][
            'description'] == VALID_ROLE_WITHOUT_TITLE['description']

    def test_role_updates_successfully_when_title_and_description_supplied(
            self, init_db, client, auth_header, new_role):
        """
        Test update works when both description and title
        supplied

        Parameters:
                client (object): fixture to get flask test client
                auth_header (dict): fixture to get token
                new_role (object): fixture with a new role
        """

        response = client.patch(
            f'{BASE_URL}/roles/{new_role.id}',
            data=json.dumps(VALID_ROLE_TITLE_DESCRIPTION_THREE),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["updated"].format(
            "Role")
        assert isinstance(response_json['data'], dict)
        assert response_json['data'][
            'description'] == VALID_ROLE_TITLE_DESCRIPTION_THREE['description']
        assert response_json['data'][
            'title'] == VALID_ROLE_TITLE_DESCRIPTION_THREE['title']

    def test_role_updates_successfully_when_same_data_provided(
            self, init_db, client, auth_header, new_role):
        """
        Test update works when the same data with same id and details is
        supplied

        Parameters:
                client (object): fixture to get flask test client
                auth_header (dict): fixture to get token
                new_role (object): fixture with a new role
        """
        response = client.patch(
            f'{BASE_URL}/roles/{new_role.id}',
            data=json.dumps(VALID_ROLE_TITLE_DESCRIPTION_TWO),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES["updated"].format(
            "Role")
        assert isinstance(response_json['data'], dict)
        assert response_json['data'][
            'description'] == VALID_ROLE_TITLE_DESCRIPTION_TWO['description']
        assert response_json['data'][
            'title'] == VALID_ROLE_TITLE_DESCRIPTION_TWO['title']

    def test_role_update_fails_when_no_token_provided(self, client, new_role):
        """
        Test end point returns a 401 when no
        token is supplied

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_role (object): fixture with to use for already existing role
        """

        response = client.patch(
            f'{BASE_URL}/roles/{new_role.id}', data=VALID_ROLE_ENCODED)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response_json['status'] == 'error'

    def test_role_update_fails_when_using_invalid_role_id(
            self, client, auth_header):
        """
        Test endpoint returns a 400 when an
        invalid role_id is supplied.
        An example of an invalid id is one
        with a # symbol in it

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
        """

        response = client.patch(
            f'{BASE_URL}/roles/@1234#5',
            data=VALID_ROLE_ENCODED,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['message'] == serialization_errors['invalid_id']
        assert response_json['status'] == 'error'

    def test_role_update_fails_for_duplicate_role(self, client, duplicate_role,
                                                  new_role, auth_header):
        """
        Test endpoint returns a 409 when
        trying to update a duplicate
        role

        Parameters:
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            duplicate_role (object): fixture to add another role to Database
        """

        # save another role to the DB
        duplicate_role.save()

        response = client.patch(
            f'{BASE_URL}/roles/{new_role.id}',
            data=json.dumps(VALID_UPDATE_ROLE_DATA_DUPLICATED),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json['message'] == serialization_errors[
            'exists'].format('Role')
        assert response_json['status'] == 'error'

    def test_soft_delete_role(self, client, init_db, new_custom_role,
                              auth_header, new_user):
        """
            Tests for soft deleting a role
        """
        new_user.save()
        new_custom_role.save()
        response = client.delete(
            f'{BASE_URL}/roles/{new_custom_role.id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Role')

    def test_delete_role_not_found(self, client, init_db, auth_header):
        """
            Tests that 404 is returned for an attempt to delete a
            non-existent role
        """
        response = client.delete(
            f'{BASE_URL}/roles/-L6YY54rfd98GTY', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Role')

    def test_delete_role_invalid_id(self, client, init_db, auth_header):
        """
        Tests that 400 is returned when id is invalid
        """
        response = client.delete(
            f'{BASE_URL}/roles/-LX%%%tghrfe5', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_delete_role_without_token(self, client, init_db):
        """
        Tests that 401 is returned when token is not provided
        """
        response = client.delete(f'{BASE_URL}/roles/-LX%%%tghrfe5')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_delete_role_with_existing_user(
            self, client, init_db, user_with_role, request_ctx,
            mock_request_obj_decoded_token, auth_header):
        """
        Tests that a role will not delete when role has existing user assigned
        """
        new_user_with_role, role_id = user_with_role
        new_user_with_role.save()  # create new user in new role
        response = client.delete(
            f'{BASE_URL}/roles/{role_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 403
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            'model_delete_children'].format('Role', 'User(s)')

    def test_delete_role_after_user_deleted(
            self, client, init_db, user_with_role, request_ctx,
            mock_request_two_obj_decoded_token, auth_header, new_user):
        """
        Test for deleting a role after existing user has been deleted
        """
        new_user.save()
        new_user_with_role, role_id = user_with_role
        new_user_with_role.save()  # create new user in new role
        new_user_with_role.delete()  # soft delete new user
        response = client.delete(
            f'{BASE_URL}/roles/{role_id}', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['deleted'].format(
            'Role')

    def test_get_soft_deleted_role_succeeds(
            self, client, init_db, new_role, duplicate_role2, request_ctx,
            mock_request_two_obj_decoded_token, auth_header, new_user):
        """
        Test get soft deleted roles
        """
        new_user.save()
        new_role.save()
        duplicate_role2.save()
        duplicate_role2.delete()

        get_roles = client.get(f'{BASE_URL}/roles', headers=auth_header)

        response = client.get(
            f'{BASE_URL}/roles?include=deleted', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        response_data = response_json['data']

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_data[0]['id'] == duplicate_role2.id

    def test_role_schema_when_resource_access_level_not_list(
            self, client, init_db, auth_header, new_permission, new_resource):
        new = {
            "title": "operations manaager op",
            "description": "reports to the operations director",
            "resourceAccessLevels": {
                "permissionIds": new_permission.id,
                "resourceId": new_resource.id
            }
        }

        response = client.post(
            f'{BASE_URL}/roles', data=json.dumps(new), headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors'] == {
            'resourceAccessLevels': ['Invalid type. Please provide an array']
        }
