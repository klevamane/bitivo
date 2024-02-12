"""Module with asset categories fixtures """
import random

# Third Party Modules
import pytest

# Database
from api.models.database import db

# Models
from api.models import AssetCategory, Attribute, Asset, Center

# Utilities
from api.schemas.asset_category import AssetCategorySchema


@pytest.fixture(scope='module')
def multiple_categories(app, new_user):
    """
    Create the asset category records for testing
    """
    new_user.save()
    categories = ['Laptop', 'Chromebook', 'Apple']

    for category in categories:
        db.session.add(
            AssetCategory(
                name=category, image={"public_id": "hauvx56khbsyajkziw1c"}))

    db.session.commit()


@pytest.fixture(scope='module')
def new_asset_category(app, init_db, new_user):
    new_user.save()
    params = {
        'name': 'Laptop',
        'image': {
            "public_id": "hauvx56khbsyajkziw1c"
        },
        'created_by': new_user.token_id
    }
    asset_category = AssetCategory(**params)
    return asset_category


@pytest.fixture(scope='module')
def second_asset_category(app, init_db, new_user_three):
    new_user_three.save()
    params = {'name': 'Laptop', 'created_by': new_user_three.token_id}
    asset_category = AssetCategory(**params)
    return asset_category


@pytest.fixture(scope='module')
def new_test_asset_category(app):
    params = {
        'name': 'MacBook Pro',
        'image': {
            "public_id": "hauvx56khbsyajkziw1c"
        }
    }
    asset_category = AssetCategory(**params)
    return asset_category


@pytest.fixture(scope='module')
def asset_categories(app):
    asset_category = AssetCategory.query.filter_by()
    return asset_category


@pytest.fixture(scope='module')
def asset_category_and_schema():
    return {'model': AssetCategory, 'schema': AssetCategorySchema}


@pytest.fixture(scope='module')
def new_asset_category_with_deleted_asset(app, request_ctx,
                                          mock_request_two_obj_decoded_token,
                                          new_space, new_user):
    """
    Fixture for asset category with a deleted child asset.
    """
    from api.models import User
    user = User.query_(include_deleted=True).all()[0]
    user.update_(deleted=False)
    new_user.save()
    new_space.save()
    asset_category = AssetCategory(
        name='Laptop1', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()

    asset = Asset(
        tag='abd',
        asset_category_id=asset_category.id,
        assignee_id=new_space.id,
        assignee_type='space',
        created_by=new_user.token_id)

    asset = asset.save()
    asset.delete()

    return asset_category


@pytest.fixture(scope='module')
def new_asset_category_with_non_deleted_asset(app, new_space):
    """
    The module scope is used here to prevent a test module data leaking into
    another.
    Fixture for asset category with a non deleted child asset.
    """
    new_space.save()
    asset_category = AssetCategory(
        name='Laptop0', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()
    asset = Asset(
        tag='abc',
        asset_category_id=asset_category.id,
        assignee_id=new_space.id,
        assignee_type='space')

    asset = asset.save()

    return asset_category


@pytest.fixture(scope='module')
def test_asset_category(app, new_user):
    asset_category = AssetCategory(
        name='Desktop', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()
    new_user.save()
    attribute_one = Attribute(
        _key='waranty',
        label='waranty',
        is_required=True,
        input_control='Text')
    attribute_two = Attribute(
        _key='length', label='length', is_required=False, input_control='Text')
    asset_category.attributes.append(attribute_one)
    asset_category.attributes.append(attribute_two)

    return asset_category


@pytest.fixture(scope='module')
def test_asset_category_with_custom_fields(app, new_user):
    asset_category = AssetCategory(
        name='Dongles', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()
    new_user.save()
    color_attribute = Attribute(
        input_control="dropdown",
        label="Color",
        is_required=True,
        choices="grey,black",
        _key="color")
    port_attribute = Attribute(
        input_control="checkbox",
        label="port",
        is_required=True,
        choices="usb,usb-c,hdmi,sd",
        _key="port")
    usage_attribute = Attribute(
        input_control="radio button",
        label="usage",
        is_required=True,
        choices="old,new,moderate",
        _key="usage")
    serial_attribute = Attribute(
        input_control="text",
        label="serial number",
        is_required=True,
        _key="serialNumber")
    date_attribute = Attribute(
        input_control="date",
        label="Date of purchase",
        is_required=True,
        _key="DateOfPurchase")

    asset_category.attributes.append(color_attribute)
    asset_category.attributes.append(port_attribute)
    asset_category.attributes.append(usage_attribute)
    asset_category.attributes.append(serial_attribute)
    asset_category.attributes.append(date_attribute)

    return asset_category


@pytest.fixture(scope='module')
def test_single_asset_category(app):
    asset_category = AssetCategory(
        name='AppleTv', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()
    attribute_one = Attribute(
        _key='waranty',
        label='waranty',
        is_required=True,
        choices=['Green', 'Red'],
        input_control='Text')
    attribute_two = Attribute(
        _key='length', label='length', is_required=False, input_control='Text')
    asset_category.attributes.append(attribute_one)
    asset_category.attributes.append(attribute_two)

    return asset_category


@pytest.fixture(scope='module')
def test_single_asset_category2(app):
    asset_category = AssetCategory(
        name='LatestAssets', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()
    attribute_one = Attribute(
        _key='waranty',
        label='waranty',
        is_required=True,
        choices=['Green', 'Red'],
        input_control='Text')
    attribute_two = Attribute(
        _key='length', label='length', is_required=False, input_control='Text')
    asset_category.attributes.append(attribute_one)
    asset_category.attributes.append(attribute_two)

    return asset_category


@pytest.fixture(scope='function')
def sheet_migration_data():
    category_data = {
        'name': 'Test devices',
        'image': {
            "public_id": "hauvx56khbsyajkziw1c"
        }
    }
    center_data = {
        'name': 'Test Center',
        'image': {
            "public_id": "br4mxeqx5zb8rlakpfkm",
            "format": "jpg",
            "url": "https://res.cloudinary.com/"
        }
    }
    asset_category = AssetCategory(**category_data)
    center = Center(**center_data)
    attributes = [
        dict(
            _key='device',
            label='device',
            is_required=True,
            input_control='Text'),
        dict(
            _key='serialNumber',
            label='Serial Number',
            is_required=True,
            input_control='Text'),
        dict(
            _key='assignee',
            label='assigine',
            is_required=True,
            input_control='Text')
    ]
    attributes_instances = []
    for attribute in attributes:
        attribute = Attribute(**attribute)
        attributes_instances.append(attribute)
    return asset_category, center


@pytest.fixture(scope='module')
def new_asset_category_subcategory_asset(app, new_space, new_center, new_user):
    """
        Fixture to create an asset-category, an asset subcategory
        and asset associated with the created asset-category
    """
    new_user.save()
    new_space.save()
    params = {
        'name': 'MacBook',
        'image': {
            "public_id": "hauvx56khbsyajkziw1c"
        }
    }
    asset_category = AssetCategory(**params)
    asset_category.save()
    asset = Asset(
        tag='AND/VET/' + str(random.randint(100, 500)),
        center_id=new_center.id,
        assignee_id=new_space.id,
        assignee_type='space',
        asset_category_id=asset_category.id)
    asset.save()
    sub_category = AssetCategory(
        name="MacBook Pro",
        description="Apple Computer",
        image={"public_id": "hauvx56khbsyajkziw1c"},
        parent_id=asset_category.id)
    sub_category.save()
    asset = Asset(
        tag='AND/VEF/' + str(random.randint(100, 500)),
        center_id=new_center.id,
        assignee_id=new_space.id,
        assignee_type='space',
        asset_category_id=sub_category.id)
    asset.save()
    return asset_category


@pytest.fixture(scope='module')
def new_asset_category_with_one_asset(app, new_space):
    """
    The module scope is used here to prevent a test module data leaking into
    another.
    Fixture for asset category with a non deleted child asset.
    """
    new_space.save()
    asset_category = AssetCategory(
        name='Laptop0', image={"public_id": "hauvx56khbsyajkziw1c"})
    asset_category = asset_category.save()
    asset = Asset(
        tag='cbd',
        asset_category_id=asset_category.id,
        assignee_id=new_space.id,
        assignee_type='space')

    asset = asset.save()

    return asset_category
