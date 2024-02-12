""" Module with user model schemas. """

# Third Party
from marshmallow import (fields, post_load)

# Validators
from ..utilities.validators.validate_id import id_validator
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.status_validator import validate_status
from ..utilities.validators.email_validator import email_validator
from ..utilities.validators.url_validator import url_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.user_validator import UserValidator

# Helpers
from ..utilities.helpers.schemas import common_args

# Schemas
from .base_schemas import AuditableBaseSchema


class UserSchema(AuditableBaseSchema):
    """ User model schema. """
    name = fields.String(
        **common_args(validate=(string_length_validator(60), name_validator)))
    email = fields.String(**common_args(validate=email_validator))
    status = fields.String(validate=validate_status, load_only=True)
    status_dump = fields.Method('get_status_value', dump_to='status')
    image_url = fields.String(
        **common_args(validate=url_validator),
        load_from='imageUrl',
        dump_to='imageUrl')
    role_id = fields.String(
        load_from='roleId', load_only=True, validate=id_validator)
    center_id = fields.String(
        load_from='centerId',
        load_only=True)
    token_id = fields.String(
        load_from='tokenId',
        dump_to='tokenId',
        **common_args(validate=id_validator))
    role = fields.Nested(
        'RoleSchema',
        dump_only=True,
        only=['id', 'title', 'description', 'resource_access_levels'])
    center = fields.Nested(
        'CenterSchema', only=['id', 'name', 'image', 'user_count'])

    @post_load
    def validate_fields_against_db(self, data):
        """
        Ensure id fields reference existing resource
        and email supplied is not owned by an exising user

        Arguments:
            data (dict): request body

        Raises:
            ValidationError: Used to raise exception if request body is empty
        """
        # Convert certain fields to lower case
        self.to_lower(data, ['status', 'email'])

        UserValidator.validate(data)

    def get_status_value(self, obj):
        """Returns the value of status retrieved from database"""
        return obj.status.value

    def to_lower(self, data, keys):
        """
        Converts fields in data to lower case

        Arguments:
            data (dict): request body
            keys (list): list of keys
        """

        for k in keys:
            if data.get(k):
                data[k] = data.get(k).lower()
