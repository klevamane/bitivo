""" Module for parsing url queries """

from inspect import isclass
from re import sub
from datetime import datetime
from functools import wraps
from flask import request
from werkzeug.datastructures import ImmutableMultiDict, CombinedMultiDict

# Middleware
from api.middlewares.base_validator import ValidationError

# Models
from api.models.base.base_model import BaseModel

# Error messages
from ..utilities.messages.error_messages import query_errors, filter_errors
from ..utilities.helpers.check_prefix import check_prefix


class QueryParser():
    """
    Parses queries from the frontend
    """

    # Queries excluded from parsing
    excluded_keys = ['include', 'limit', 'page', 'deleted', 'sort', 'order']

    @classmethod
    def parse(cls, model, key, value):
        """
        Converts a single url query to an immutable multidimensional
        dictionary query with a `where` format.

        Parameters:
            model (BaseModel): the model a filter is being generated for
            value (str): the value passed into the url query
            key (str): the key of the url query
        Returns:
            (dict): an immutable multidimensional dictionary query
        """

        prefix = ''
        actual_key = key.strip()
        value = value.strip().lower()
        operator = ''
        # Don't parse queries that are excluded
        if actual_key.lower() in cls.excluded_keys:
            return None

        # Parse as old syntax, if key is `where`
        if actual_key.lower() == 'where':
            return cls.parse_where_query(value)

        (prefix, actual_key, operator) = check_prefix(key)
        actual_key = cls.to_snake_case(actual_key)

        # Check if the column exist on the model
        column = cls.validate_column_or_custom_attributes_exists(
            model, actual_key)

        if column:
            filter_query = cls.filter_by_column_query(actual_key, value,
                                                      prefix, column, operator)
        else:
            filter_query = ImmutableMultiDict(
                [('where', f'{key.strip()}, like,{value}')])
        return filter_query

    @classmethod
    def parse_all(cls, model, url_queries):
        """
        Parses multiple url queries

        Parameters:
            model (BaseModel): the model a filter is being generated for
            url_queries (ImmutableMultiDict): the arguments being sent via
              the url
        """
        where_list = []
        for key, value in url_queries.items():
            result = cls.parse(model, key, value)
            if result:
                where_list.append(('where', result.get('where')))
        return ImmutableMultiDict(where_list)

    @classmethod
    def parse_where_query(cls, value):
        """
        Parses queries with old `where` syntax

        Parameters:
            value (str): the value passed into the url query
        """
        return ImmutableMultiDict([('where', value)])

    @classmethod
    def to_snake_case(cls, string):
        """
        Converts a string in PascalCase or camelCase to snake_case one
        """
        return sub(r'(.)([A-Z])', r'\1_\2', string).lower()

    @classmethod
    def validate_column_exists(cls, model, name):
        """
        Checks if `name` exists on `model` as a column

        Parameters:
            model (BaseModel): the model a filter is being generated for
            name (str): the key of the url query
        """
        if name not in model.__table__.columns:
            cls.raises('invalid_query_non_existent_column', name,
                       model.__name__)
        return getattr(model, name, None)

    @classmethod
    def validate_column_or_custom_attributes_exists(cls, model, name):
        """
        Checks if `name` exists on `model` as a column and the model has a custom_attributes column

        Parameters:
            model (BaseModel): the model a filter is being generated for
            name (str): the key of the url query
        """
        json_field = getattr(model, 'custom_attributes', None)
        if name not in model.__table__.columns and not json_field:
            cls.raises('invalid_query_non_existent_column', name,
                       model.__name__)
        return getattr(model, name, None)

    @classmethod
    def validate_type_is_date_or_integer(cls, key, value, column_type):
        """
        Validates that
        - the type of value matches column type
        - the type is a number or a datetime

        Parameters:
            key (str): the key of the url query
            value (str): the value passed into the url query
            column_type (sqltypes): the type of the column
        """
        allowed_types = [int, float, datetime]

        result = cls.validate_query_type(key, value, column_type)

        if type(result[0]) not in allowed_types:
            cls.raises('invalid_prefixed_query_type', key)

    @classmethod
    def get_column_type_str(cls, column_type):
        """
        Gets the stringified value of the column type

        Parameters:
            column_type (sqltypes): the type of the column
        """

        # Stringifies column type
        column_type_str = str(column_type)

        # Checks if the column type is a `VARCHAR`. If it is, it checks
        # if it is an `ENUM` and returns the appropriate type.
        if column_type_str.startswith('VARCHAR'):
            column_type_str = (hasattr(column_type, 'enums')
                               and 'ENUM') or 'VARCHAR'
        return column_type_str

    @classmethod
    def validate_query_type(cls, key, value, column_type):
        """
        Checks if the value is castable to Python type the column
        type represents

        Parameters:
            key (str): the key of the url query
            value (str): the value passed into the url query
            column_type (sqltypes): the type of the column `key` refers to
        """

        column_type_str = cls.get_column_type_str(column_type)

        def enum(value):
            if value not in column_type.enums:
                raise ValueError('not a valid value of the enum')

        database_types = {
            'VARCHAR': {
                'cast': str,
                'op': 'like'
            },
            'INTEGER': {
                'cast': int,
                'op': 'eq'
            },
            'FLOAT': {
                'cast': float,
                'op': 'eq'
            },
            'DATETIME': {
                'cast': lambda value: datetime.strptime(value, '%Y-%m-%d'),
                'op': 'eq'
            },
            'ENUM': {
                'cast': enum,
                'op': 'eq',
            },
            'BOOLEAN': {
                'cast': bool,
                'op': 'eq',
            }
        }

        try:
            result = ()
            # Gets the object corresponding to the column type from
            # `database_types` dictionary
            database_type = database_types.get(column_type_str)

            # Checks if query value can be casted to type of the column
            if database_type:
                result = (database_type.get('cast')(value),
                          database_type.get('op'))
            else:
                cls.raises('invalid_query_unsupported_type', key)
            return result
        except ValueError:
            cls.raises('invalid_query_wrong_value', key, value)

    @classmethod
    def raises(cls, error_key, *args):
        """
        Raises a query error

        Parameters:
            error_key (str): the key for accessing the correct error message
            args (*): variable number of arguments
        """
        raise ValidationError(
            {'message': query_errors[error_key].format(*args)}, 400)

    @classmethod
    def parse_queries(cls, func):
        """
        A decorator function that allows the parser to be used
        with pagination helper

        Parameters:
            func (function): the function that is being decorated
        """

        @wraps(func)
        def decorated_func(*args, **kwargs):
            # Check if the first argument has a type of model
            cls.validate_type_is_base_model(args[0], func.__name__)
            filter_query = cls.parse_all(args[0], request.args)
            request.args = CombinedMultiDict(
                [request.args, ImmutableMultiDict(filter_query)])
            return func(*args, **kwargs)

        return decorated_func

    @classmethod
    def validate_type_is_base_model(cls, value, func_name):
        """
        Checks if the value is a subclass of BaseModel

        Parameters:
            value (class): the class to test if it is a subclass of BaseModel
            func_name (str): the fname of the function that is being
                decorated
        """

        if not isclass(value):
            cls.raises('incompatible_decorated_function', func_name)
        if not issubclass(value, BaseModel):
            cls.raises('incompatible_decorated_function', func_name)

    @classmethod
    def validate_include_key(cls, query_keys, query_dict):
        """Check if 'include' query valid.

        Args:
            query_keys (tuple): tuple containing allowable 'include' query
                                key values.
            query_dict (dict): Dict holding all query data.

        Raises:
            (Validation Error): if supplied query key is invalid.
        """

        for key in query_dict:
            if key not in query_keys:
                raise ValidationError(
                    {'message': filter_errors['INVALID_COLUMN'].format(key)})

    @classmethod
    def filter_by_column_query(cls, *args):
        actual_key, value, prefix, column, operator = args
        # Check if there is a `start` or `end` prefix
        if prefix:
            cls.validate_type_is_date_or_integer(actual_key, value,
                                                 column.type)
        # Otherwise, parsed as `like` or `eq` operation
        else:
            operator = cls.validate_query_type(actual_key, value,
                                               column.type)[1]
        return ImmutableMultiDict([('where',
                                    f'{actual_key},{operator},{value}')])
