""" Module for base marshmallow schema. """
from marshmallow import Schema, fields
from sqlalchemy.engine.result import RowProxy
from itertools import _grouper

from ..middlewares.base_validator import ValidationError


class BaseSchema(Schema):
    """Base marshmallow schema with common attributes."""
    id = fields.String(dump_only=True)
    deleted = fields.Boolean(dump_only=True)

    def load_json_into_schema(self, data):
        """Helper function to load raw json request data into schema"""
        data, errors = self.loads(data)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data

    def load_object_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema"""
        data, errors = self.load(data, partial=partial)

        if errors:
            raise ValidationError(
                dict(errors=errors, message='An error occurred'), 400)

        return data

    def dump(self, _obj, many=None, update_fields=True, **kwargs):
        """Method to override the Shema dump method
           This methods determines whether to include deleted object in
           returned data depending on the arguments passed.

        Args:
            self(obj): instance of the BaseSchema class
            _obj(obj): current object going through the schema dump method
            many(bool): determines whether _obj is to be serialized as a collection or not
            update_fields(bool): Whether to update the schema's field classes.
            kwargs(dict): key word arguments passed to method

        Returns:
            dump(func): dump method after performing some actions on _obj

        """
        request_args = kwargs.pop('request_args', {})
        include = request_args.get('include')

        try:
            obj = _obj.all()
        except:
            obj = _obj

        BaseSchema.filter_object(obj, include)
        return super(BaseSchema, self).dump(
            obj, many=many, update_fields=update_fields, **kwargs)

    @staticmethod
    def filter_object(obj, include):
        """Filter through iterables to return only undeleted objects
        when 'include=deleted' params are passed

        Args:
            obj(object): current object going through the schema dump method
            include(dict): string from request args to determine whther to include deleted objects
                           in the returned data.

        Returns:
            obj(object): filtered or unfilter object depending on include parameter
        """
        # check that the right data is passed for it to be filtered
        check_object_type = lambda obj: not isinstance(obj, (
            str, dict, RowProxy, _grouper)) and hasattr(obj, '__iter__')

        filter_dict_or_object_type = BaseSchema.filter_helper

        # check if obj is iterable or 'include=deleted' params passed
        if include != 'deleted' and check_object_type(obj):
            obj = filter_dict_or_object_type(obj)
        return obj

    @staticmethod
    def filter_helper(obj):
        """Assists the filter_object method

        Args:
            obj(object): current object going through the filter_object method

        Returns:
            filter_dict_or_object_type(function): filters data in iterable depending on whether
                                    it is a dict type or object type
        """
        # filter data using appropriate list comprehension
        list_comprehension = lambda obj, check: [item for item in obj if not item.deleted] if\
            check else [item for item in obj if 'deleted' in item.keys() and not item['deleted']]

        # filter data in iterable depending on whether it is a dict type or object type
        filter_dict_or_object_type = lambda obj: list_comprehension(obj, True) if\
            obj and hasattr(obj[0], 'deleted') else list_comprehension(obj, False)

        return filter_dict_or_object_type


class AuditableBaseSchema(BaseSchema):
    """ Base marshmallow schema for auditable models. """
    created_at = fields.DateTime(dump_only=True, dump_to='createdAt')
    updated_at = fields.DateTime(dump_only=True, dump_to='updatedAt')
    deleted_at = fields.DateTime(dump_only=True, dump_to='deletedAt')
    created_by = fields.String(dump_only=True, dump_to='createdBy')
    updated_by = fields.String(dump_only=True, dump_to='updatedBy')
    deleted_by = fields.String(dump_only=True, dump_to='deletedBy')
