"""Module for setting up fixtures for testing"""
# pylint: skip-file
from os import environ

import alembic.command
import alembic.config
import dramatiq
# Third-party libraries
import pytest
from dramatiq.brokers.redis import RedisBroker
from flask import current_app, g, request
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (DropConstraint, DropTable, ForeignKeyConstraint,
                               MetaData, Table)

# Models
from api.models import (AssetCategory, Attribute, Center, Permission, Resource,
                        ResourceAccessLevel, WorkOrder)
# Database
from api.models.database import db
# Utilities
from api.utilities.dynamic_filter import DynamicFilter
from config import AppConfig
# Local imports
from main import create_app

environ['FLASK_ENV'] = 'testing'

pytest_plugins = [
    "tests.fixtures.comments", "tests.fixtures.maintenance_categories",
    "tests.fixtures.work_orders", "tests.fixtures.requests",
    "tests.fixtures.schedules", "tests.fixtures.request_types",
    "tests.fixtures.users", "tests.fixtures.roles",
    "tests.fixtures.attributes", "tests.fixtures.space_types",
    "tests.fixtures.asset_categories", "tests.fixtures.resources",
    "tests.fixtures.centers", "tests.fixtures.spaces",
    "tests.fixtures.stock_counts", "tests.fixtures.resource_access_levels",
    "tests.fixtures.assets", "tests.fixtures.permissions",
    "tests.fixtures.asset_repair", "tests.fixtures.authorization",
    "tests.fixtures.hot_desk", "tests.fixtures.slack",
    "tests.fixtures.sendgrid", "tests.fixtures.hot_desk_response",
    "tests.fixtures.asset_supporting_document",
    "tests.fixtures.asset_note", "tests.fixtures.asset_insurance",
    "tests.fixtures.asset_warranty",
]

redis_broker = RedisBroker(url=AppConfig.REDIS_URL)
dramatiq.set_broker(redis_broker)


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """

    _app = create_app(AppConfig)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='module')
def init_db(app):
    db.drop_all()
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()

@pytest.fixture(scope='module')
def request_ctx():
    """
    Setup a request client, this gets executed for each test module.
    :param app: Pytest fixture
    :return: Flask request client
    """
    ctx = current_app.test_request_context()
    ctx.push()
    yield ctx
    ctx.pop()


@pytest.fixture(scope='module')
def dynamic_filter():
    """
    Create the DynamicFilter object for testing
    """
    return DynamicFilter(AssetCategory)


@pytest.fixture(scope="function")
def set_up_db(app):
    # reset database at beginning of test
    db_drop_all(db)
    alembic_cfg = alembic.config.Config("./migrations/alembic.ini")
    alembic.command.stamp(alembic_cfg, 'base')

    yield
    # clean database at end of test
    db.session.close()
    db_drop_all(db)


def db_drop_all(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []

        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk['name']))
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()

    db.engine.execute("DROP TABLE IF EXISTS alembic_version CASCADE")
    db.engine.execute("DROP SEQUENCE IF EXISTS requests_id_seq CASCADE")

    sequences = [
        'assignee_type', 'frequencytypesenum', 'requeststatusenum',
        'schedulestatusenum', 'hotdeskrequeststatusenum', 'frequencyenum',
        'statusenum', 'parenttype', 'hotdeskresponsestatusenum',
        'repairlogstatusenum', 'assetsupportingdocumenttypeenum',
        'assetwarrantystatusenum'
    ]

    sequences_ = ','.join(sequences)
    sql = f'DROP TYPE IF EXISTS {sequences_} CASCADE'
    db.engine.execute(sql)
