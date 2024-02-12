"""Contains functions for seeding asset categories and attributes to the db

Example:
    These data can be seeded using the following flask command::

        $ flask seed asset_category
"""

# Third party
from humps.camel import case

# Models
from api.models import AssetCategory, Attribute

# Database Instance
from api.models.database import db

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data


def seed_asset_category(clean_data=False):
    """Creates asset categories and corresponding custom attributes

    This seeds asset categories to the database and adds corresponding
    custom attributes.

    Args:
        clean_data (bool): Determines if seed data is to be cleaned.

    Returns:
        None
    """

    asset_category_data = get_env_based_data('asset_category')[
        'asset_category']

    if not clean_data:
        asset_category_data = clean_seed_data('asset_category',
                                              asset_category_data)

    asset_categories = [
        AssetCategory(name=category['name'])
        for category in asset_category_data
    ]

    # Add relevant asset categories to the database
    for asset_category in asset_categories:
        db.session.add(asset_category)
    db.session.commit()

    # Create all the attributes associated with asset categories
    create_attributes(asset_categories, asset_category_data)


def create_attributes(asset_categories, asset_category_data):
    """Creates multiple attributes under respective asset category

    Args:
        asset_categories (list): a list of asset categories saved to the
            database
        asset_category_data (list): a list of asset category data gotten from
            file

    Returns:
        None
    """

    for i, item in enumerate(asset_category_data):
        for attribute in item['attributes']:
            db.session.add(
                Attribute(
                    _key=case(attribute[0]),
                    label=attribute[0],
                    is_required=attribute[1],
                    input_control='text',
                    asset_category_id=asset_categories[i].id,
                ))

    # Commit attributes
    db.session.commit()
