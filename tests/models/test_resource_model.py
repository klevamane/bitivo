import pytest
from api.models import Resource
from api.middlewares.base_validator import ValidationError


class TestResourceModel:
    """
    Test resource model
    """

    def test_new_resource(self, init_db, new_resource):
        """
        Should create and return a resource

        Parameters:
            init_db (object): Used to create the database structure using the models
            new_resource (object): Fixture to create a new resource
        """
        resource = new_resource
        assert resource == new_resource.save()

    def test_count(self):
        """
        Should return the count of available resources
        """
        assert Resource.count() == 1

    def test_query(self):
        """
        Should return the count of available resources through the query_
        """
        assert Resource.query_().count() == 1

    def test_update(self, new_resource):
        """
        Should update a resource
        Parameters:
            new_resource (object): Fixture to update a resource
        """
        new_resource.update_(name='Centers')
        assert new_resource.name == 'Centers'

    def test_resource_model_string_representation(self, new_resource):
        """
        Should compute the official string representation of resource

        Parameters:
            new_resource (object): Fixture to create a new resource
        """
        assert repr(new_resource) == f'<Resource: {new_resource.name}>'

    def test_delete(self, new_resource, request_ctx,
                    mock_request_obj_decoded_token):
        """
        Should remove a resource when deleted
        Parameters:
            request_ctx (object): request client context
            mock_request_obj_decoded_token (object): Mock decoded_token from request object
            new_resource (object): Fixture to create a new resource
        """
        new_resource.delete()
        assert Resource.get(new_resource.id) is None
