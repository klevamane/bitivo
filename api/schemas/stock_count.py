"""Module for the stock count schema"""

# Standard library
from datetime import datetime as dt
from itertools import groupby

# Third party
from marshmallow import fields, validates_schema, post_load

# Schemas
from .asset_category import AssetCategorySchema
from .base_schemas import AuditableBaseSchema

# Helpers
from ..utilities.helpers.schemas import common_args

# Validators
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.stock_count_validators import StockCountValidator


class StockCountSchema(AuditableBaseSchema):
    """Stock count model schema"""

    asset_category = fields.Nested(
        AssetCategorySchema,
        dump_only=True,
        dump_to='assetCategory',
        only=['id', 'name'])

    asset_category_id = fields.String(
        **common_args(validate=StockCountValidator.validate_asset_category_id),
        load_from='assetCategoryId',
        load_only=True)

    count = fields.Integer(required=True, load_only=True)
    week = fields.Integer(required=True, load_only=True)

    weeks = fields.Dict(dump_only=True)

    token_id = fields.String(
        **common_args(validate=id_validator),
        load_only=True,
        load_from='tokenId')

    center_id = fields.String(
        **common_args(validate=id_validator),
        load_from='centerId',
        load_only=True)

    last_stock_count = fields.Date(
        format='dd-mm-yyyy', dump_only=True, dump_to='lastStockCount')

    week = fields.Integer(
        **common_args(validate=StockCountValidator.validate_week),
        load_only=True)
    count = fields.Integer(
        **common_args(validate=StockCountValidator.validate_count),
        load_only=True)

    @post_load
    def validate_weeks(self, data):
        """Validates for different week values.

        Ensures only stock count values for the same week can be added at a time.

        Args:
            data (dict): Dict holding serialised obj

        Returns:
            None
        """
        StockCountValidator.validate_different_weeks(
            self.context.get('week_list'))

    @validates_schema
    def validate_record_not_existing(self, data):
        """Validates that a record does not already exist.

        Checks whether the stock count record for the asset category
        for that month and year already exists in the database.

        Args:
            data (dict): Request body data.

        Returns:
            None
        """

        week = data.get("week")
        asset_category_id = data.get("asset_category_id")
        if week and asset_category_id:
            month = dt.now().month
            year = dt.now().year
            StockCountValidator.validate_duplicate_stock_count(
                week, asset_category_id, month, year)

        # Validates for any asset category ID duplicates
        StockCountValidator.validate_asset_category_duplicate(
            data, self.context.get('asset_category_id_set', set()))

    @staticmethod
    def _grouper(item):
        """Helper method for grouping items

        This method is used as the key to the `groupby` function.

        Args:
            item (StockCount): The item to be grouped

        Returns:
            tuple: A tuple containing the keys used to group the items
        """
        return (
            item.created_at.year,
            item.created_at.month,
            item.asset_category_id,
            item.asset_category.name,
        )

    @staticmethod
    def format_output(query_result):
        """Generator method for formatting output

        Formats the output into the required form. It groups items from the
        query result by asset category and year and month

        Args:
            query_result (BaseQuery): The query results

        Examples:
            output = [data for data in schema.format_output(query_result)]

        Yields:
            dict: the formatted output in dictionary form
        """
        sorted_query = sorted(
            query_result, key=StockCountSchema._grouper, reverse=True)
        grouped = groupby(sorted_query, StockCountSchema._grouper)
        for (year, month, id_, name), weeks in grouped:
            week_list = list(weeks)
            yield {
                'category': {
                    'id': id_,
                    'name': name
                },
                'weeks': {
                    week.week: {
                        'date': str(week.created_at),
                        'count': week.count,
                        'id': week.id
                    }
                    for week in week_list
                },
                # set the latest date as the last stock count date
                'lastStockCount':
                '{}'.format(
                    str(
                        max(week_list,
                            key=lambda item: item.created_at).created_at)),
                'control':
                week_list[0].asset_category.priority.value.title()
            }


class StockLevelCountSchema(StockCountSchema):
    """Extends the the stock count schema to modify the count field"""

    # modifies the count field to dump_only
    count = fields.Integer(dump_only=True)
