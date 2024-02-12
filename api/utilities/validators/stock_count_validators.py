"""Module for stock count validation"""

# Third party
from sqlalchemy import extract

# Models
from ...models.stock_count import StockCount

# Validators
from .duplicate_validator import validate_input_duplicate
from .validate_id import id_validator
from .asset_category_exists import asset_category_exists

# Error
from ..error import raise_error, raises

# Error messages
from ..messages.error_messages import INVALID_INPUT_MSG_EXTRAS


class StockCountValidator:
    """Validate stock count details"""

    @classmethod
    def validate_stock_count_list(cls, request_data):
        """Checks if stock count is valid list.

        Verify that the stock count data provided is a list with a length >=1.

        Args:
            request_data (dict): dict containing stock count request data
            for various asset categories.

        Raises:
            ValidationError: If 'stockCount' list is not a list or is an
                empty list.
        """

        stock_count_list = request_data.get("stockCount")
        # Validate for 'stockCount' field unavailable
        if stock_count_list is None:
            raises('missing_input_field', 400, 'stockCount')

        # Validate for stock_count_list is an empty list
        if not isinstance(stock_count_list, list) or len(stock_count_list) < 1:
            raises('invalid_input_value', 400, 'stockCount')

    @classmethod
    def validate_duplicate_stock_count(cls, week, asset_category_id, month,
                                       year):
        """Checks if stock count record is already existing in the DB.

        Args:
            week (int): Value of week for which count is to be recorded.
            asset_category_id (str): ID of the asset category whose count
                is to be recorded.
            month (int): Number value of the month.
            year (int): Current year.

        Raises:
            ValidationError: If stock count record for the specified period
                already exists.
        """

        # Get any matching stock count records for the corresponding period
        stock_count = StockCount.query_() \
            .filter_by(
            week=week, asset_category_id=asset_category_id)\
            .filter(extract('month', StockCount.created_at) == month)\
            .filter(
            extract('year', StockCount.created_at) == year)\
            .first()
        if stock_count:
            raise_error('stock_count_exists', 'stockCount',
                        **{'fields': 'stockCount'})

    @staticmethod
    def validate_asset_category_duplicate(data, asset_category_id_set):
        """Validates that asset_category_id is not duplicated in the request.

        Args:
            data (dict): Dict containing stock count collection element details.
            asset_category_id_set (set): Set of asset category ids.

        Raises:
            ValidationError: If assets category is duplicated.
        """

        validate_input_duplicate(data, asset_category_id_set,
                                 'asset_category_id')

    @staticmethod
    def validate_asset_category_id(asset_category_id):
        """Checks if asset_category_id is valid.

        Args:
            asset_category_id (str): Asset category ID value.

        Raises:
            ValidationError: If asset_category_id has invalid format
                or doesn't exist.
        """

        # Checks if  ID valid.
        id_validator(asset_category_id)
        # Checks if asset category exists.
        asset_category_exists(asset_category_id)

    @staticmethod
    def validate_week(week):
        """Validates week provided in request data.

        Checks that the week value in the request data is an integer and that
        it lies between 1-4.

        Args:
            week (int): Week in month for which stock count is being taken.

        Raises:
            ValidationError: If week values not  in the range of 1 - 4.
        """

        if week not in (1, 2, 3, 4) or not isinstance(week, int):
            raise_error('invalid_value',
                        *[week, INVALID_INPUT_MSG_EXTRAS['week']])

    @classmethod
    def validate_different_weeks(cls, week_list):
        """Validates that same value for week was provided.

        Args:
            week_list (list): List of all provided week values.

        Raises:
            ValidationError: If week list values differ.
        """

        # Convert list of week values to set,
        # if length of set != 1 it means there's different values
        # for week in the list.
        if len(set(week_list)) != 1:
            raises('different_week', 400)

    @classmethod
    def validate_count(cls, count):
        """Checks if the count is a valid integer.

        count value should range from 0 to 10,000.

        Args:
            count (int): Stock count number value.

        Raises:
            ValidationError: If count value is invalid.
        """

        if count not in range(0, 1000000):
            raise_error('invalid_value',
                        *[count, INVALID_INPUT_MSG_EXTRAS['count']])
