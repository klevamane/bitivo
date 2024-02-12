"""Contains functions for seeding assets to the database

Example:
    These data can be seeded using the following flask command::

        $ flask seed asset
"""
# third party
from datetime import datetime

# Models
from api.models import Asset, Space

# Database
from api.models.database import db

# Enums
from api.utilities.enums import AssetStatus

# Utilities
from api.utilities.helpers.seeders import clean_seed_data

# Seed data
from .seed_data import get_env_based_data


def seed_asset(clean_data=False):
    """Seeds assets to the database

    Args:
        clean_data (bool): Determines if seed data is to be cleaned.

    Returns:
        None
    """
    assets = get_env_based_data('asset')

    asset_tags_list = [asset[0] for asset in assets]
    if not clean_data:
        # List of asset tags not already existing in the DB.
        asset_tags_list = clean_seed_data('asset', asset_tags_list, True)

    # Creates new assets list without already existing entries.
    cleaned_assets = []
    for asset in assets:
        if asset[0] in asset_tags_list:
            cleaned_assets.append(asset)

    save_assets(cleaned_assets)


def save_assets(assets):
    """Saves asset objects in a list persistently

    Args:
        assets (list): List of objects to save

    Returns:
        None
    """
    space = Space.query_()[1]
    asset_instances = []

    # create list of statuses to be seeded for each asset
    statuses = [item.value for item in AssetStatus]
    count = 0
    for asset in assets:
        asset_instances.append(
            Asset(
                tag=asset[0],
                asset_category_id=asset[1].id,
                center_id=asset[2].id,
                assignee_id=space.id,
                assignee_type='space',
                custom_attributes=asset[3],
                status=statuses[count],
                date_assigned=date_assign(statuses[count])))
        # increment count else restart from zero
        count = count + 1 if count < len(statuses) - 1 else 0

    db.session.add_all(asset_instances)
    db.session.commit()


def date_assign(status):
    return datetime.now()
