"""Module for space type schema"""
# Third party libraries
from marshmallow import fields, post_load

# Models
from api.models.space_type import SpaceType

# Schemas
from .base_schemas import AuditableBaseSchema

# Validators
from ..utilities.validators.name_validator import name_validator
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.attributes_validator import validate_attribute

# Helpers
from ..utilities.helpers.schemas import common_args


class SpaceTypeSchema(AuditableBaseSchema):
    """
    Space type model schema
    """
    type = fields.String(**common_args(
        validate=[string_length_validator(60), name_validator]))

    color = fields.String(**common_args(
        validate=[string_length_validator(60), name_validator]))

    spaces = fields.Method('get_spaces')

    def get_spaces(self, obj):
        """Returns the spaces of a space type

        Args:
            obj (class): an instance of the SpaceType model

        Returns:
            (list): a list of spaces in a space type
        """

        from .space import SpaceSchema

        center_id = self.context['center_id']
        only = ('id', 'name', 'space_type', 'parent_id', 'center_id',
                'children_count')

        spaces = obj.spaces.filter_by()

        if center_id:
            spaces = spaces.filter_by(center_id=center_id)

        return SpaceSchema(many=True, only=only).dump(spaces).data

    @staticmethod
    def organize_output(data):
        """Organizes the response data to desired output

        Args:
            data (list): a list of space types with associated spaces

        Returns:
            (tuple): a list of spaces space types and a dict of spaces
        """
        grouped_spaces = {}
        space_types = []

        for space_type in data:
            type_name = space_type['type'].lower() + 's'
            grouped_spaces.update({type_name: space_type['spaces']})
            space_types.append({
                "type": space_type['type'],
                "color": space_type['color'],
                "id": space_type['id']
            })
        return space_types, grouped_spaces

    @post_load
    def validate_type(self, data):
        """
        validate type attribute is not a duplicate
        """
        if 'type' in data:
            validate_attribute(data, 'type', SpaceType)
