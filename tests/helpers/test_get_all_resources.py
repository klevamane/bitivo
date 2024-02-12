"""Test get all resource helper"""
import pytest
from unittest.mock import patch
from api.utilities.helpers.resource_manipulation import get_all_resources
from api.utilities.messages.error_messages import serialization_errors
from api.middlewares.base_validator import ValidationError


class TestGetAllResources:
    '''tests get all resources helper with invalid colum in exta_query'''

    @patch('api.utilities.helpers.resource_manipulation.request')
    def test_get_all_resources_with_invalid_extra_query_key_fails(
            self, mock_request, app, asset_category_and_schema):
        """Test get all resource when invalid column is passed to extra_query

        Args:
            mock_request (MagicMock): flask request mock instance
            app (Instance): fixture to initialize the flask app
            asset_category_and_schema(dict): a dictionary containing asset_category model and schema
        """
        mock_request.args = {}
        with app.test_request_context(
                'my-url?pagination=false'), pytest.raises(
                    ValidationError) as error:
            get_all_resources(
                asset_category_and_schema['model'],
                asset_category_and_schema['schema'],
                extra_query={'wrong column': 'hi'})
        assert error.value.error['message'] == \
            serialization_errors['invalid_field']
