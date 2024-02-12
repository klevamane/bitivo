import pytest
from api.models import ResourceAccessLevel
from api.middlewares.base_validator import ValidationError


class TestResourcesAccessLevelModel:
    """
    Test resources access level model
    """

    def test_new_resources_access_level(self, init_db,
                                        new_resource_access_level):
        """
        Should create and return a resource

        Parameters:
            init_db (object): Used to create the database structure using the models
            new_resource_access_level (object): Fixture to create a new resource access level
        """
        access_level = new_resource_access_level
        assert access_level == new_resource_access_level.save()

    def test_count(self):
        """
        Should return the count of available resource access levels
        """
        assert ResourceAccessLevel.count() == 1

    def test_query(self):
        """
        Should return the count of available resource access levels through the query_
        """
        assert ResourceAccessLevel.query_().count() == 1

    def test_update(self, new_permission, new_resource_access_level):
        """
        Should update a resource access level
        Parameters:
            new_permission (object): Fixture to create a permission
            new_resource_access_level (object): Fixture to update a resource
        """
        permissions = [new_permission]
        new_resource_access_level.update_(permissions=permissions)
        assert new_resource_access_level.permissions == permissions

    def test_resource_access_level_model_string_representation(
            self, new_resource_access_level):
        """
        Should compute the official string representation of resource access level
        """
        assert repr(
            new_resource_access_level
        ) == f'<ResourceAccessLevel: resource_id: {new_resource_access_level.resource_id} role_id: {new_resource_access_level.role_id}>'

    def test_delete(self, new_resource_access_level, request_ctx,
                    mock_request_obj_decoded_token):
        """
        Should remove a resource access level when deleted
        Parameters:
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request object
            new_resource_access_level (object): Fixture to create a new resource access level
        """
        new_resource_access_level.delete()
        assert ResourceAccessLevel.get(new_resource_access_level.id) is None
