# Standard
from unittest.mock import patch

# Third Party Libraries
import pytest

# Utilities
from api.utilities.paginator import pagination_helper
from api.utilities.messages.error_messages import serialization_errors

# Middlewares
from api.middlewares.base_validator import ValidationError


class TestPaginationHelper:
    """tests pagination_helper function"""

    @patch('api.utilities.paginator.request')
    def test_pagination_help_with_invalid_extra_query_key_fails(
            self, mock_request, app, asset_category_and_schema):
        """Test pagination_helper raises ValidationError with invalid extra_query column or key

        Args:
            mock_request (MagicMock): flask request mock instance
            app (Instance): fixture to initialize the flask app
            asset_category_and_schema(dict): a dictionary containing asset_category model and schema

        """
        mock_request.args = {}

        with app.test_request_context(
                "/test-url?where=created_at,gl, 18-06-2018 12:06:43.339809"
        ), pytest.raises(ValidationError) as error:

            pagination_helper(
                asset_category_and_schema['model'],
                asset_category_and_schema['schema'],
                extra_query={'invalid_column': 'test_value'})

        assert error.value.error['message'] == serialization_errors[
            'invalid_field']
