"""
Module for testing asset status activity tracker
"""
from flask import request

# models
from api.models import History
from api.models.database import db

# Utilities
from api.utilities.history.asset_status_activity import asset_status_activity_on_repair_log
from api.utilities.enums import AssetStatus


def test_asset_status_activity_on_repair_log(init_db, new_user, new_asset, request_ctx,
                                             mock_request_obj_decoded_token, mock_request_two_obj_decoded_token):
    """
    Test asset_status_activity inserts into the history table.

    Args:
        init_db (SQLAlchemy): fixture to initialize the test database
        request_ctx (object): request client context
        auth_header (dict): fixture to get token
        mock_request_obj_decoded_token (object): Mock decoded_token from request object
        new_user (dict): fixture to create a new user
        new_asset (dict): fixture to create a new asset
    """

    actor = request.decoded_token['UserInfo']
    new_user.name, new_user.token_id = actor['name'], actor['id']

    new_user.save()

    asset_status_activity_on_repair_log(
        new_asset.id, new_asset.status, db.session)

    history = History.query_().filter_by(resource_id=new_asset.id).first()

    assert history.action == 'edit'
    assert history.activity == f"status changed from {new_asset.status} to {AssetStatus.IN_REPAIRS.value} by {actor['name']}"
