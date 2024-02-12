"""Module with assets fixtures """

# System libraries
import json
import datetime as dt
from dateutil.relativedelta import *
import random
import string

# Third Party Modules
import pytest

# Database
from api.models.database import db

# Models
from api.models import AssetCategory, Asset, StockCount, Center, Attribute

# Utilities
from api.utilities.helpers.random_string_gen import gen_string
from api.utilities.enums import AssigneeType


@pytest.fixture(scope='function')
def new_asset(init_db, new_user, new_center, new_space):
    asset_category = AssetCategory(name='test_category').save()
    new_user.save()
    new_space.save()
    asset = Asset(
        tag='AND/VET/' + str(random.randint(100, 500)),
        center_id=new_center.id,
        assignee_id=new_space.id,
        assignee_type='space',
        asset_category_id=asset_category.id,
        created_by=new_user.token_id)
    return asset.save()


@pytest.fixture(scope='module')
def new_asset_for_asset_note(init_db, new_center, new_space, new_user):
    new_user.save()
    asset_category = AssetCategory(name='test_category').save()
    new_space.save()
    asset = Asset(
        tag='AND/VET/' + str(random.randint(100, 500)),
        center_id=new_center.id,
        assignee_id=new_space.id,
        assignee_type='space',
        asset_category_id=asset_category.id)
    return asset.save()


@pytest.fixture(scope='module')
def new_asset_for_asset_warranty(init_db, new_center, new_space, new_user):
    new_user.save()
    asset_category = AssetCategory(name='test_category').save()
    new_space.save()
    asset = Asset(
        tag='AND/VET/' + str(random.randint(100, 500)),
        center_id=new_center.id,
        assignee_id=new_space.id,
        assignee_type='space',
        asset_category_id=asset_category.id)
    return asset.save()


@pytest.fixture(scope='module')
def new_data_for_asset_flows_test(app, init_db, new_user, new_center,
                                  new_space_two, new_space):
    new_user.save()
    new_center.save()
    new_space_two.save()
    new_space.save()
    today = dt.datetime.today()
    asset_category = AssetCategory(name='another_category').save()
    StockCount(
        count=10,
        asset_category_id=asset_category.id,
        center_id=new_center.id,
        token_id=new_user.token_id,
        week=1).save()
    records = [{
        'tag': 'AND/TEST/002',
        'center_id': new_center.id,
        'assignee_id': new_space_two.id,
        'assignee_type': 'store',
        'asset_category_id': asset_category.id,
        'date_assigned': today,
    },
               {
                   'tag': 'AND/TEST/003',
                   'center_id': new_center.id,
                   'assignee_id': new_space.id,
                   'assignee_type': 'space',
                   'asset_category_id': asset_category.id,
                   'date_assigned': today,
               },
               {
                   'tag': 'AND/TEST/004',
                   'center_id': new_center.id,
                   'assignee_id': new_space.id,
                   'assignee_type': 'space',
                   'asset_category_id': asset_category.id,
                   'date_assigned': today,
               }]

    return [Asset(**data).save() for data in records]


@pytest.fixture(scope='module')
def asset_flows_data(app, new_test_asset_category, new_user, new_space_store):
    """Fixture for a stock count.

    Args:
        app (object): application
        new_test_asset_category (object): fixture for a new asset category
        new_center (object): fixture for a new center
        new_user (object): fixture for a new user
        new_space_store (object): fixture for a new space with type store

    """
    user = new_user.save()
    category = new_test_asset_category.save()
    new_space_store.save()
    stock_count = StockCount(
        count=1,
        asset_category_id=category.id,
        center_id=new_space_store.center_id,
        token_id=user.token_id,
        week=1)
    stock_count.save()
    inflow = Asset(
        tag=f'AND/12/LAP',
        asset_category_id=category.id,
        assignee_id=new_space_store.id,
        assignee_type='store',
        assigned_by='Eze',
        center_id=new_space_store.center_id,
        date_assigned='2018-11-09 00:00:00').save()
    outflow = Asset(
        tag=f'AND/13/LAP',
        asset_category_id=category.id,
        assignee_id=user.token_id,
        assignee_type='user',
        assigned_by='Eze',
        center_id=new_space_store.center_id,
        date_assigned='2018-11-09 00:00:00').save()

    return inflow, outflow


@pytest.fixture(scope='module')
def asset_out_flow(new_user, new_space):
    """Add Assets for testing outflow"""
    new_user.save()
    new_space.save()
    category_one = AssetCategory(name=gen_string()).save()
    category_two = AssetCategory(name=gen_string()).save()
    now = dt.datetime.now()
    assets_outflow_data = [{
        'asset_category_id':
        category_one.id,
        'created_at':
        dt.datetime.now() - relativedelta(months=1),
        'assigned_by':
        new_user.name,
        'assignee_id':
        new_space.id,
        'date_assigned':
        dt.datetime.now() - relativedelta(days=3),
        'assignee_type':
        'space',
        'tag':
        gen_string()
    },
                           {
                               'asset_category_id':
                               category_one.id,
                               'created_at':
                               dt.datetime(now.year, now.month, 1),
                               'assigned_by':
                               new_user.name,
                               'assignee_id':
                               new_space.id,
                               'date_assigned':
                               dt.datetime.now() - relativedelta(days=2),
                               'assignee_type':
                               'space',
                               'tag':
                               gen_string()
                           }]
    return [
        Asset(**asset_outflow).save() for asset_outflow in assets_outflow_data
    ]


@pytest.fixture(scope='module')
def asset_inflow_list(init_db, new_center, new_space):
    """Fixture for asset inflow.

    Args:
        init_db (object): Initialize the test db
        new_center (dict): fixture for a new center
        new_space (dict): fixture for a new space

    Returns:
            asset (Request): Object of the created asset
    """
    now = dt.datetime.now()
    asset_category = AssetCategory(name='test_category2').save()
    new_space.save()
    new_center.save()
    asset = [{
        'tag': 'AND/VET/114',
        'center_id': new_center.id,
        'assignee_id': new_space.id,
        'assignee_type': AssigneeType.store.value,
        'asset_category_id': asset_category.id,
        'date_assigned': dt.datetime.now() - relativedelta(months=1),
        'status': 'ok'
    },
             {
                 'tag': 'AND/VET/113',
                 'center_id': new_center.id,
                 'assignee_id': new_space.id,
                 'assignee_type': AssigneeType.store.value,
                 'asset_category_id': asset_category.id,
                 'date_assigned': dt.datetime(now.year, now.month, 1),
                 'status': 'ok'
             }]
    return [Asset(**asset_inflow).save() for asset_inflow in asset]


@pytest.fixture(scope='module')
def asset_inflow(init_db, new_center, new_space, new_user):
    """Fixture for asset inflow.

    Args:
        init_db (object): Initialize the test db
        new_center (object): fixture for a new center
        new_space (object): fixture for a new space

    Returns:
            asset (Request): Object of the created asset
    """
    new_user.save()
    now = dt.datetime.now()
    asset_category = AssetCategory(name='test_category2').save()
    new_space.save()
    new_center.save()
    asset = Asset(
        tag='AND/VET/112',
        center_id=new_center.id,
        assignee_id=new_space.id,
        assignee_type=AssigneeType.store.value,
        asset_category_id=asset_category.id,
        date_assigned=now,
        status='ok')
    return asset.save()


@pytest.fixture(scope='function')
def asset_with_attrs(new_user):
    """Test asset with no custom attributes."""
    category = AssetCategory(name=gen_string()).save()
    center = Center(name=gen_string(), image={"meta": gen_string()}).save()
    new_user.save()

    attributes = [{
        '_key': 'warranty',
        'label': 'warranty',
        'is_required': True,
        'asset_category_id': category.id,
        'input_control': 'Text'
    },
                  {
                      '_key': 'length',
                      'label': 'length',
                      'input_control': 'Text',
                      'asset_category_id': category.id,
                      'is_required': False
                  },
                  {
                      '_key': 'color',
                      'label': 'Color',
                      'input_control': 'dropdown',
                      'choices': 'Green,Red',
                      'asset_category_id': category.id,
                      'is_required': False
                  },
                  {
                      '_key': 'screen size',
                      'label': 'screenSize',
                      'input_control': 'radio button',
                      'choices': 'Yellow,Purple',
                      'asset_category_id': category.id,
                      'is_required': True
                  }]

    for attribute in attributes:
        db.session.add(Attribute(**attribute))
    db.session.commit()
    data = {
        'tag': gen_string(),
        'asset_category_id': category.id,
        'center_id': center.id,
        'status': 'available',
        'assignee_id': new_user.token_id,
        'assignee_type': 'user',
        'created_by': new_user.token_id,
        'custom_attributes': {
            'warranty': '2019-02-09',
            'length': '12cm',
            'screen size': 'Red',
            'color': 'Green',
            'serialNumber': '10',
            'sortCode': '12ACD'
        }
    }
    asset = Asset(**data)
    return asset.save()


@pytest.fixture(scope='module')
def asset_without_attributes(new_user):
    """Test asset with no custom attributes."""
    category = AssetCategory(name=gen_string()).save()
    center = Center(name=gen_string(), image={"meta": gen_string()}).save()
    new_user.save()

    data = {
        'tag': gen_string(),
        'asset_category_id': category.id,
        'center_id': center.id,
        'assignee_id': new_user.token_id,
        'assignee_type': 'user',
        'assigned_by': new_user.name,
        'date_assigned': '2018-11-03 00:00:00',
        'custom_attributes': {},
        'created_by': new_user.token_id
    }
    asset = Asset(**data)
    return asset.save()


@pytest.fixture(scope='module')
def asset_with_invalid_status(app, test_asset_category, new_spaces):
    """Fixture for new asset with invalid status field
    Args:
        app (Flask): Instance of Flask test app
        test_asset_category (AssetCategory): Fixture for AssetCategory object
        new_spaces (list): Fixture of a collection of Space objects
    Returns:
        dict: Data for new asset with invalid  status
    """
    return {
        'tag': "Anaeze's Macbook",
        'assetCategoryId': test_asset_category.id,
        'spaceId': new_spaces["spaces"][0].id,
        'status': 'invalid_status'
    }


@pytest.fixture(scope='function')
def asset_details(assignee_details, new_center, asset_without_attributes):
    asset_data = {
        'centerId': new_center.id,
        'assetCategoryId': asset_without_attributes.asset_category_id,
        'tag': ''.join(random.choices(string.ascii_letters, k=9))
    }

    def func(assignee_type='user', **kwargs):
        assignee_types = {
            'user': {
                **asset_data,
                **assignee_details('user')
            },
            'space': {
                **asset_data,
                **assignee_details('space')
            }
        }
        result = assignee_types.get(assignee_type)
        result.update(**kwargs)
        return result

    return func


@pytest.fixture(scope="function")
def multiple_assets():
    assets = {
        "assetCategoryId":
        "-Lc1qCsjU35Ek895mzq7",
        "assetCategoryName":
        "MONITORS",
        "assets": [{
            "assetCategoryId": "-L_lqkv-GWte5E_nolGL",
            "tag": "AND/634/12",
            "assigneeId": "-L_lql2gUguQLTBmPkpv",
            "assigneeType": "space",
            "status": "ok",
            "waranty": "done"
        },
                   {
                       "assetCategoryId": "-L_lqkv-GWte5E_nolGL",
                       "tag": "AND/634/13",
                       "assigneeId": "-L_lql3gAMVhOarf6HYc",
                       "assigneeType": "user",
                       "status": "ok",
                       "waranty": "done"
                   },
                   {
                       "assetCategoryId": "-L_lqkv-GWte5E_nolGL",
                       "tag": "AND/634/14",
                       "assigneeId": "-L_lql2gUguQLTBmPkpv",
                       "assigneeType": "space",
                       "status": "ok",
                       "length": "done",
                       "waranty": "djsdfjkn"
                   },
                   {
                       "assetCategoryId": "-L_lqkv-GWte5E_nolGL",
                       "tag": "AND/634/15",
                       "assigneeId": "-L_lql3gAMVhOarf6HYc",
                       "assigneeType": "user",
                       "status": "ok",
                       "waranty": "done"
                   }]
    }
    return assets


@pytest.fixture(scope="function")
def multiple_assets2():
    assets = {
        "assetCategoryName":
        "MONITORS",
        "assigneeType":
        "space",
        "assignee":
        "Non-Existing Assignee",
        "assets": [
            {
                "tag": "AND/666/22",
                "status": "ok",
                "waranty": "done"
            },
            {
                "tag": "AND/134/73",
                "status": "ok",
                "waranty": "done"
            },
        ]
    }
    return assets
