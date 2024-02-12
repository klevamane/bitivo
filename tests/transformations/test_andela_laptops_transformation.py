# Third party libraries
import json
from io import BytesIO
import pyexcel as pe

# Utilities
from mock import Mock

from api.tasks.transformer.accessories_transformer import AccessoriesTransformer

# Mocks
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from tests.mocks.accessories_transformation import ANDELA_LAPTOPS_SHEET_DATA, CLEAN_MOCK_ANDELA_LAPTOPS_DATA

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestAccessoriesTransformation:
    """Tests functions for transforming accessories sheet"""

    def test_andela_laptops_succeeds(self, client, init_db,
                                     auth_header_form_data):
        """Should create a new book with clean data in the Andela Laptops sheet
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header_form_data (dict): Fixture to get auth for form data
        """

        data = dict(
            file=(BytesIO(b''), 'accessories.xlsx'),
            doc_name='accessories',
            email='sample@andela.com',
            center_name='Lagos')
        pe.get_book_dict = Mock(
            side_effect=lambda **kwargs: ANDELA_LAPTOPS_SHEET_DATA)
        AccessoriesTransformer.transform.delay = Mock()
        response = client.post(
            f'{BASE_URL}/sheets/transform',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'transformation_initiated'].format('sample@andela.com')

    def test_andela_laptops_succeeds_with_celery(self, client, init_db):
        """Should create a new book with clean data in the Andela Laptops sheet
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        AccessoriesTransformer.send_email = Mock()
        new_book = AccessoriesTransformer.transform(ANDELA_LAPTOPS_SHEET_DATA,
                                                    'sample@andela.com')

        AccessoriesTransformer.send_email.assert_called_once
        assert new_book == CLEAN_MOCK_ANDELA_LAPTOPS_DATA
