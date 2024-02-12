"""
Module of tests for update role endpoints
"""

# Third party
from flask import json

# Utilities
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.constants import CHARSET, MIMETYPE
from api.utilities.messages.error_messages import (database_errors, jwt_errors)

# Mock
from tests.mocks.role import (
    TEMPLATE_UPDATE_PERMISSION_DATA, VALID_ROLE_WITH_EMPTY_PERMISSION,
    ROLE_WITH_INVALID_PERMISSION, ROLE_WITH_DUPLICATE_PERMISSIONS,
    ROLE_WITH_DUPLICATE_RESOURCES, VALID_ROLE_WITH_EMPTY_OBJECT_PERMISSION)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1
URL = f"{AppConfig.API_BASE_URL_V1}/spaces"


class TestUpdatePermissionsOnRole:
    """
    Tests endpoint for updating permissions on a a given role
    """

    def test_role_updates_permissions_on_existing_resource_succeeds(
            self, client, init_db, auth_header, new_resource_access_level,
            new_permission, new_user):
        """
        Test updating permissions on a role with on existing resource succeeds

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """
        new_user.save()
        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = access_level.resource_id
        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = [new_permission.id]

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['updated'].format(
            'Role')
        assert len(response_json['data']['resourceAccessLevels']) == len(
            TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'])

    def test_role_updates_permissions_on_new_resource_succeeds(
            self, client, init_db, auth_header, new_resource, new_permission,
            new_roles):
        """
        Test updating permissions on a role with new resource succeeds

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_roles (object): fixture with a new role
            new_resource (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """

        new_permission = new_permission.save()
        resource = new_resource.save()
        roles = new_roles
        role = roles[3].save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = resource.id
        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = [new_permission.id]

        response = client.patch(
            f'{BASE_URL}/roles/{role.id}',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['updated'].format(
            'Role')
        assert len(response_json['data']['resourceAccessLevels']) == len(
            TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'])

    def test_role_updates_with_empty_permisionIds_list_succeeds(
            self, client, init_db, auth_header, new_resource_access_level,
            new_user):
        """
        Tests that a patch requests with resource access levels with empty
        permission ids are set to No Access permission

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
        """
        new_user.save()
        access_level = new_resource_access_level.save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = access_level.resource_id

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = []

        # request with no permissions in list
        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES['updated'].format(
            'Role')
        assert response_json['data']['resourceAccessLevels'][0]['permissions'][
            0]['type'] == 'No Access'

    def test_role_update_permissions_with_non_existing_role_fails(
            self, client, init_db, auth_header, new_resource_access_level,
            new_permission):
        """
        Test updating permissions with non existing role fails

        Parameters:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """

        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = access_level.resource_id
        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = [new_permission.id]

        response = client.patch(
            f'{BASE_URL}/roles/vcnbhdnmsdkjsmnskj',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            "non_existing"].format("Role")

    def test_role_update_permissions_with_invalid_resource_access_level_fails(
            self, client, init_db, auth_header, new_resource_access_level,
            new_permission):
        """
        Should fail when an invalid resource access level is provided

        Parameters:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """

        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(ROLE_WITH_INVALID_PERMISSION),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['resourceAccessLevels'][
            0] == serialization_errors['invalid_resource_access_levels']

    def test_role_update_permissions_with_duplicate_resource_fails(
            self, client, init_db, auth_header, new_resource_access_level,
            new_permission):
        """
        Should fail when an duplicate resource ids are provided

        Parameters:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """

        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()
        ROLE_WITH_DUPLICATE_RESOURCES['resourceAccessLevels'][0][
            'permissionIds'] = [new_permission.id]

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(ROLE_WITH_DUPLICATE_RESOURCES),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['1']['resourceId'][
            0] == serialization_errors['duplicate_found'].format('resource id')

    def test_role_update_permissions_with_full_access_and_other_permissions_fails(
            self, client, init_db, auth_header, new_resource_access_level,
            new_permission, new_permissions):
        """
        Should fail when there is full access id with another permission id

        Parameters:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
            new_permissions (List): fixture with all permission objects
        """

        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()
        full_access = new_permissions[3].save(
        )  # get the full access permission from the fixture
        role_with_full_access = VALID_ROLE_WITH_EMPTY_OBJECT_PERMISSION
        role_with_full_access['resourceAccessLevels'][0]['permissionIds'] = [
            full_access.id, new_permission.id
        ]

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(role_with_full_access),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['0']['permissionIds'][
            0] == serialization_errors['single_permission'].format(
                'Full Access')

    def test_role_update_permissions_with_non_existing_permission_fails(
            self, client, init_db, auth_header, new_resource_access_level):
        """
        Test updating permissions with non existing permission fails

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
        """

        access_level = new_resource_access_level.save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = access_level.resource_id
        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = ['hgdsytasdhvas']

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'

    def test_role_update_permissions_with_non_existing_resource_fails(
            self, client, init_db, auth_header, new_resource_access_level,
            new_permission):
        """
        Test updating permissions with non existing resource fails

        Parameters:
            init_db(SQLAlchemy): fixture to initialize the test database
            client (object): fixture to get flask test client
            auth_header (dict): fixture to get token
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """

        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = 'tadgfayuaty'
        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = [new_permission.id]

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'

    def test_role_update_permissions_with_invalid_token_fails(
            self, client, init_db, new_resource_access_level, new_permission):
        """
        Should return a 401 error response when token is not provided
        or invalid

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
        """
        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()

        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'resourceId'] = access_level.resource_id
        TEMPLATE_UPDATE_PERMISSION_DATA['resourceAccessLevels'][0][
            'permissionIds'] = [new_permission.id]

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(TEMPLATE_UPDATE_PERMISSION_DATA),
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_role_update_permissions_with_empty_resource_access_leves_fails(
            self, client, init_db, new_resource_access_level, new_permission,
            auth_header):
        """
        Should return a 400 error response when resource access levels is empty

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_resource_access_level (object): fixture with a new role
            new_permission (object): fixture with a new permission
            auth_header (dict): fixture to get token
        """
        new_permission = new_permission.save()
        access_level = new_resource_access_level.save()

        response = client.patch(
            f'{BASE_URL}/roles/{access_level.role_id}',
            data=json.dumps(VALID_ROLE_WITH_EMPTY_PERMISSION),
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['resourceAccessLevels'][
            0] == serialization_errors['not_empty']
