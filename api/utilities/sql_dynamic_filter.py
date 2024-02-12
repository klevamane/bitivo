# Third Party Library
from flask import request
from datetime import datetime

# Local Modules
from api.middlewares.base_validator import ValidationError
from api.utilities.messages.error_messages import filter_errors
from api.utilities.constants import DATE_COLUMNS
from api.utilities.error import raises
from .dynamic_filter import DynamicFilter
import re


class SQLDynamicFilter(DynamicFilter):
    """
    A class that returns filtered conditions for sql queries
    """

    def sql_query_filter(self, args):
        """Returns filters for sql query.

        Args:
            args (ImmutableDict): The request query object
            columns (list): list of columns that belongs to a particular table

        Returns:
            (str): the filters for sql query
        """

        # get table columns and types
        columns = self.model.__mapper__.columns
        invalid_column_types = [col.type for col in columns]
        valid_types = []
        # Remove search_vector column from list because calling
        # model.__mapper__.columns.python_type on  TSVectorType
        # raises a NotImplementedError

        for index in invalid_column_types:
            try:
                valid_types.append(index.python_type)
            except:
                continue

        columns = columns.keys()
        column_types = dict(zip(columns, valid_types))

        filter_conditions = ''

        raw_filters = args.getlist('where')
        for raw in raw_filters:

            filter_conditions = self.get_where_conditions(
                raw, filter_conditions, columns)

        filter_conditions = self.get_key_conditions(args, filter_conditions,
                                                    columns, column_types)

        return filter_conditions

    def sql_filter_mapper(self, column, op, value):
        """Maps an operator to sql filter condition

        Args:
            column (str): The table column for filter
            op (str): The operator to be mapped
            value (str): The filter condition value to be matched

        Returns:
            (str): A filter condition
        """

        if column in DATE_COLUMNS:
            value = f"'{value}'"
        op_mapper = {
            'like': f"{column} ilike '%{value}%'",
            'eq': f"{column} = {value}",
            'lt': f"{column} < {value}",
            'ne': f"{column} != {value}",
            'gt': f"{column} > {value}",
            'le': f"{column} <= {value}",
            'ge': f"{column} >= {value}",
        }

        return op_mapper.get(op.lower().strip(), '')

    def get_where_conditions(self, raw, filter_conditions, columns):
        """Returns filters for sql query from where parameters.

        Builds filter condition from the where parameters
        E.g if raw args contains 'where=runningLow,gt,5' it
        should return 'AND running_low > 5' which will be
        passed as one of the filter conditions in the WHERE
        clause of an sql statement

        Args:
            raw (str): the conditions to be parsed
            filter_conditions (str): The request query object
            columns (list): list of columns that belongs to a particular table

        Returns:
            (str): the sql filter conditions
        """

        key_in_snake_case, op, value, key = self.strip_query(raw)

        column = key_in_snake_case if key_in_snake_case in columns else None

        if not column:
            raise ValidationError(
                dict(message=filter_errors['INVALID_COLUMN'].format( key_in_snake_case)))

        return filter_conditions + f' AND {self.sql_filter_mapper(column, op, value)}'

    def to_type(self, value):
        """Converts string value to int if the
            value is not in a date format

        Args:
            value (str): The value to be converted

        Returns:
            given value if not convertable else an int
        """

        try:
            if re.search(r'\d{4}-\d{2}-\d{2}', value):
                return datetime.strptime(value, '%Y-%m-%d')
            return int(value)
        except ValueError:
            return value

    def validate_value_type(self, key, value, column_types):
        """Validates fields type.

        Args:
            key (str): The field to be validated
            value (str): The value to be validated
            columns_types (dict): mapping of fields to types

        Raises:
            400 error with message if value is to valid type for key
        """

        if column_types.get(key) != type(self.to_type(value)):
            raises('invalid_value', 400, value, key + ' field')

    def get_key_conditions(self, args, filter_conditions, columns,
                           column_types):
        """Returns filters condition from query fields.

        Builds filter condition from the query parameters
        that are available in the columns of a table
        E.g if there is a url query parameter 'name=Monitors'
        it should return ' AND name = Monitors' which will be
        passed as one of the filter conditions in the WHERE
        clause of an sql statement

        Args:
            args (ImmutableDict): The request query object
            filter_conditions (str): The request query object
            columns (list): list of columns that belongs to a particular table
            columns_types (dict): dict mapping column names to types

        Returns:
            (str): the sql filter conditions
        """

        from .query_parser import QueryParser as qp

        excluded_keys = qp.excluded_keys + columns + ['where']
        filters = filter_conditions

        for key, value in args.items():
            snake_case_key = qp.to_snake_case(key)
            if snake_case_key not in excluded_keys:
                qp.raises('invalid_query_non_existent_column', key,
                          'AssetCategory')

            if snake_case_key in columns:
                self.validate_value_type(snake_case_key, value, column_types)
                filters += f" AND {snake_case_key} = '{value}'"

        return filters
