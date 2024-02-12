"""Module that handles asset-related operations"""
# System libraries
import copy
from datetime import datetime

# Third-party libraries
import pyexcel as pe
from flask_restplus import Resource
from flask import request, jsonify, g
from werkzeug.datastructures import ImmutableMultiDict

from api.utilities.swagger.collections.asset import asset_namespace
from api.utilities.swagger.swagger_models.asset import asset_model
from api.utilities.swagger.constants import (
    ASSET_REQUEST_PARAMS, PAGINATION_PARAMS,
    SEARCH_ASSET_BY_DATE_AND_WARRANTY_REQUEST_PARAMS)
from api.models import Asset
from api.utilities.error import raises
from api.middlewares.base_validator import ValidationError
from api.middlewares.token_required import token_required
from ..middlewares.permission_required import permission_required
from ..schemas.asset import (AssetSchema, UpdateAssetSchema)
from ..utilities.constants import EXCLUDED_FIELDS, QUERY_COLUMNS
from ..utilities.helpers.asset_endpoints import (create_asset_response,
                                                 create_asset_category_struct)
from ..middlewares.base_validator import ValidationError
from ..models import User

# Helpers
from ..utilities.helpers.pagination_conditional import should_resource_paginate
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.validators.validate_id import validate_id
from ..utilities.validators.asset_validator import (asset_data_validators)
from ..utilities.validators.asset_custom_attrs_validator import (
    validate_asset_custom_attrs)
from ..utilities.validators.validate_json_request import validate_json_request
from ..utilities.validators.asset_migration_validators import (
    validate_sheet_name_input, migration_get_or_404)
from ..utilities.helpers.get_book import get_book

# schemas
from ..schemas.asset import (AssetSchema, UpdateAssetSchema)

# Helpers
from ..utilities.helpers.resource_manipulation import get_paginated_resource, get_all_resources
from ..utilities.helpers.resource_manipulation_for_delete import delete_by_id
from ..schemas.asset_category import AssetReconciliationStatsSchema
from api.utilities.validators.unreconciled_asset_validator import validate_request_param
from api.utilities.helpers.asset_categories_endpoints import unreconciled_asset_report
from api.middlewares.permission_required import Resources


@asset_namespace.route('/')
class AssetResource(Resource):
    """
    Resource class for carrying out CRUD operations on asset entity
    """

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_json_request
    @asset_namespace.expect(asset_model)
    def post(self):
        """
        An endpoint that creates a new asset in the database
        """
        # asset_data_validators function parses and validates request data
        new_asset = Asset(
            created_by=request.decoded_token['UserInfo']['id'],
            created_at=datetime.utcnow(),
            **asset_data_validators(request, edit=False))
        new_asset.save()

        response = create_asset_response(
            new_asset, message=SUCCESS_MESSAGES['created'].format('Asset'))

        return response, 201

    @token_required
    @asset_namespace.doc(params=ASSET_REQUEST_PARAMS)
    @permission_required(Resources.ASSETS)
    def get(self):
        """
        Gets Lists of all assets
        """

        data, pagination_object = should_resource_paginate(
            request, Asset, AssetSchema)

        return jsonify({
            "status": 'success',
            "message": 'Assets fetched successfully',
            "data": data,
            "meta": pagination_object
        })


@asset_namespace.route('/search')
class SearchAssetResource(Resource):
    """Resource for search assets endpoints."""

    @token_required
    @asset_namespace.doc(
        params=SEARCH_ASSET_BY_DATE_AND_WARRANTY_REQUEST_PARAMS)
    @permission_required(Resources.ASSETS)
    def get(self):
        """
        Search Asset by date and warranty
        """
        qry_keys = ('start', 'end', 'warranty_start', 'warranty_end')
        qry_dict = request.args.to_dict()

        [
            raises('invalid_column', 400, key) for key in qry_dict
            if key not in qry_keys
        ]

        qry_list = [(
            'where',
            f'{QUERY_COLUMNS[key]["column"]},{QUERY_COLUMNS[key]["filter"]},{value}'
        ) for key, value in qry_dict.items()]

        args = ImmutableMultiDict(qry_list)
        assets = Asset.query_(args)

        asset_schema = AssetSchema(many=True, exclude=EXCLUDED_FIELDS)

        return {
            'status': 'success',
            'data': asset_schema.dump(assets).data
        }, 200


@asset_namespace.route('/<string:asset_id>')
class SingleAssetResource(Resource):
    """Resource class for single asset endpoints."""

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    @validate_json_request
    @asset_namespace.expect(asset_model)
    def patch(self, asset_id):
        """Endpoint for patching an asset."""
        asset = Asset.get_or_404(asset_id)
        data = request.get_json()

        # catch null value of center and remove center from asset otherwise
        # serializer schema will reject it

        if 'centerId' in data and data['centerId'] is None:
            del data['centerId']
            asset.center_id = None

        schema = UpdateAssetSchema(context={'asset_id': asset_id})
        data = schema.load_object_into_schema(data, partial=True)

        # check if asset category instance was placed in Flask's g object
        # at the point of asset category validation in the schema
        # otherwise get it from the asset instance backref
        if not g.get('asset_category'):
            asset_category = asset.asset_category
        else:
            asset_category = g.asset_category
            g.pop('asset_category')

        if 'custom_attributes' in data:
            # make a deep copy of the custom attributes in the asset
            # in case of nested dicts
            data = self.format_custom_attributes_in_data(
                data, asset, asset_category)

        # update asset and add update audit info
        asset.update_(updated_at=datetime.utcnow(), **data)

        response = create_asset_response(
            asset, message=SUCCESS_MESSAGES['edited'].format('Asset'))

        return response, 200

    def format_custom_attributes_in_data(self, *args):
        """Validate custom_attributes in data.

        Args:
           *args: Variable length argument list and the mandatory position arguments for this list are:
              data (object): data from an incoming request
              asset_category (instance): Asset category instance
              asset (instance): An asset instance

        """
        data, asset, asset_category = args
        existing_asset_attrs = copy.deepcopy(asset.custom_attributes)
        existing_asset_attrs = existing_asset_attrs if existing_asset_attrs else {}

        asset_category_attrs = create_asset_category_struct(asset_category)

        request_data_keys = list(data['custom_attributes'].keys())

        validated_asset_attrs = validate_asset_custom_attrs(
            request_data_keys, asset_category_attrs, data,
            existing_asset_attrs)

        # replace incoming data's custom attrs with the modified asset's
        # custom attributes
        data['custom_attributes'] = validated_asset_attrs

        return data

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def delete(self, asset_id):
        """ Endpoint to delete an asset"""
        return delete_by_id(Asset, asset_id, 'Asset')

    @token_required
    @permission_required(Resources.ASSETS)
    @validate_id
    def get(self, asset_id):
        """
        Get a single asset
        """

        asset = Asset.get_or_404(asset_id)

        asset_schema = AssetSchema(exclude=EXCLUDED_FIELDS)

        asset_data = asset_schema.dump(asset).data

        return {
            'data': asset_data,
            'status': 'success',
            'message': SUCCESS_MESSAGES['fetched'].format('Asset'),
        }


@asset_namespace.route('/upload')
class AssetMigrationResource(Resource):
    """Resource class for asset migration."""

    @classmethod
    def migration_set_up(cls, request_obj):
        """ sets up the data to be manipulated
         sets up the uploaded file so we can be able to
        access and manipulates its content
         Args:
            request_obj (instance): flasks request instance
         Returns:
             book (list): the data of the sheet to be worked on
        """
        book = get_book(request_obj)
        names = {key.lower(): key for key in book.keys()}
        # access the name passed from the user to be able to
        # access the respective sheet
        sheet_name = request_obj.form.get('sheet_name', '').lower()
        sheet_name = validate_sheet_name_input(sheet_name, book)
        # return the respective sheet with the name provided
        return book[names.get(sheet_name)]

    @token_required
    @permission_required(Resources.ASSETS)
    def post(self):
        """POST method for migrating assets of asset category
         Imports assets from an excel file and saves the records
        the Activo api
         Returns:
            tuple: Success response with 200 status code
        """
        from ..tasks.migration import Migrations

        # Models
        from api.models import AssetCategory, Center

        requester = request.decoded_token['UserInfo']
        assigned_by = request.form.get('assigned_by',
                                       requester['email']).strip()
        assigned_by = User.query_().filter_by(email=assigned_by).first()
        if not assigned_by:
            raise ValidationError({'message': 'assigned_by not found'})
        sheet_data = self.migration_set_up(request)
        name = request.form.get('sheet_name').strip()
        center_name = request.form.get('center_name', '').strip()
        asset_category = migration_get_or_404(name, AssetCategory, 'category')
        center = migration_get_or_404(center_name, Center, 'center')
        category_name = asset_category.name

        Migrations.migrate_assets.delay(requester, sheet_data, {
            'name': category_name,
            'id': asset_category.id
        }, center.id, assigned_by.name)

        return {
            'status':
            'success',
            'message':
            SUCCESS_MESSAGES['asset_migrated'].format('Asset', category_name)
        }, 200


@asset_namespace.route('/reconciliation')
class AssetReconciliationReportResouce(Resource):
    @token_required
    @permission_required(Resources.ASSETS)
    @asset_namespace.doc(params=PAGINATION_PARAMS)
    def get(self):
        """
        Gets list of assets and the corresponding asset count

        """

        parameter = validate_request_param(request)
        parameter['skip_filter'] = True

        data, pagination_meta = unreconciled_asset_report(**parameter)

        return {
            'status': 'success',
            'data': data,
            "meta": pagination_meta
        }, 200
