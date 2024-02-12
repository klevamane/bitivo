""" Test module for testing celery """
 # System Imports
from unittest.mock import Mock
 # models
from api.models import Asset
 # Mocks
from tests.mocks.asset_migration import MOCK_BOOK_DATA
from tests.mocks.user import REQUESTER


class TestCelery:
    """ Test celery implementation """
    @staticmethod
    def test_celery_app_is_running(init_db, new_spaces, sheet_migration_data):
        """Test that the send email function is being invoked
        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
            sheet_migration_data (object): Mock data for asset category and center
            new_spaces (dict): a dictonary of spaces to be seeded
        """
        # Helpers
        from api.tasks.migration import Migrations
        from manage import mail
        mail.send = Mock()
        asset_category, center = sheet_migration_data
        asset_category.save()
        center.save()
        requester = REQUESTER
        sheet_data = MOCK_BOOK_DATA[asset_category.name]
        Migrations.migrate_assets.s(requester, sheet_data, {'name': asset_category.name,'id': asset_category.id}, center.id, 'sample.email@andela.com').apply()
        mail.send.assert_called_once()
        assets = Asset.query.all()
        assert len(assets) > 1

    def test_celery_app_is_running_duplicate_data(
            self, init_db, sheet_migration_data, new_spaces):
        """Test that the send email function is being invoked for duplicate data
        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
            sheet_migration_data (object): Mock data for asset category and center
            new_spaces (dict): a dictonary of spaces to be seeded
        """
        self.test_celery_app_is_running(init_db, new_spaces,
                                        sheet_migration_data)

    def test_celery_app_is_running_non_duplicate_data(
            self, init_db, sheet_migration_data, new_spaces):
        """Test that the send email function is being invoked for duplicate data
        Args:
            init_db (SQLAlchemy): Fixture to initialize the test database
            sheet_migration_data (object): Mock data for asset category and center
            new_spaces (dict): a dictonary of spaces to be seeded
        """
        self.test_celery_app_is_running(init_db, new_spaces,
                                        sheet_migration_data)
