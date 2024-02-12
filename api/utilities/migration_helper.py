"""Module for handling migration tasks, methods here must not be called outside
celery task to avoid import error
"""

# Third-party libraries
from sqlalchemy import text
import requests
from marshmallow import fields

# Application instance
from manage import app

# Database instance
from ..models.database import db

# Schemas
from ..schemas.base_schemas import AuditableBaseSchema

# Utilities
from ..utilities.sql_queries import sql_queries

# app config
from config import AppConfig

with app.app_context():
    from api.models import Role
    ROLE_DATA = {'title': 'Regular User', 'description': 'default user'}
    DEFAULT_ROLE = Role.find_or_create(ROLE_DATA, title=ROLE_DATA['title'])

    class UserImportSchema(AuditableBaseSchema):
        """Schema for processing imported data from API staging"""
        id = fields.String(dump_to='token_id')
        name = fields.String()
        email = fields.String()
        picture = fields.String(dump_to='image_url')
        role_id = fields.String(default=DEFAULT_ROLE.id)


def create_or_skip(*args):
    """Create new records into activo or skip if exists
    Args:
        args (tuple): Collection of arguments passed as follows:
            model (BaseModel): The table in which data is to be migrated
            key (string): Unique field with which to filter records
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

        skipped_list = []
        for item in data:
            if item[key] in existing:
                skipped_list.append(item[key])
            else:
                existing.add(item.get(key))
                db.session.add(model(**item))
        db.session.commit()
        return skipped_list


def get_andela_users(headers):
    """Retrieve people records from api-staging

    Args:
        headers (dict): Authorization for making request to activo-staging
    Returns:
        dict: Serialized user records from api-staging
    """
    url = AppConfig.API_STAGING
    raw_users = requests.get(url, headers=headers).json().get('values')
    import_schema = UserImportSchema(many=True)
    return import_schema.dump(raw_users).data
