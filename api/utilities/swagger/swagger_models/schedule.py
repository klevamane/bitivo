"""
Model Definition for schedule collection
"""

from flask_restplus import fields

from ..collections.schedule import schedule_namespace

schedule_model = schedule_namespace.model(
    "schedule_model", {
        'work_order_id': fields.String(
            required=True, description='work order id'),
        'assignee_id': fields.String(
            required=True, description='assignee id'),
        'due_date': fields.String(
            required=True, description='due date'),
        'status': fields.String(
            required=True, description='status'),
        'attachment': fields.String(
            required=True, description='attachments')
    }
)
