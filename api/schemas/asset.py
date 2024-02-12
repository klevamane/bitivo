""" Module for asset model schema. """
# Third-party libraries
from marshmallow import fields, post_load, pre_load
from itertools import groupby
from datetime import datetime as dt

# Models
from ..models import Asset

# Schemas
from .base_schemas import AuditableBaseSchema
from .user import UserSchema
from .space import SpaceSchema

# Enum
from ..utilities.enums import AssigneeType

from api.models import Space, User

# Validators
from ..utilities.validators.string_length_validators import string_length_validator
from ..utilities.validators.asset_status_validator import validate_asset_status
from ..utilities.validators.asset_category_exists import asset_category_exists
from ..utilities.validators.resource_exists_validator import resource_exists
from ..utilities.validators.update_tag_validator import update_tag_validator
from ..utilities.validators.allocation_validators import \
    (validate_assignee_id, validate_assignee_type,
     validate_space_in_center, validate_id_and_type_both_present,
     validate_id_matches_type)

# Helpers
from ..utilities.helpers.schemas import common_args


class AssetSchemaOperationsHelper:
    """Asset schema Helper"""
    assignee_mapper = {'user': User, 'space': Space, 'store': Space}

    @staticmethod
    def is_a_store(assignee, assignee_type):
        """Asset assignee store type checker

            Args:
                assignee (Asset): The Asset object
                assignee_type (Asset): The Asset object

            Returns:
                boolean: True or False
        """
        store_type = AssigneeType.store.value.lower()
        return isinstance(
            assignee,
            Space) and (assignee_type == store_type
                        or assignee.space_type.type.lower() == store_type)

    @classmethod
    def load_assignee_type(cls, obj):
        """Load the asset assignee type

            Args:
                obj (Asset): The Asset object

            Returns:
            str: The Assignee type
        """
        assignee_type = obj['assignee_type'].lower()
        assignee = cls.assignee_mapper[assignee_type].get(obj['assignee_id'])
        if cls.is_a_store(assignee, assignee_type):
            assignee_type = AssigneeType.store.value
        obj['date_assigned'] = dt.now()
        return assignee_type


class AssetSchema(AuditableBaseSchema):
    """Asset model schema"""

    tag = fields.String(**common_args(validate=string_length_validator(60)))

    custom_attributes = fields.Dict(
        load_from="customAttributes", dump_to="customAttributes")

    asset_category_id = fields.String(
        **common_args(validate=string_length_validator(60)),
        load_from="assetCategoryId",
        dump_to="assetCategoryId")

    center_id = fields.String(
        load_from="centerId",
        dump_to="centerId",
        validate=[string_length_validator(60), resource_exists])

    assignee_id = fields.String(
        load_only=True,
        load_from="assigneeId",
        **common_args(validate=validate_assignee_id))

    assignee_type = fields.String(
        load_from="assigneeType",
        **common_args(validate=validate_assignee_type),
        load_only=True)

    assignee_type_dump = fields.Method(
        'get_assignee_type', dump_to="assigneeType")

    assigned_by = fields.String(dump_only=True, dump_to='assignedBy')

    date_assigned = fields.Method(
        'parse_date_assigned', dump_to='dateAssigned', dump_only=True)

    status = fields.String(validate=validate_asset_status)

    assignee = fields.Method("get_assignee", dump_only=True)

    def parse_date_assigned(self, obj):
        return obj.date_assigned.date().strftime('%Y-%m-%d') if (
            obj.date_assigned) else ''

    def get_assignee_type(self, obj):
        """Get the assignee type object

        Args:
            obj (Asset): The Asset object

        Returns:
            str: The Assignee type
        """
        assignee_mapper = AssetSchemaOperationsHelper.assignee_mapper

        assignee = assignee_mapper[obj.assignee_type.value].get(
            obj.assignee_id)
        assignee_type = obj.assignee_type.value
        if AssetSchemaOperationsHelper.is_a_store(assignee, assignee_type):
            assignee_type = AssigneeType.space.value
        return assignee_type

    def get_assignee(self, obj):
        """Get the assignee object

        Gets the asset's assignee object and serializes it using the
        appropriate schema

        Args:
            obj (Asset): The Asset object

        Returns:
            dict: The serialized assignee details
        """
        assignee_types = {
            'space': (SpaceSchema, ('id', 'name', 'space_type')),
            'user': (UserSchema, ('token_id', 'name', 'email', 'role.id',
                                  'role.title', 'role.description')),
            'store': (SpaceSchema, ('id', 'name', 'space_type'))
        }
        schema, only = assignee_types.get(obj.assignee_type.name)
        return schema(only=only).dump(obj.assignee).data

    @post_load
    def validate_space_assignee_in_center_provided(self, data):
        """Validates that the space is in the asset's center
        Also validates that the assignee id and type match
        Args:
            data (dict): The request data
        """
        validate_id_matches_type(data)
        validate_space_in_center(data)
        if 'assignee_type' in data:
            data[
                'assignee_type'] = AssetSchemaOperationsHelper.load_assignee_type(
                    data)


class UpdateAssetSchema(AuditableBaseSchema):
    """Update asset model schema"""

    tag = fields.String(
        validate=[string_length_validator(60), update_tag_validator])

    custom_attributes = fields.Dict(
        load_from="customAttributes", dump_to="customAttributes")

    asset_category_id = fields.String(
        load_from="assetCategoryId",
        dump_to="assetCategoryId",
        validate=[string_length_validator(60), asset_category_exists])

    center_id = fields.String(
        load_from="centerId",
        dump_to="centerId",
        validate=[string_length_validator(60), resource_exists])

    status = fields.String(validate=validate_asset_status)

    assignee_id = fields.String(
        load_from="assigneeId", load_only=True, validate=validate_assignee_id)

    assignee_type = fields.String(
        load_from='assigneeType',
        dump_to="assigneeType",
        validate=validate_assignee_type)

    assigned_by = fields.String(dump_only=True, dump_to='assignedBy')

    date_assigned = fields.DateTime(dump_only=True, dump_to='dateAssigned')

    @pre_load
    def validate_assignee_id_and_type_both_present(self, data):
        """Validates that both assignee id and type are present
        Args:
            data (dict): The request data
        """
        validate_id_and_type_both_present(data)

    @post_load
    def validate_space_assignee_in_center_provided(self, data):
        """Validates that the space is in the asset's center
        Also validates that the assignee id and type match
        Args:
            data (dict): The request data
        """

        data.update(self.context)
        validate_id_matches_type(data)
        validate_space_in_center(data)
        if 'assignee_type' in data:
            data[
                'assignee_type'] = AssetSchemaOperationsHelper.load_assignee_type(
                    data)


class AssetInflowAnalyticsSchema(AuditableBaseSchema):
    """Asset Inflow Analytic schema for CSV"""

    tag = fields.String(dump_to="Tag")

    category = fields.Function(
        lambda obj: obj.asset_category.name, dump_to="Category")

    assigned_by = fields.String(dump_to="Assigned By")

    assignee = fields.Function(
        lambda obj: obj.assignee.name, dump_to="Assignee")

    date_assigned = fields.Function(
        lambda obj: obj.date_assigned.date(), dump_to="Date Assigned")

    center = fields.Function(lambda obj: obj.center.name, dump_to="Center")

    store = fields.Function(lambda obj: obj.assignee.name, dump_to="Store")

    class Meta:
        fields = ('tag', 'category', 'store', 'center', 'assigned_by',
                  'date_assigned', 'assignee')
        ordered = True


class AssetInflowOutflowSchema(AssetSchema):
    """Asset Inflow and Outflow schema."""

    @staticmethod
    def group_keys(item):
        """Helper method for grouping items

        This method is used as the key to the `groupby` function.

        Args:
           item: The Asset model object

        Returns:
            (tuple): A tuple containing the keys used to group the items
        """
        formated_date = (item.date_assigned.strftime('%Y-%m-%d'))
        return (item.assignee_id, item.asset_category.id,
                item.asset_category.name, item.assigned_by, formated_date)

    @classmethod
    def grouped(cls, query_result):
        """This method is used to group the output

        Groups the output into specific forms. It groups items from the
        query result by asset category, assignee id, assigned by and date assigned

        Args:
            query_result: The query results
         Examples:
            output = [data for data in schema.grouped(query_result)]

        Returns:
            (dict): the grouped output in dictionary form
        """

        sorted_group = sorted(query_result, key=cls.group_keys)
        only = ['tag', 'assignee_type_dump', 'assignee', 'created_at']
        for (assignee_id, asset_category_id, name, assigned_by,
             date), assets in groupby(sorted_group, cls.group_keys):
            asset = cls(many=True, only=only).dump(assets).data

            yield {
                'category': {
                    'name': name,
                    'id': asset_category_id
                },
                'assignedBy': assigned_by,
                'assets': asset,
                'quantity': len(asset),
                'dateAssigned': str(date)
            }
