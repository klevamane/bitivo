"""
Model Definition for work order collection
"""
from flask_restplus import fields
from ..collections.work_order import work_order_namespace

work_order_model = work_order_namespace.model(
    "work_order_model", {
        'title': fields.String(required=True,
                               description="title of the work order"),
        'description': fields.String(required=True,
                                     description="description of the \
                                     work order"),
        'centerId': fields.String(required=True, description="id of center"),
        'assigneeId': fields.String(required=True,
                                    description="token id of an assignee"),
        'maintenanceCategoryId': fields.String(required=True,
                                               description="id of maintenance \
                                                category"),
        'frequency': fields.String(required=True,
                                   description="frequency type for work \
                                            order"),
        'frequencyUnits': fields.Integer(required=True,
                                         description="frequency unit for work \
                                              order"),
        'startDate': fields.String(required=True,
                                   description="work order start date"),
        'endDate': fields.String(required=True,
                                 description="work order end date")
    }
)
