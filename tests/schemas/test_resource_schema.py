import pytest
from api.schemas.resource import ResourceSchema
from api.middlewares.base_validator import ValidationError

from api.utilities.messages.error_messages import serialization_errors


class TestResourceSchema:
    """
    Test resource schema
    """

    def test_resource_schema_with_valid_data_passes(self, init_db):
        """
        Should pass when valid resource data is supplied
        """
        data = {'name': 'Assets'}
        schema = ResourceSchema()
        serialized_data = schema.load_object_into_schema(data)
        assert serialized_data['name'] == data['name']

    def test_resource_schema_with_invalid_data_fails(self, init_db):
        """
        Should fail with invalid resource data
        """
        data = {'name': '@232Assets'}
        schema = ResourceSchema()
        with pytest.raises(ValidationError):
            schema.load_object_into_schema(data)

    def test_resource_schema_with_name_exceeding_length_fails(self):
        """ Should fail with name exceeding a length of 60 """

        data = {
            'name':
            'AssetsAssetsAssetsAssetsAssetsAssetsAssetsAssetsAssetsAssetsAssets'
        }
        schema = ResourceSchema()

        with pytest.raises(ValidationError) as error:
            schema.load_object_into_schema(data)

        assert error.value.error['status'] == 'error'
