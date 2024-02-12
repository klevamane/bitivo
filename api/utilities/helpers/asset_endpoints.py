"""Module for asset endpoints helpers."""
from ...schemas.asset import AssetSchema
from ..constants import EXCLUDED_FIELDS


def create_asset_response(asset_instance, message, handle_many=False):
    """Helper function to create a response after asset operations

    :param asset_instance: An single asset instance or a collection of asset
                           instances in a query object
    :type asset_instance: SQLAlchemy query object
    :param message: Message to be passed with the response
    :type message: string
    :param handle_many: Flag to let the function know whether to handle a
                        single instance or a collection, defaults to False
    :param handle_many: bool, optional
    """

    exclude = EXCLUDED_FIELDS.copy()
    exclude.remove('updated_by')
    schema = AssetSchema(many=handle_many, exclude=exclude)

    response = {
        "status": "success",
        "message": message,
        "data": schema.dump(asset_instance).data
    }

    return response


def create_asset_category_struct(asset_category):
    """Helper function to create a data structure of the asset category's
    attributes to validate the request's asset attributes against

    :param asset_category: model instance of the asset's asset category
    :type asset_category: SQLAlchemy model object
    """

    asset_category_attrs = dict()
    for attr in asset_category.attributes.all():
        asset_category_attrs[attr._key] = {  #pylint: disable=W0212
            'is_required': attr.is_required,
            'choices': attr.choices
        }

    return asset_category_attrs
