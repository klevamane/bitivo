
"""Module for handling migration tasks, methods here must not be called outside
celery task to avoid import error
"""
# System libraries
from datetime import date, datetime

# Third-party libraries
from sqlalchemy import text
from humps.camel import case

# Database instance
from ..models.database import db

# Models
from api.models import User, Space, Asset

# Schemas
from ..utilities.messages.success_messages import SUCCESS_MESSAGES
from ..utilities.messages.error_messages import MIGRATION_ERRORS, serialization_errors

# Application instance
from manage import app

# Utilities
from ..utilities.sql_queries import sql_queries

from api.utilities.enums import AssetStatus
from .constants import ASK_FEJI


def process_failed_item(*args):
    """Processes assets that were not successfully migrated
    Generates message for assets that were not successfully migrated

    Args:
        args (list):
            0 (dict): skipped row from the data
            1 (str): unique key for validation. e.g Tag
            2 (list): list of valid statuses
            3 (bool): True for invalid status and False for valid status
            4 (bool): True for exists and False if it does not exist

    Returns:
        dict: Skipped row from the data
    """

    item, key, status_list, invalid_status, exists = args
    copy_item = item.copy()
    errors = []
    if exists:
        errors.append(MIGRATION_ERRORS['duplicate_key'].format(key.title(), item[key]))

    if invalid_status:
        valid_statuses = ', '.join(status_list)
        errors.append(serialization_errors['asset_status'].format(
            asset_status=f'"{valid_statuses}"'))

    if len(item[key]) < 1:
       errors.append(MIGRATION_ERRORS['invalid_key_length'].format(key.title()))

    migration_issue = copy_item.pop('Migration issue', {})

    if migration_issue:
        errors.append(migration_issue)
    copy_item.update({'Reasons for failure': ', '.join(errors)})
    return format_item(copy_item)


def process_success_item(item):
    """Processes assets that were successfully migrated
    Generates message for assets that were successfully migrated

    Args:
        item (dict): Skipped row from the data

    Returns:
        dict: Skipped row from the data
    """
    copy_item = item.copy()
    for invalid_key in ('assignee', 'Migration issue', 'Row Number',
                        'report_attributes'):
        item.pop(invalid_key, {})
    return format_item(copy_item)


def format_item(copy_item):
    """Formats the item to be included in the attachment
    Removes report_attributes from item to avoid invalid key error when saving

    Args:
        item (dict): Skipped row from the data

    Returns:
        dict: Skipped row from the data
    """
    attributes = copy_item.pop('report_attributes', {})

    invalid_keys = ('assignee_id', 'asset_category_id', 'center_id',
                    'assignee_type', 'date_assigned', 'assigned_by',
                    'custom_attributes')
    item = {}
    for key, value in copy_item.copy().items():
        if key not in invalid_keys:
            item.update({key.title(): value})

    copy_item = {**attributes, **item}

    return copy_item


def create_or_skip_assets(*args):
    """Create new records into activo or skip if exists
    Args:
        args (tuple): Collection of arguments passed as follows:
            model (BaseModel): The table in which data is to be migrated
            key (string): Unique field with which to filter records e.g Tag
            table_name (string): Name of the table to query
            data (list): Data retrieved from API to be migraded to db
    Returns:
        list: collection of records skipped
    """
    with app.app_context():
        model, key, table_name, data = args
        # existing records to skip
        existing = db.engine.execute(
            text(sql_queries['get_column'].format(key, table_name)))
        existing = {item[0] for item in existing}

        failed_data, success_data = [], [] # stores failed and success data respectively
        statuses = AssetStatus.get_all()

        # validates status
        validate_status = lambda x: x.get('status', '').lower() not in statuses
        for index, item in enumerate(data):
            item.update({'Row Number': index + 2})
            # Checks if asset exists or not a valid status
            striped_key = item[key].strip()
            exists = item[key] in existing
            invalid_status = validate_status(item)
            if not striped_key or exists or invalid_status:
                item = process_failed_item(item, key, statuses, invalid_status, exists)
                failed_data.append(item)
            else:
                existing.add(item.get(key))
                success_data.append(process_success_item(item))
                db.session.add(model(**item))
        db.session.commit()
        return failed_data, success_data


def data_to_file(file_data):
    """Writes a list of objects into a file object

    Arguments:
        file_data (list): An array of skipped records to be sent via email
        file_name (str): The name to use for the file object that will be created

    Returns:
        (file): The file object containing the data from file_data
    """

    import csv
    from io import StringIO

    output_file = StringIO()
    if len(file_data) > 0:
        csv_header = file_data[0].keys()
        dict_writer = csv.DictWriter(output_file, fieldnames=list(csv_header))
        dict_writer.writeheader()
        dict_writer.writerows(file_data)
    return output_file


def check_for_assignee(name):
    """Find assignee
        Check if the assignee is a user otherwise
        assign the assignee to store
        Args:
            name (str): the assignee name

        Returns:
            assignee (object): returns the object of the assignee
        """
    get_assignee = lambda model, name : model.query_().filter(model.name.ilike(str(name))).first()
    assignee = get_assignee(User, name) or get_assignee(Space, name)

    if not assignee:
        name = 'Ops Store'
        assignee = get_assignee(Space, name)
    return assignee


def cast_date_keys(is_date_keys, key, value):
    """Casts date keys to a the date format
    Args:
        is_date_keys (func): Checks if a key is a date keys
        key (string): Unique field with which to filter records
        value (str): The value to cast
    Returns:
        str: Casted value
    """
    if is_date_keys(key):
        value = value.strftime('%Y-%m-%dT%H:%M:%S') if isinstance(value,
                                                                  date) else ''
    return value


def map_sheet_columns_to_database_columns(*args):
    """Creates new records into activo or skip if exists
    Args:
        args (tuple): Collection of arguments passed as follows:
            columns (list): The table in which data is to be migrated
            record (dict):
            is_date_keys (func): Checks if a key is a date keys
            is_custom_atrr (func): Checks if a key is a custom attribute
    Returns:
        list: collection of records skipped
    """

    asset, custom_attributes, report_attributes = {}, {}, {}
    columns, record, is_date_keys, is_custom_attr = args
    for key, value in zip(columns, record[:]):
        value = cast_date_keys(is_date_keys, key, value)
        if is_custom_attr(key):
            custom_attributes.update({case(key): value})
            report_attributes.update({key.title(): value})
        else:
            asset.update({key.lower(): value})
    asset.update({'report_attributes': report_attributes})
    return asset, custom_attributes


def populate_records_with_data(*args):
    """Populate the data object to be saved
    maps the data to be saved in thier respective field names
    as specified in the table
    Args:
        asset_data (dict) : The data records
        columns (list): the column names
        asset_category (obj): object instance of asset categories
    Returns:
        skipped_list (list): the list of records that were not
        successfuly saved
    """
    with app.app_context():

        # Remove assignee and tag from the column to get custom attributes
        assets = []
        requester, sheet_data, columns, asset_category_id, center_id, assigned_by = args
        is_custom_attr = lambda key: key not in ('Tag', 'Assignee', 'Status')
        is_date_keys = lambda key: is_custom_attr(key) and key.lower().startswith('date')
        for record in sheet_data[1:]:
            asset, custom_attributes = map_sheet_columns_to_database_columns(
                columns, record, is_date_keys, is_custom_attr)
            assignee = check_for_assignee(name=asset.get('assignee'))
            if assignee.name.lower() != str(asset.get('assignee')).lower():
                migration_issue = ASK_FEJI
            else:
                migration_issue = ''

            assignee_type = assignee.__class__.__name__.lower()
            assignee_maper = {'user': 'token_id', 'space': 'id'}
            asset.update({
                "asset_category_id":
                asset_category_id,
                "center_id":
                center_id,
                "assigned_by":
                assigned_by,
                "assignee_type":
                assignee_type,
                "date_assigned":
                datetime.now(),
                "assignee_id":
                getattr(assignee, assignee_maper.get(assignee_type)),
                'Migration issue': migration_issue,
                "custom_attributes":
                custom_attributes
            })
            assets.append(asset)
        return create_or_skip_assets(Asset, 'tag', 'asset', assets)
