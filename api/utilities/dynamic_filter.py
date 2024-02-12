# Third Part Library
from sqlalchemy import func
from sqlalchemy.types import Unicode

# Local Modules
from .filter_functions import (like, is_equal, less_than, not_equal,
                               greater_than, less_or_equal, greater_or_equal)
from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import filter_errors
from api.utilities.constants import DATE_COLUMNS
from api.utilities.error import raise_error_helper
from api.utilities.validators.date_validator import date_validator


class DynamicFilter:
    """
    A class that returns filtered database records
    """

    def __init__(self, model):
        """
        Constructor to initialize an instance of the class.
        :param model: the model class that will be using the methods of
        this class
        """
        self.model = model
        self.query = model.query

    mapper = {
        'like': like,
        'eq': is_equal,
        'lt': less_than,
        'ne': not_equal,
        'gt': greater_than,
        'le': less_or_equal,
        'ge': greater_or_equal,
    }

    def validate_query(self, key, value, op):
        """Validate parameters passed to any endpoint for filtering.

        The essence of this is to validate parameters before making a call to
        the database, if the parameters are invalid then we dont make any
        database query which therefore improves performance

        Note:
            For filtering by delete the parameter should be a boolean
            For filtering by date the date should be a valid date
            The filter operator should be valid

        Args:
            key (str): the parameter key to be validated
            value (str): the parameter value to be validated
            op (str): a representation of the operator to be validated

        Raises:
            ValidationError: if any of the parameters is not valid

        Examples:
            delete
            ======
            Correct:
            http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
            deleted,eq,true

            Incorrect and will throw an error and return a response:
            http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
            deleted,eq,Invalid_delete_value

            date
            ====
            Correct:
            http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
            created_at,eq,2018-06-19

            Incorrect and will throw an error and return a response:
            http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
            created_at,eq,invalid_date

            Invalid operator
            ================
            http://127.0.0.1:5000/api/v1/asset-categories/stats?where=
            deleted,invalid_operator,true

        """

        # validate operator
        is_invalid = op not in self.mapper
        raise_error_helper(is_invalid, filter_errors, 'INVALID_OPERATOR')

        # validate value of deleted key
        is_invalid = (key == 'deleted' and value not in ('true', 'false'))
        raise_error_helper(is_invalid, filter_errors,
                           'INVALID_DELETE_ATTRIBUTE')

        # validate date value
        if key in DATE_COLUMNS:
            date_validator(value)

    def filter_query(self, args):
        """Returns filtered database entries

        An example of filter_condition is:

            User.query_('name,like,john').Apart from 'like',
            other comparators are eq(equal to),ne(not equal to),lt(less than),
            le(less than or equal to) gt(greater than),
            ge(greater than or equal to)
        Args:
            args (list): filter_condition

        Returns:
            list: an array of filtered records
        """
        # get filter parameters
        raw_filters = args.getlist('where')
        include_deleted = args.to_dict().get('include')
        result = self.query

        if include_deleted and include_deleted == 'deleted':
            result = self.query.include_deleted()

        for raw in raw_filters:

            key_in_snake_case, op, value, key = self.strip_query(raw)

            column = getattr(self.model, key_in_snake_case, None)
            json_field = getattr(self.model, 'custom_attributes', None)

            # getting the method to operator function
            db_filter = self.mapper.get(op)
            result = self.filter_column_attributes(
                column, json_field, db_filter, key_in_snake_case, value,
                result, key)

        return result

    def filter_column_attributes(self, *args):
        """Filters the database records

        Operations:
            1. filters with key-value is column and not json field
            2. filters with custom attributes method is json_field
            3. filters with datetime fields
            4. raises an error is column or json_field is None

        It uses a function to filter the database column by the column key and value

        Args:
            *args (ImmutableDict):
                column(obj): SQL alchemly object attribute
                json_field(obj): SQL alchemly object attribute
                db_filter(function): Filtering function
                key(str): column name to be filtered
                value(str): value to filter by
                result(obj): SQL Alchemly query
        Returns:
            result(obj): SQL Alchemly query
        """
        column, json_field, db_filter, key_in_snake_case, value, result, key = args

        if not column and not json_field:
            raise ValidationError(
                dict(message=filter_errors['INVALID_COLUMN'].format(
                    key_in_snake_case)))
        elif not column and json_field:
            result = result.filter(
                db_filter(
                    self.model.custom_attributes[key].astext.cast(Unicode),
                    value))
        elif str(column.type) == 'DATETIME':
            result = result.filter(db_filter(func.date(column), value))
        else:
            result = result.filter(db_filter(column, value))
        return result

    def strip_query(self, raw):
        """Parse query conditions.

        Operations:
            1. splits raw query into key,operator and value
            1. validates parsed query format
            2. changes the query key to snake_case

        Args:
            raw (str): the conditions to be parsed

        Returns:
            (str): the sql filter conditions
        """
        try:
            key, op, value, = raw.split(',', 3)
        except ValueError:
            raise_error_helper(True, filter_errors, 'INVALID_FILTER_FORMAT',
                               raw)

        from .query_parser import QueryParser
        key_in_snake_case = QueryParser.to_snake_case(key.strip())
        op = op.lower().strip()
        value = value.strip()

        self.validate_query(key_in_snake_case, value, op)

        return key_in_snake_case, op, value, key
