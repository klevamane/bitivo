#system libraries
from unittest.mock import Mock
from io import BytesIO

#third-party libraries
from flask import json
import pyexcel as pe

#Constants
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# app config
from config import AppConfig

#mock data
from tests.mocks.asset_migration import CLEAN_MOCK_USB_DATA, DATA
BASE_URL = AppConfig.API_BASE_URL_V1
from api.tasks.transformer.accessories_transformer import AccessoriesTransformer


class TestTransformUsbSheet:
    """
    Tests endpoint for transforming usb-c dongle sheet
    """

    def test_transform_usb_c_dongle_succeed(self, init_db,
                                            auth_header_form_data, client):
        """Should return an 200 status code and success message notifying the
              user of a scheduled migration
              Args:
                  client (FlaskClient): Fixture to get flask test client
                  init_db (SQLAlchemy): Fixture to initialize the test database
                  auth_header (dict): Fixture to get token
        """
        data = dict(
            file=(BytesIO(b''), 'accessories_register.xlsx'),
            doc_name='assetRegister',
            email='sample@andela.com',
            center_name='Lagos')
        pe.get_book_dict = Mock(
            side_effect=lambda **kwargs: CLEAN_MOCK_USB_DATA)
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

    def test_celery_app_is_running(self, init_db):
        """Should check if celery app is running
              Args:
                  init_db (SQLAlchemy): Fixture to initialize the test database
        """
        sheet = pe.Sheet(DATA)

        new_book = AccessoriesTransformer.transform_usb_dongle_assets(
            sheet, {})
        new_sheet = {'USB-C Dongle': pe.Sheet(CLEAN_MOCK_USB_DATA)}

        assert new_book['USB-C Dongle'][0] == new_sheet['USB-C Dongle'][0]
        assert type(new_sheet) == dict
        assert type(new_book) == dict
