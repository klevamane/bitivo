"""
Model Definition for maintenance category collection
"""

from flask_restplus import fields
from ..collections.maintenance_category import maintenance_category_namespace

# swagger model that defines maintenance category fields
maintenance_category_model = maintenance_category_namespace.model(
    "maintenance_category_model", {
        'title': fields.String(
            required=True, description='title of the maintenance category'
        ),
        'assetCategoryId': fields.String(
            required=True, description='id of asset'
        ),
        'centerId': fields.String(
            required=True, description='id of center'
        )
    }
)
