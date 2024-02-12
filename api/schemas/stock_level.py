"""Module for stock level"""
# Third Party
from marshmallow import fields

# Schemas
from .asset_category import AssetCategorySchema
from .stock_count import StockLevelCountSchema

# models
from api.models import StockCount, AssetCategory


class StockLevelSchema(AssetCategorySchema):
    """Schema extending the asset category schema to include the stock count"""

    name = fields.String(dump_to='name')
    stock_count = fields.Method('get_stock_counts', dump_to='stockCount')
    running_low = fields.Integer(dump_to='runningLow')
    low_in_stock = fields.Integer(dump_to='lowInStock')
    priority = fields.String(dump_to='priority')
    expected_balance = fields.Method('get_expected_balance', dump_to='expectedBalance')

    def get_stock_counts(self, obj):
        """Returns the asset category stock count"""

        # gets the stock count for each category within the given context
        record = AssetCategory.get(obj.id).stock_counts.filter(StockCount.deleted == False) \
                .filter(StockCount.created_at
                    .between(self.context['start_date'],
                             self.context['end_date']))\
            .order_by(StockCount.created_at.desc()).first()

        # instantiating the schema
        schema = StockLevelCountSchema(only=['count'])

        # serializing the record
        data = schema.dump(record).data
        return data['count'] if 'count' in data else 0

    def get_expected_balance(self, obj):
        """Get the expected balance of stock count"
            Args:
                obj(RowProxy) :  a tuple representing a single SQLAlchemy result

            Returns: expected balance(Integer): An Integer of expected balance

        """
        # get total assigned assets
        total_assigned = obj.space_assignee + obj.people_assignee
        # get expected balance of stock
        expected_balance = obj.total_ok_assets - total_assigned
        return expected_balance
