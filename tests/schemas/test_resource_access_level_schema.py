# Third party
import pytest

# Schemas
from api.schemas.resource_access_level import ResourceAccessLevelSchema
from api.schemas.role import RoleSchema

# Middlewares
from api.middlewares.base_validator import ValidationError


class TestResourcesAccessLevelSchema:
    """
    Test resources access level schema
    """

    def test_resource_access_level_schema_with_valid_data_passes(
            self, init_db, new_resource_access_level):
        """
        Should pass when valid resources access level data is supplied
        """
        data = {
            'role_id': new_resource_access_level.role_id,
            'resource_id': new_resource_access_level.resource_id
        }
        schema = ResourceAccessLevelSchema()
        serialized_data = schema.load_object_into_schema(data, partial=True)
        assert serialized_data['role_id'] == data['role_id']
        assert serialized_data['resource_id'] == data['resource_id']

    def test_resource_access_level_schema_with_duplicate_data_fails(
            self, init_db, new_resource_access_level):
        """
        Should fail and raise validation error when duplicate resource access level data is supplied
        """
        data = {
            'role_id': new_resource_access_level.role_id,
            'resource_id': new_resource_access_level.resource_id
        }

        new_resource_access_level.save()
        schema = ResourceAccessLevelSchema()
        with pytest.raises(ValidationError) as excInfo:
            schema.load_object_into_schema(data)
        assert excInfo.type == ValidationError

    def test_resource_access_level_schema_with_invalid_data_fails(
            self, init_db):
        """
        Should fail when invalid resource access level data is passed
        """
        data = {'role_id': 1}
        schema = ResourceAccessLevelSchema()
        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data)


class TestPermissionsSchema:
    """
    Test Permissions Schema
    """

    def test_permissions_schema_with_valid_data_succeeds(
            self, new_resource_access_level):
        """
        Should pass when valid permission data is supplied

        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """

        data = {
            "resourceId": new_resource_access_level.resource_id,
            "permissionIds": [new_resource_access_level.permissions[0].id]
        }

        new_resource_access_level.save()

        schema = ResourceAccessLevelSchema()
        serialized_data = schema.load_object_into_schema(data)

        assert serialized_data["resource_id"] == data["resourceId"]
        assert serialized_data["permission_ids"] == data["permissionIds"]

    def test_permissions_schema_with_invalid_resource_fails(
            self, new_resource_access_level):
        """
        Should throw an error when the resource matching the query supplied can not be found


        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """
        data = {
            "resourceId": 'tagdagvyasv',
            "permissionIds": [new_resource_access_level.permissions[0].id]
        }

        schema = ResourceAccessLevelSchema()

        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data, partial=True)

    def test_permissions_schema_with_invalid_permission_id_fails(
            self, new_resource_access_level):
        """
        Should throw an error when the permissions matching supplied permission id is not found.

        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """
        data = {
            "resourceId": new_resource_access_level.resource_id,
            "permissionIds": ['gfandgysagagh']
        }

        schema = ResourceAccessLevelSchema()

        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data, partial=True)

    def test_permissions_schema_with_duplicate_permission_ids_succeeds(
            self, new_resource_access_level):
        """Should return no errors when placed into the schema.

        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """
        data = {
            "resourceId":
            new_resource_access_level.resource_id,
            "permissionIds": [
                new_resource_access_level.permissions[0].id,
                new_resource_access_level.permissions[0].id
            ]
        }

        schema = ResourceAccessLevelSchema()

        assert schema.load(data, partial=True).errors == {}

    def test_permissions_schema_with_duplicate_resource_id_fails(
            self, new_resource_access_level):
        """
        Should throw an error when duplicate resource ids are supplied.

        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """

        data = {
            "resourceAccessLevels":
            [{
                "resourceId": new_resource_access_level.resource_id,
                "permissionIds": [new_resource_access_level.permissions[0].id]
            },
             {
                 "resourceId": new_resource_access_level.resource_id,
                 "permissionIds":
                 [new_resource_access_level.permissions[0].id]
             }]
        }

        new_resource_access_level.save()

        schema = RoleSchema()

        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data, partial=True)

    def test_permissions_schema_with_missing_resource_access_levels_key_succeeds(
            self, new_resource_access_level):
        """
        Should not return any error when non recognized field is supplied.

        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """

        data = {
            "unknown key": [{
                "resourceId":
                new_resource_access_level.resource_id,
                "permissionIds": [new_resource_access_level.permissions[0].id]
            },
                            {
                                "resourceId":
                                new_resource_access_level.resource_id,
                                "permissionIds":
                                [new_resource_access_level.permissions[0].id]
                            }]
        }

        new_resource_access_level.save()

        schema = RoleSchema()

        assert schema.load(data, partial=True).errors == {}

    def test_permissions_schema_with_empty_resource_access_levels_key_fails(
            self, new_resource_access_level):
        """
        Should throw an error when an empty list of resourceAccessLevels is supplied.

         Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """

        data = {"resourceAccessLevels": []}

        new_resource_access_level.save()

        schema = RoleSchema()

        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data, partial=True)

    def test_permissions_schema_with_full_access_permission_and_more_than_perm_ids_fails(
            self, new_resource_access_level, new_permissions):
        """
        Should throw an error when the full access permission id is supplied 
        along other permissions.

        Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
            new_permissions (list): A list containing new permissions
        """

        full_permission = new_permissions[3].save()
        other_permission = new_permissions[0].save()

        data = {
            "resourceId": new_resource_access_level.resource_id,
            "permissionIds": [full_permission.id, other_permission.id]
        }

        new_resource_access_level.save()

        schema = ResourceAccessLevelSchema()

        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data, partial=True)

    def test_permissions_schema_with_invalid_resource_access_levels_type_fails(
            self, new_resource_access_level):
        """
        Should throw an error when an empty list of resourceAccessLevels is supplied.

         Args:
            new_resource_access_level (resourceAccessLevel): an instance of resourceAccessLevel
        """

        data = {"resourceAccessLevels": [{}, ""]}

        new_resource_access_level.save()

        schema = RoleSchema()

        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data, partial=True)
