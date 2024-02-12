"""Module for testing the flask seed command"""

# System Imports
from subprocess import call
from os import environ

# Third party
import pytest

# App config
from config import AppConfig

# local Imports
from api.models import (Center, AssetCategory, SpaceType, Space, Asset, Role,
                        User, Permission, Resource, ResourceAccessLevel,
                        StockCount, RequestType, Comment, Request, WorkOrder,
                        Schedule, MaintenanceCategory, HotDeskRequest)
from api.utilities.seed_choices import SEED_OPTIONS
from api.utilities.helpers.seeders import json_to_dictionary

# global variable models mapping
MODELS = {
    'centers': Center.query_,
    'asset_categories': AssetCategory.query_,
    'space_types': SpaceType.query_,
    'spaces': Space.query_,
    'asset': Asset.query_,
    'roles': Role.query_,
    'users': User.query_,
    'permissions': Permission.query_,
    'resources': Resource.query_,
    'resource_access_levels': ResourceAccessLevel.query_,
    'stock_counts': StockCount.query_,
    'request_types': RequestType.query_,
    'requests': Request.query_,
    'comments': Comment.query_,
    'work_orders': WorkOrder.query_,
    'schedules': Schedule.query_,
    'maintenance_category': MaintenanceCategory.query_,
    'hot_desk_requests': HotDeskRequest.query_
}


class TestSeedDatabase:
    """
    Test for checking if the seed command works
    """

    def test_flask_seed_succeeds_without_arguments(self, init_db):
        """
        Should return a length of database objects to be more than zero if its successful when no
        arguments are passed

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        # Seeding all data
        call(["flask", "seed"])

        for names in MODELS.keys():
            results = MODELS[names]().all()
            # check the value of the length returned should be more than zero
            assert len(results) > 0

    def test_flask_seed_succeeds_when_correct_argument_is_used(self, init_db):
        """
        Should return a length of databse objects to be more than zero when
        the correct argument is used with the flask seed command

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        # seed center
        call(["flask", "seed", "centers"])
        result = MODELS['centers']().all()
        assert len(result) > 0

        # seed asset category
        call(["flask", "seed", "asset_categories"])
        result = MODELS['asset_categories']().all()
        assert len(result) > 0

        # seed space type
        call(["flask", "seed", "space_types"])
        result = MODELS['space_types']().all()
        assert len(result) > 0

        # seed space
        call(["flask", "seed", "spaces"])
        result = MODELS['spaces']().all()
        assert len(result) > 0

        # seed roles
        call(["flask", "seed", "roles"])
        result = MODELS['roles']().all()
        assert len(result) > 0

        # seed user
        call(["flask", "seed", "users"])
        result = MODELS['users']().all()
        assert len(result) > 0

        # seed permissions
        call(["flask", "seed", "permissions"])
        result = MODELS['permissions']().all()
        assert len(result) > 0

        # seed asset
        call(["flask", "seed", "asset"])
        result = MODELS['asset']().all()
        assert len(result) > 0

        # seed resource
        call(["flask", "seed", "resources"])
        result = MODELS['resources']().all()
        assert len(result) > 0

        # seed resource access level
        call(["flask", "seed", "resource_access_levels"])
        result = MODELS['resource_access_levels']().all()
        assert len(result) > 0

        # seed stock counts
        call(["flask", "seed", "stock_counts"])
        result = MODELS['stock_counts']().all()
        assert len(result) > 0

        # seed request types
        call(["flask", "seed", "request_types"])
        result = MODELS['request_types']().all()
        assert len(result) > 0

        # seed requests
        call(["flask", "seed", "requests"])
        result = MODELS['requests']().all()
        assert len(result) > 0

        # seed comments
        call(["flask", "seed", "comments"])
        result = MODELS['comments']().all()
        assert len(result) > 0

        # seed work orders
        call(["flask", "seed", "work_orders"])
        result = MODELS['work_orders']().all()
        assert len(result) > 0

        # seed schedules
        call(["flask", "seed", "schedules"])
        result = MODELS['schedules']().all()
        assert len(result) > 0

        # seed maintenance categories
        call(["flask", "seed", "maintenance_category"])
        result = MODELS['maintenance_category']().all()
        assert len(result) > 0

        # seed hot desk requests
        call(["flask", "seed", "hot_desk_requests"])
        result = MODELS['hot_desk_requests']().all()
        assert len(result) > 0

    def test_flask_seed_succeeds_with_case_insensitive_arguments(
            self, init_db):
        """
        Should return database objects more than zero when successful even if
        the case are insensitive

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """
        # seed center
        call(["flask", "seed", "CENTERS"])
        result = MODELS['centers']().all()
        assert len(result) > 0

        # seed asset category
        call(["flask", "seed", "aSSet_cateGories"])
        result = MODELS['asset_categories']().all()
        assert len(result) > 0

        # seed space type
        call(["flask", "seed", "sPAce_TYpes"])
        result = MODELS['space_types']().all()
        assert len(result) > 0

        # seed space
        call(["flask", "seed", "spACEs"])
        result = MODELS['spaces']().all()
        assert len(result) > 0

    def test_flask_seed_fails_when_wrong_arguments_are_used(
            self, init_db, capfd):
        """
        Should return an error message error showing the accepted arguments when
        wrong arguments are used

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
            capfd(pytest): fixture to allow access to stdout/stderr output
        """
        call(["flask", "seed", "something_ELSE"])

        # capture the stderr output from the terminal
        captured = capfd.readouterr()
        output = ', '.join([choice for choice in SEED_OPTIONS])
        assert f'choose from {output}' in captured.err

    def test_flask_seed_with_argument_in_production_environ_succeeds(
            self, init_db):
        """
        Should return a length of database objects to be more than zero when
        the correct argument is used with the flask seed command

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        # Saves test environment variable and sets it to 'production'
        test_env = AppConfig.FLASK_ENV
        environ['FLASK_ENV'] = 'production'

        # seed center
        call(["flask", "seed", "centers"])
        result = MODELS['centers']().all()
        assert len(result) > 0
        # Restores test environment variable.
        environ['FLASK_ENV'] = test_env

    def test_flask_seed_only_new_records_succeeds(self, init_db):
        """Tests only new records are seeded while existing records are skipped

        Args:
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        Asset.query.filter_by(tag='AND/K32/001').delete()
        assets = MODELS['asset']().all()
        init_db.session.commit()

        # seed asset data
        call(["flask", "seed", "asset"])
        result = MODELS['asset']().all()
        # Checks that new record added
        assert len(result) > len(assets)

    def test_get_environment_based_data_with_invalid_file_name(self):
        """Tests that error raised if json seed data file not found"""

        with pytest.raises(FileNotFoundError):
            json_to_dictionary('test_file_path')
