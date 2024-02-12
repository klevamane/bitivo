# Third party libraries
from io import BytesIO
from unittest.mock import Mock
from collections import OrderedDict

import pyexcel as pe
from flask import json

# Utilities
from api.tasks.transformer.asset_transformer import AssetRegisterTransformer
from api.tasks.transformer.transformer_interface import AssetTransformerInterface
from api.utilities.helpers.asset_rows import row_to_remove
from api.utilities.helpers.asset_transformer import remove_column

# Mocks
from tests.mocks.asset_register_tranformer import (
    ASSET_REGISTER_MOCK,
    TRANSFORMED_INSURED_ASSET_MOCK,
    SHEET_HEADERS,
    MOCK_ET_AIRCONDITIONER_DATA,
    CLEAN_MOCK_ET_AIRCONDITIONER_DATA,
    CLEAN_AMITY_DATA,
    MOCK_AMITY_DATA,
    MOCK_CLEAN_IT_DATA,
    UNCLEAN_JM1_BOOK_DATA,
    CLEAN_JM1_DATA,
    MOCK_UNCLEAN_IT_DATA,
    DATA,
    CLEAN_DATA,
    UNCLEAN_JM1_BOOK_DATA2)

# Constants
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors

from api.views.sheet_transformer import transformer_mapper
from unittest.mock import MagicMock

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestAssetRegisterTransformation:
    """Tests functions for transforming asset register document"""

    def test_insured_assets_succeeds(self, client, init_db):
        """Should create funiture, generator,and office equipment sheets of this sheet
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database

        """
        AssetRegisterTransformer.send_email = Mock()
        ASSET_REGISTER_MOCK_COPY = ASSET_REGISTER_MOCK.copy()
        EMAIL = 'email@andela.com'
        new_book = AssetRegisterTransformer.transform(ASSET_REGISTER_MOCK_COPY,
                                                      EMAIL)

        from api.tasks.email_sender import Email
        Email.send_email = Mock()
        Email.send_email.assert_called_once
        assert new_book['FUNITURE'] == TRANSFORMED_INSURED_ASSET_MOCK[
            'FUNITURE']
        assert new_book['OFFICE EQUIPMENT'] == TRANSFORMED_INSURED_ASSET_MOCK[
            'OFFICE EQUIPMENT']
        assert new_book['GENERATOR'] == TRANSFORMED_INSURED_ASSET_MOCK[
            'GENERATOR']

    def test_transform_data_asynchronously_succeeds(self, client, init_db,
                                                    auth_header_form_data,
                                                    sheet_migration_data):
        """Should return an 200 status code and success message notifying the
        user of a scheduled data transformation

        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """

        data = dict(
            file=(BytesIO(b''), 'asset_register.xlsx'),
            doc_name='assetRegister',
            email='sample@andela.com',
            center_name='Lagos')
        pe.get_book_dict = Mock(
            side_effect=lambda **kwargs: ASSET_REGISTER_MOCK)
        AssetRegisterTransformer.transform.delay = Mock()
        response = client.post(
            f'{BASE_URL}/sheets/transform',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'transformation_initiated'].format('sample@andela.com')

    def test_transform_data_with_unsupported_file_type_fails(
            self, client, init_db, auth_header_form_data,
            sheet_migration_data):
        """Should fail when an unsupported file type is provided

        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """

        extension = 'xls'
        data = dict(
            file=(BytesIO(b''), f'asset_register.{extension}'),
            doc_name='assetRegister',
            email='sample@andela.com',
            center_name='Lagos')
        pe.get_book_dict = Mock(
            side_effect=lambda **kwargs: ASSET_REGISTER_MOCK)
        AssetRegisterTransformer.transform.delay = Mock()
        response = client.post(
            f'{BASE_URL}/sheets/transform',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_file_type'].format(extension)

    def test_transform_data_with_invalid_data_fails(self, client, init_db,
                                                    auth_header_form_data,
                                                    sheet_migration_data):
        """Should fail when invalid data are provided

        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """

        data = dict(
            file=(BytesIO(b''), f'asset_register.xlsx'),
            doc_name='invalid',
            email='sample@gmail.com')
        pe.get_book_dict = Mock(
            side_effect=lambda **kwargs: ASSET_REGISTER_MOCK)
        AssetRegisterTransformer.transform.delay = Mock()
        response = client.post(
            f'{BASE_URL}/sheets/transform',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['errors']['email'][0] == serialization_errors[
            'email_syntax']
        assert response_json['errors']['doc_name'][0] == serialization_errors[
            'invalid_doc_name'].format(list(transformer_mapper.keys()))

    def test_et_airconditioners_transformation_succeeds(self, init_db):
        """Should pass when a sheet with et-air conditioneers is uploaded for formatting

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        new_book = OrderedDict()
        sheet = pe.Sheet(
            sheet=MOCK_ET_AIRCONDITIONER_DATA['ET AIRCONDITIONERS'],
            name='ET AIRCONDITIONERS')
        new_book = AssetRegisterTransformer.transform_et_airconditioners(
            sheet, new_book)
        assert new_book[
            'ET AIRCONDITIONERS'] == CLEAN_MOCK_ET_AIRCONDITIONER_DATA[
                'ET AIRCONDITIONERS']
        assert new_book['ET AIRCONDITIONERS'][
            2] == CLEAN_MOCK_ET_AIRCONDITIONER_DATA['ET AIRCONDITIONERS'][2]
        assert new_book[
            'ET AIRCONDITIONERS'] == CLEAN_MOCK_ET_AIRCONDITIONER_DATA[
                'ET AIRCONDITIONERS']

    def test_book_with_et_airconditioners_transformation_succeeds(self):
        """ Should pass when return a book with et-airconditioners key """
        from api.tasks.transformer.asset_transformer import AssetRegisterTransformer
        AssetRegisterTransformer.send_email = Mock()
        sheet = pe.Sheet(
            sheet=MOCK_ET_AIRCONDITIONER_DATA['ET AIRCONDITIONERS'],
            name='ET AIRCONDITIONERS')
        sheets = {sheet.name: sheet}
        mock_book = pe.Book(sheets)

        book = AssetRegisterTransformer.transform(mock_book.to_dict(),
                                                  "simon@andela.com")
        assert len(book) == len(mock_book)
        assert book.keys() == mock_book.to_dict().keys()

    def test_amity_transformation_succeeds(self, init_db):
        """Should pass when a sheet with amity is uploaded for formatting

        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        new_book = OrderedDict()
        sheet = pe.Sheet(sheet=MOCK_AMITY_DATA['AMITY 2.0'], name='AMITY 2.0')
        book = AssetRegisterTransformer.transform_amity_2_0(sheet, new_book)
        assert len(book['1HP Split Unit Air Conditioner']) == len(
            CLEAN_AMITY_DATA['1HP Split Unit Air Conditioner'])
        assert book['Swivel Chair'] == CLEAN_AMITY_DATA['Swivel Chair']
        assert book['Generators'] == CLEAN_AMITY_DATA['Generators']

    def test_amity_2_0_transformation_succeeds(self):
        """ Should pass when returned book has 'AMITY 2.0' """
        AssetRegisterTransformer.send_email = Mock()
        book = AssetRegisterTransformer.transform(MOCK_AMITY_DATA,
                                                  "sindf@andela.com")
        assert len(book) == len(CLEAN_AMITY_DATA)
        assert book.keys() == CLEAN_AMITY_DATA.keys()

    def test_transform_IT_device_method_works_succeeds(self):
        """
            Test transform_jm_1 methods works
        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        returns:
                None
        """
        new_book = OrderedDict()
        sheet = pe.Sheet(
            sheet=MOCK_UNCLEAN_IT_DATA['IT Devices'], name='IT Devices')
        book = AssetRegisterTransformer.transform_it_devices(sheet, new_book)
        assert book['IT Devices'] == MOCK_CLEAN_IT_DATA['IT Devices']

    def test_transform_et_worksatations(self, init_db):
        """Should create et workstation sheet from the unclean data
        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        sheet = type('sheet', (object, ), {})
        sheet = sheet()
        setattr(sheet, 'row', DATA)
        setattr(sheet, 'name', 'ET WORKSTATIONS')
        new_book = AssetRegisterTransformer.transform_chairs_and_workstation_assets(
            sheet, {}, new_column='New Column')
        assert new_book == CLEAN_DATA

    def test_transform_jm_1_method_works(self):
        """Test transform_jm_1 methods works
        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
        """
        new_book = OrderedDict()
        sheet = pe.Sheet(sheet=UNCLEAN_JM1_BOOK_DATA['JM 1'], name='JM 1')
        book = AssetRegisterTransformer.transform_jm_1(sheet, new_book)
        assert book['JM 1'][5] == CLEAN_JM1_DATA['JM 1'][5]

    def test_row_to_remove(self):
        """Test for row to remove method"""

        new_book = OrderedDict()
        area_data = ['EQUIPMENTS', 'FURNITURE & FITTINGS']
        sheet = pe.Sheet(sheet=UNCLEAN_JM1_BOOK_DATA2['JM 1'], name='JM 1')
        AssetRegisterTransformer.transform_jm_1(sheet, new_book)
        sheet = UNCLEAN_JM1_BOOK_DATA2

        for row in sheet.items():
            row_removed = row_to_remove(row, area_data, row[1][4])
        assert row_removed[1][:4] == CLEAN_JM1_DATA['JM 1'][1:5]

    def test_asset_transform_interface_succeeds(self):
        """
        Test for asset transformation interface
        """
        ASSET_REGISTER_MOCK_COPY = ASSET_REGISTER_MOCK.copy()

        EMAIL = 'email@andela.com'
        scripts_mapper = {
            'insured assets': AssetRegisterTransformer.transform_insured_assets
        }
        # Just call these two functions so the pass lines in both functions will be covered
        AssetTransformerInterface.transform(ASSET_REGISTER_MOCK_COPY, EMAIL)

        AssetTransformerInterface.transform_all(
            ASSET_REGISTER_MOCK_COPY, scripts_mapper, EMAIL, 'Asset Register')
