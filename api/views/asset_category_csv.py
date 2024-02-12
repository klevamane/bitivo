"""Asset categories csv data resource module"""

from datetime import date

import flask_excel as excel
from flask import request
from flask_restplus import Resource

from api.utilities.swagger.collections.asset import asset_categories_namespace
from ..middlewares.token_required import token_required
from ..models.asset_category import AssetCategory
# Resourses
from ..middlewares.permission_required import Resources
# Permissions
from ..middlewares.permission_required import permission_required


@asset_categories_namespace.route('/export')
class ExportAssetCategories(Resource):
    """
    Resource class for asset categories csv data files
    """

    @token_required
    @permission_required(Resources.ASSET_CATEGORIES)
    def get(self):
        """Download asset categories with their assets count"""

        asset_categories = AssetCategory.query_(request.args).all()
        column_names = ['name', 'assets_count']

        return excel.make_response_from_query_sets(
            asset_categories,
            column_names,
            'csv',
            file_name=f'Asset Categories Export - {date.today()}')
