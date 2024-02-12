"""Module for export stock level"""
# Third Party
from marshmallow import fields

# Schemas
from .stock_level import StockLevelSchema


class ExportStockLevelSchema(StockLevelSchema):
    """Schema extending the stock level schema"""

    name = fields.String(dump_to='Name')
    stock_count = fields.Method('get_stock_counts', dump_to='Stock Count')
    running_low = fields.Integer(dump_to='Running Low')
    low_in_stock = fields.Integer(dump_to='Low In Stock')

    class Meta:
        fields = ['name', 'stock_count', 'running_low', 'low_in_stock']
        ordered = True

