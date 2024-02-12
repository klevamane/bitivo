"""Module for asset supporting document resource."""

# Flask
from flask_restplus import Resource
from flask import request

from api.utilities.swagger.collections.asset import (
    supporting_document_namespace, asset_namespace)
from api.utilities.swagger.swagger_models.asset import supporting_documents_model

# Models
from api.models import AssetSupportingDocument, Asset

# Middlewares
from api.middlewares.token_required import token_required

# Schemas
from ..schemas.asset_supporting_document import AssetSupportingDocumentSchema
from ..schemas.asset import AssetSchema

# Validators
from ..utilities.validators.validate_form_data_request import validate_form_data_request, validate_document_type
from api.utilities.validators.validate_id import validate_id
from api.utilities.validators.validate_file_type import allowed_file

# utilities
from ..utilities.constants import EXCLUDED_FIELDS, REDUNDANT_FIELDS
from ..utilities.helpers.endpoint_response import get_success_responses_for_post_and_patch
from ..tasks.cloudinary.cloudinary_file_handler import FileHandler
from ..utilities.enums import AssetSupportingDocumentTypeEnum
from ..utilities.error import raises
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
# Resources
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@supporting_document_namespace.route('/<string:document_id>')
class DeleteAssetSupportingDocumentResource(Resource):
    """
    Resource class for deleting asset's
    supporting document
    """

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def delete(self, document_id):
        """
        A method for deleting an asset supporting document
        """
        return delete_by_id(AssetSupportingDocument, document_id,
                            'Asset supporting document')


@asset_namespace.route('/<string:asset_id>/documents')
class AssetSupportingDocumentResource(Resource):
    """Resource class for asset supporting document endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_form_data_request
    @validate_document_type
    @asset_namespace.expect(supporting_documents_model)
    def post(self, asset_id):
        """
        Endpoint to create an asset's supporting document.
         Args:
            asset_id (string): id for the asset
            request (object): request object
         Returns:
            reponse (dict): response data
        """

        document_type = request.form.get('documentType').replace(" ", "_")
        document_name = request.form.get('documentName')
        file = request.files.get('document')

        if not file:
            raises('required_field', 400, 'document')

        if not allowed_file(file.filename):
            raises('invalid_file_type', 400, 'document')

        request_data = {
            'documentName': document_name,
            'documentType': AssetSupportingDocumentTypeEnum[document_type],
            'assetId': asset_id,
        }
        exclude = EXCLUDED_FIELDS.copy()
        exclude.extend(REDUNDANT_FIELDS)
        asset_supporting_document_schema = AssetSupportingDocumentSchema(
            exclude=exclude)
        asset_supporting_document = asset_supporting_document_schema.load_object_into_schema(
            request_data)

        document = FileHandler.upload_file(file)

        asset_supporting_document = AssetSupportingDocument(
            **asset_supporting_document, document=document)
        asset_supporting_document = asset_supporting_document.save()
        response, status_code = get_success_responses_for_post_and_patch(
            asset_supporting_document,
            asset_supporting_document_schema,
            'Asset Supporting Document',
            status_code=201,
            message_key='created')

        return response, status_code

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def get(self, asset_id):
        """Endpoint to get all supporting documents for an asset"""

        Asset.get_or_404(asset_id)
        exclude = EXCLUDED_FIELDS.copy()
        exclude.extend(REDUNDANT_FIELDS)

        schema = AssetSupportingDocumentSchema(exclude=exclude, many=True)
        documents = schema.dump(AssetSupportingDocument.query_().filter_by(
            asset_id=asset_id).all()).data

        return {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['fetched'].format('Asset supporting documents'),
            'data': {
                'documents': documents,
            }
        }, 200
