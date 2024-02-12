"""
Asset categories endpoints helpers
"""

# Third Party Library
from sqlalchemy import text
from sqlalchemy.orm import column_property
from flask import request
from werkzeug.datastructures import ImmutableMultiDict

# Database
from api.models.database import db

# Model
from api.models import AssetCategory

# Utilities
from ..sql_queries import sql_queries
from ..sql_constants import start, end
from ..paginator import (generate_metadata, pagination_helper)
from api.utilities.helpers.resource_manipulation import get_all_resources
from ...schemas.asset_category import (
    AssetCategorySchema, EagerLoadAssetCategoryAttributesSchema,
    AssetReconciliationStatsSchema, AssetCategoryStatsSchema,
    AttributesAndStatsSchema)
from ..validators.sorting_order_by_validator import validate_order_by_args
from ..validators.sorting_column_validator import validate_sort_column
from ..enums import AssetStatus
from ..query_parser import QueryParser
from api.utilities.helpers.pagination_conditional import should_resource_paginate
from ..sql_dynamic_filter import SQLDynamicFilter
from api.utilities.helpers.resource_manipulation_for_delete import delete_by_id
from .add_center_to_sql import add_center_to_query


def asset_categories(include_deleted=False):
    """Get list of asset categories and pagination meta

    Returns:
        tuple: a tuple of data and pagination meta
    """
    return pagination_helper(
        AssetCategory, AssetCategorySchema, include_deleted=include_deleted,
        extra_query={'parent_id': None})


def sideload_with_attributes(include_deleted=False):
    """Sideload asset categories with custom attributes

    Returns:
        tuple: a tuple of data and pagination meta
    """
    return pagination_helper(
        AssetCategory,
        EagerLoadAssetCategoryAttributesSchema,
        include_deleted=include_deleted,
        extra_query={'parent_id': None})


def sideload_with_stats():
    """Sideload asset categories with stats

    Returns:
        tuple: a tuple of data and pagination meta
    """
    sql = sql_queries['categories_with_stats']

    return process_query(sql, AssetCategory, AssetCategoryStatsSchema)


def sideload_with_attributes_and_stats():
    """Sideload asset categories with attributes and stats

    Returns:
        list: list of asset categories
    """
    sql = sql_queries['attributes_and_stats']

    return process_query(sql, AssetCategory, AttributesAndStatsSchema)


def get_single_asset_category_stats(id):

    # get sql query text
    sql = add_center_to_query(sql_queries['single_category_stats'])

    record = db.engine.execute(text(sql), cat_id=id).fetchone()

    # serialize records with schema
    data = AssetCategoryStatsSchema().dump(record).data

    return data


def unreconciled_asset_report(**kwargs):
    """
    Returns the return value of the process_query function

    Args:
        kwargs (dict): key word arguments

    Returns:
        tuple: a tuple of sql data and pagination meta
    """
    sql = sql_queries['unreconciled_asset']
    return process_query(sql, AssetCategory, AssetReconciliationStatsSchema,
                         **kwargs)


def process_query(sql, model, schema, **kwargs):
    """Returns sql data and pagination meta

    Executes raw sql to return list asset
    categories and pagination meta data

    Args:
        sql (str): the sql string to be executed
        schema (class): the schema for serialization
        of records returned from the database

    Returns:
        tuple: a tuple of sql data and pagination meta
    """
    request_args_copy = request.args
    if kwargs.get('skip_filter', False):
        request.args = ImmutableMultiDict([])
    filter = SQLDynamicFilter(model) \
        .sql_query_filter(request.args)
    # get query parameters
    sort, order = get_sort_args()

    # get sql query text
    sql = add_center_to_query(sql)
    sql = text(
        sql.format(
            filter=filter,
            sort=sort,
            order=order,
            startDate=kwargs.get('startDate', start),
            endDate=kwargs.get('endDate', end)))

    sql_count = text(sql_queries['asset_categories_count'])

    # get full count of asset categories
    full_count = db.engine.execute(sql_count).fetchone().count

    # get pagination meta data
    request.args = request_args_copy
    limit, offset, pagination_meta = generate_metadata(full_count)
    params = {'limit': limit, 'offset': offset}
    records = db.engine.execute(sql, **params).fetchall()
    data = schema(many=True).dump(records).data

    return data, pagination_meta


def get_sort_args():
    """Get sort args

        Returns:
            (tuple): A tuple of sorting column
            and order
    """

    valid_columns = [
        'id', 'name', 'assets_count', 'running_low', 'low_in_stock',
        'created_at'
    ]
    sort_column = QueryParser.to_snake_case(
        request.args.get('sort', 'created_at'))

    sort = validate_sort_column(sort_column, valid_columns)
    order = validate_order_by_args(request.args.get('order', 'desc'))

    return sort, order


def map_asset_categories_data(key):
    """Maps a key to response data

        Args:
            key (str): key to map tuple

        Returns:
            (func): a function that will be called to return data
            for the asset categories endpoints sideloaded with stats
    """

    data = {
        'attributes': sideload_with_attributes,
        'single_stats': get_single_asset_category_stats,
        'stats': sideload_with_stats,
        'attributes_stats': sideload_with_attributes_and_stats,
    }

    return data.get(key, asset_categories)


def delete_asset_handler(subcategory_id):
    """
    This method handles deletion of a subcategory assets
    Args:
    subcategory_id (str): The id of the subcategory
    """
    assets = AssetCategory.get(subcategory_id).assets.all()
    for asset in assets:
        if asset.deleted is False:
            delete_by_id(asset, asset.id, '')


def sub_category_handler(data, asset_category_id, schema, model):
    """ Handle asset subcategory update
    Args:
        data (dict): asset subcategory data
        asset_category_id (str): asset category id
        schema (instance): schema object
        model (instance): model object
    Return:
        None
    """
    sub_category_ = schema.load_object_into_schema(
        data)
    if data.get('id'):
        sub_ = model()
        sub = sub_.get_or_404(data['id'])
        sub.update_(**sub_category_)
    else:
        sub_category_.update({'parent_id': asset_category_id})
        sub_category_ = model(**sub_category_)
        sub_category_.save()
