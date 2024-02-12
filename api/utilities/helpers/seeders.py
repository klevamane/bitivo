"""Seeders helper module"""

# Standard library
import json

# Third party
from sqlalchemy import tuple_

# Models
from ...models.database import db
from ...models.center import Center
from ...models.space_type import SpaceType
from ...models.asset_category import AssetCategory
from ...models.space import Space
from ...models.asset import Asset
from ...models.role import Role
from ...models.user import User
from ...models.permission import Permission
from ...models.resource import Resource
from ...models.resource_access_level import ResourceAccessLevel
from ...models.request_type import RequestType
from ...models.work_order import WorkOrder
from ...models.schedule import Schedule
from ...models.maintenance_category import MaintenanceCategory
from ...models.hot_desk import HotDeskRequest

# App config
from config import AppConfig


def seed_data_helper(*args, **kwargs):
    """Abstracts seed data functionality

    Args:
        *args: Variable length argument list.
            get_data(func): get data based on environment.
            data_type(str): type of data to be seeded, ie, string repr of a model.
            model(class): Tsble to be seeded.
        **kwargs: Arbitrary keyword arguments.
    """
    get_data, data_type, model = args
    data = get_data(data_type)[data_type]

    if not kwargs.get('clean_data', False):
        data = clean_seed_data(data_type, data)

    model.bulk_create(data)


# Convert JSON to Python Dictionary
def json_to_dictionary(file_path):
    """Method that converts a JSON file to a Dictionary

    Args:
        file_path(str): directory to the JSON file

    Returns:
        dict: converts JSON to a dictionary
    """
    if AppConfig.FLASK_ENV in ('production', 'staging'):
        env_path = 'production'
    else:
        env_path = 'development'
    try:
        with open(file_path.format(env_path)) as data:
            return json.load(data)
    except FileNotFoundError:
        raise FileNotFoundError('File Not Found Error')


def get_existing_records(resource_details, lookup_list):
    """Gets list of unique lookup values for already existing records.

    Args:
        resource_details (tuple): Consists model class, unique lookup field &
            param to be used in the query.
        lookup_list (list): Contains all lookup values for new data to be seeded.

    Returns:
        list: List of unique lookup column values for already existing records.
    """

    model, lookup_field, query_param = resource_details

    # The following block applies in cases where a table to be seeded
    # has no unique constraint columns.
    # Currently only works with a combination of 2 fields.
    if isinstance(lookup_field, tuple):
        new_lookup_list = []
        for value in lookup_list:
            new_lookup_list.append((value[0], value[1]))

        return [(record.__dict__.get(lookup_field[0]),
                 record.__dict__.get(lookup_field[1]))
                for record in db.session.query(model).filter(
                    tuple_(query_param[0], query_param[1]).in_(
                        new_lookup_list)).all()]

    return [
        record.__dict__.get(lookup_field)
        for record in db.session.query(model).filter(
            query_param.in_(lookup_list)).all()
    ]


def get_record_lists(lookup_field, data):
    """Gets list of lookup values for new records to be added.

    Args:
        lookup_field (str): Unique field to be used to check if record is
            already existing
        data (list): Holds records/data to be seeded

    Returns:
        (list): List of unique field values for the new data to be seeded. To
            be used to check for any already existing records in a table.
    """

    # List of unique field values to be used to verify already existing records
    return [record[lookup_field] for record in data]


def clean_seed_data(resource, data, is_lookup_list=False):
    """Removes already existing entries from the data to be seeded.

    Args:
        resource (str): Refers to model/table to be seeded.
        data (list/tuple): Seed data.
        is_lookup_list (bool): Indicates if args is a list of look up
            values or dicts.

    Returns:
        list : Non-existing data to be seeded to the DB
    """

    # Maps resource name to Model, unique lookup field and query_param
    # ie. { resource_name: (Model, unique_lookup_column, query_param)
    resource_mapper = {
        'center': (Center, 'name', Center.name),
        'space_type': (SpaceType, 'type', SpaceType.type),
        'asset_category': (AssetCategory, 'name', AssetCategory.name),
        'spaces': (Space, 'name', Space.name),
        'asset': (Asset, 'tag', Asset.tag),
        'role': (Role, 'title', Role.title),
        'user': (User, 'email', User.email),
        'permission': (Permission, 'type', Permission.type),
        'request_type': (RequestType, ('title', 'center_id'),
                         (RequestType.title, RequestType.center_id)),
        'resource': (Resource, 'name', Resource.name),
        'resource_access_level':
        (ResourceAccessLevel, ('role_id', 'resource_id'),
         (ResourceAccessLevel.role_id, ResourceAccessLevel.resource_id)),
        'work_order': (WorkOrder, 'title', WorkOrder.title),
        'schedule': (Schedule, ('assignee', 'work_order_id'),
                     (Schedule.assignee, Schedule.work_order_id)),
        'maintenance_category': (MaintenanceCategory, 'title',
                                 MaintenanceCategory.title),
        'hot_desk_request': (HotDeskRequest, 'requester_id', HotDeskRequest.requester_id)
    }

    resource_details = resource_mapper.get(resource)

    if is_lookup_list:
        unique_fields = data
    else:
        unique_fields = get_record_lists(resource_details[1], data)

    existing_records_list = get_existing_records(resource_details,
                                                 unique_fields)

    new_records = set(unique_fields).difference(existing_records_list)

    new_data = []
    for record in new_records:
        new_data.append(data[unique_fields.index(record)])

    return new_data
