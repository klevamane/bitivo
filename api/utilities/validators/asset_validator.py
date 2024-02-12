"""Module for validating asset input data"""

# Models
from ...models import AssetCategory, Asset, User

# Schema
from ...schemas.asset import AssetSchema

from flask import request

# Error
from ..error import raises

# Validator
from .validate_id import is_valid_id
from ..validators.allocation_validators import check_target_id


def validate_attributes(asset_category, request_data):
    """Helper function to validate asset customAttributes input data

    Args:
        asset_category (class): AssetCategory  model instance.
        request_data (dict): Holds the asset input data from the request body.
    """
    required_attributes = asset_category.attributes.filter_by(
        is_required=True).all()
    deleted = request.args.to_dict().get('include')
    required_attributes = asset_category.attributes.filter_by(
        is_required=True,
        include_deleted=True
    ).all() if deleted == 'deleted' \
        else required_attributes

    all_attributes = asset_category.attributes.filter_by().all()
    all_attributes = asset_category.attributes.filter_by(include_deleted=True).all() \
        if deleted == 'deleted' else all_attributes
    required_attribute_keys = [
        attribute._key for attribute in required_attributes  # pylint: disable=W0212
    ]
    attribute_keys = [attribute._key for attribute in all_attributes]  # pylint: disable=W0212

    # Check if given attributes invalid
    input_attributes = [key for key in request_data.get('customAttributes')]
    invalid_attributes = set(input_attributes).difference(attribute_keys)
    if invalid_attributes:
        raises('unrelated_attribute', 400, *invalid_attributes)

    # Check if required attributes missing
    missing_required_attributes = set(required_attribute_keys).difference(
        input_attributes)
    if missing_required_attributes:
        missing_required_attributes = ', '.join(missing_required_attributes)
        raises('attribute_required', 400, missing_required_attributes)


def asset_data_validators(request, edit):
    """Data parsing and validation helper for asset POST and PATCH endpoints.

    :param request: The flask request object for the endpoint
    :type request: Flask Request Object

    :param edit: Whether the asset is being edited
    :type edit: bool

    :return: Deserialized and validated asset data from the request body.
    """

    request_data = request.get_json()

    if 'assetCategoryId' not in request_data:
        raises('key_error', 400, 'assetCategoryId')

    if not is_valid_id(request_data['assetCategoryId']):
        raises('invalid_category_id', 400)

    set_center_id_if_none_provided(request, request_data)

    asset_category = AssetCategory.get_or_404(request_data['assetCategoryId'])

    validate_tag(request_data, edit=edit)

    if 'customAttributes' in request_data:
        validate_attributes(asset_category, request_data)

    asset_schema = AssetSchema()

    return asset_schema.load_object_into_schema(request_data)


def set_center_id_if_none_provided(request, request_data):
    """Sets the center id of the asset if none provided

    If the center id is not provided, we use the center id of the user
    creating the asset. If the user does not have a center id, we leave the
    center id of the asset to be null

    Args:
        request (obj): The request object
        request_data (dict): The request data
    """
    if not request_data.get('centerId'):
        user = User.get(request.decoded_token['UserInfo']['id'])
        if user and user.center_id:
            request_data['centerId'] = user.center_id


def validate_tag(request_data, edit):
    """Validates if valid tag value provided.

    Args:
        request_data (dict): Holds the input data from the request body.
        edit (bool): Determines request type, eg. if True then it's PATCH request

    Raises:
        ValidationError: If the tag field is missing, invalid or duplicated.
    """

    if not edit:
        if not request_data.get('tag'):
            raises('attribute_required', 400, 'tag')

        duplicate_asset = Asset.query.filter(
            Asset.tag == request_data.get('tag', None)).first()

        if duplicate_asset:
            raises('duplicate_asset', 409, request_data.get('tag'))


def validate_asset_id(asset_id):
    """Checks whether the asset id is valid and exists

    Args:
        asset_id (str): The asset id

    Return:
        None
    """
    check_target_id(Asset, asset_id, 'invalid_asset_id', 'asset_not_found')
