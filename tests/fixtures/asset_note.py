""" Module for asset note fixtures """

# Third Party Module
import pytest

# Mock
from unittest.mock import Mock

# models
from api.models import AssetNote


@pytest.fixture(scope='module')
def new_asset_note(init_db, new_asset_for_asset_note, new_user):
    """ Fixture for a new asset note """
    new_user.save()
    new_asset_for_asset_note.save()
    return AssetNote(
        title='',
        body='',
        asset_id=new_asset_for_asset_note.id,
        created_by=new_user.token_id)


@pytest.fixture(scope='module')
def asset_note_for_delete(init_db, new_asset_for_asset_note, new_user):
    """ Fixture for a new asset note """
    new_user.save()
    new_asset_for_asset_note.save()
    return AssetNote(
        title='to delete',
        body='some little little confirmation',
        asset_id=new_asset_for_asset_note.id,
        created_by=new_user.token_id)
