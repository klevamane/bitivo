"""Module for permission schema"""
# third party
from marshmallow import fields

# Schema
from .base_schemas import AuditableBaseSchema


class HistorySchema(AuditableBaseSchema):
    """History model schema
    """

    resource_id = fields.String(dump_to="resourceId")
    resource_type = fields.String(dump_to="resourceType")
    actor = fields.Nested(
        'UserSchema',
        only=['token_id', 'name'],
    )
    action = fields.String()
    activity = fields.String()
