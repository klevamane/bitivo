"""Module that handles asset-notes operations"""
# Third-party libraries
from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.asset import (asset_namespace,
                                                     asset_note_namespace)
from api.utilities.swagger.swagger_models.asset import asset_note_model

from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..models import AssetNote
from ..models import Asset

# schema
from ..schemas.asset_note import AssetNoteSchema
from ..schemas.asset import AssetSchema

# middlewares
from ..middlewares.token_required import token_required

# validators
from ..utilities.validators.validate_id import validate_id
from ..utilities.validators.validate_json_request import validate_json_request

# Helpers
from ..utilities.constants import EXCLUDED_FIELDS, REDUNDANT_FIELDS
from ..utilities.helpers.endpoint_response import (
    get_success_responses_for_post_and_patch)
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_namespace.route('/<string:asset_id>/notes')
class AssetNoteResource(Resource):
    """Resource class for asset note endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_json_request
    @asset_namespace.expect(asset_note_model)
    def post(self, asset_id):
        """Endpoint to create an asset note."""

        request_data = request.get_json()
        request_data['assetId'] = asset_id

        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        asset_note_schema = AssetNoteSchema(exclude=excluded)
        asset_note_data = asset_note_schema.load_object_into_schema(
            request_data)
        asset_note = AssetNote(**asset_note_data)
        asset_note.save()

        return get_success_responses_for_post_and_patch(
            asset_note,
            asset_note_schema,
            'Asset note',
            status_code=201,
            message_key='created')

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def get(self, asset_id):
        """Endpoint to get all notes for an asset"""

        Asset.get_or_404(asset_id)
        notes_excluded_fields = EXCLUDED_FIELDS.copy()
        notes_excluded_fields.extend(REDUNDANT_FIELDS)
        asset_note_schema = AssetNoteSchema(
            exclude=notes_excluded_fields, many=True)
        asset_notes = asset_note_schema.dump(
            AssetNote.query_().filter_by(asset_id=asset_id).all()).data

        return {
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Asset notes'),
            'data': asset_notes
        }, 200


@asset_note_namespace.route('/<string:note_id>')
class SingleNoteResource(Resource):
    """Resource class for single asset note endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_json_request
    @asset_note_namespace.expect(asset_note_model)
    def patch(self, note_id):
        """
        An endpoint to update the details of a single asset note
        Args:
            note_id (str): The asset note id
        Returns:
                dict: A dictionary containing the response sent to the user
        """
        request_data = request.get_json()
        asset_note = AssetNote.get_or_404(note_id)
        excluded = EXCLUDED_FIELDS.copy()
        excluded.extend(REDUNDANT_FIELDS)
        asset_note_schema = AssetNoteSchema(exclude=excluded)
        data = asset_note_schema.load_object_into_schema(
            request_data, partial=True)
        asset_note.update_(**data)
        return get_success_responses_for_post_and_patch(
            asset_note,
            asset_note_schema,
            'Asset note',
            status_code=200,
            message_key='updated')

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def delete(self, note_id):
        """ Endpoint to delete an asset note """
        return delete_by_id(AssetNote, note_id, 'Asset note')
