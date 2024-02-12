""" Module with user model schemas. """

# Third Party
from marshmallow import (fields, post_load)

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.email_validator import email_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.sheet_transformer_validator import validate_doc_name

# Helpers
from ..utilities.helpers.schemas import common_args

# Schemas
from .base_schemas import AuditableBaseSchema


class SheetTransformerSchema(AuditableBaseSchema):
    """Asset Transformer Schema. """
    doc_name = fields.String(
        **common_args(validate=(string_length_validator(60), name_validator, validate_doc_name)))
    email = fields.String(**common_args(validate=email_validator))
    