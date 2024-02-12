"""
Module of tests for user endpoints
"""
# System libraries
from unittest.mock import Mock
from io import BytesIO
# Third-party libraries
from flask import json
import pyexcel as pe
# Constants
from api.utilities.constants import CHARSET
# Messages
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import MIGRATION_ERRORS, database_errors
# Mock data
from tests.mocks.asset_migration import MOCK_BOOK_DATA, INVALID_CATEGORY_NAME

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestMigrateAssetEndpoint:
    """
    Tests endpoint for migrating assets to activo api
    """

    def test_migrate_data_asynchronously_succeeds(
            self, client, init_db, auth_header_form_data, sheet_migration_data,
            get_first_user):
        """Should return an 200 status code and success message notifying the
        user of a scheduled migration
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """
        from api.tasks.migration import Migrations
        category, center = sheet_migration_data
        category.save()
        center.save()
        data = dict(
            file=(BytesIO(b''), 'sheet.xlsx'),
            sheet_name=category.name,
            assigned_by=get_first_user.email,
            center_name=center.name)
        pe.get_book_dict = Mock(side_effect=lambda **kwargs: MOCK_BOOK_DATA)
        Migrations.migrate_assets.delay = Mock()
        response = client.post(
            f'{BASE_URL}/assets/upload',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'asset_migrated'].format('Asset', category.name)

    def test_migrate_data_fails_when_wrong_sheet_name_is_provided(
            self, client, init_db, auth_header_form_data, sheet_migration_data,
            get_first_user):
        """Should return an 400 status code and an error message
        when a wrong sheet name is used it should throw an error
        stating the sheet name is not valid
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """
        category, center = sheet_migration_data
        category.save()
        center.save()
        data = dict(
            file=(BytesIO(b''), 'sheet.xlsx'),
            sheet_name="different name",
            assigned_by=get_first_user.email,
            center_name=center.name)
        pe.get_book_dict = Mock(side_effect=lambda **kwargs: MOCK_BOOK_DATA)
        response = client.post(
            f'{BASE_URL}/assets/upload',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == MIGRATION_ERRORS[
            'not_found'].format('different name')

    def test_migrate_data_fails_when_asset_category_is_not_found(
            self, client, init_db, auth_header_form_data, get_first_user,
            sheet_migration_data):
        """Should return an 404 error status
        when the sheet name provided does not match any asset category in the
        database a validation error is invoked
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """
        category, center = sheet_migration_data
        data = dict(
            file=(BytesIO(b''), 'sheet.xlsx'),
            sheet_name=INVALID_CATEGORY_NAME,
            assigned_by=get_first_user.email,
            center_name=center.name)
        pe.get_book_dict = Mock(side_effect=lambda **kwargs: MOCK_BOOK_DATA)
        response = client.post(
            f'{BASE_URL}/assets/upload',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == database_errors[
            'non_existing'].format('{} category'.format(INVALID_CATEGORY_NAME))

    def test_migrate_data_fails_when_no_sheet_data_is_provided(
            self, client, init_db, auth_header_form_data, get_first_user):
        """Should return an 400 error status
        when the excel sheet data is not provided it throws a validation error stating that
        you need to provide the sheet data
        Args:
            client (FlaskClient): Fixture to get flask test client
            init_db (SQLAlchemy): Fixture to initialize the test database
            auth_header (dict): Fixture to get token
            mock_get (object): Fixture for mocking the get request response
            sheet_asset_category_migration_data (object): Mock data for asset category
        """

        data = dict(assigned_by=get_first_user.email)

        response = client.post(
            f'{BASE_URL}/assets/upload',
            headers=auth_header_form_data,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == MIGRATION_ERRORS['no_file']
