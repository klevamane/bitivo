"""Module for handling sending of email"""
# Third-party libraries
from flask import json

# Celery
from main import celery_app

# Utilities
from api.utilities.migration_helper import create_or_skip, get_andela_users
from api.utilities.asset_migration_helper import (populate_records_with_data,
                                                  data_to_file)

# Models
from api.models.user import User

# Messages
from api.utilities.messages.error_messages import database_errors
from api.utilities.messages.error_messages import http_errors


class Migrations():
    """Execute migration tasks"""

    @staticmethod
    @celery_app.task(name='migrate_users')
    def migrate_users(requester, headers):
        """Migrate people records from api-staging and send status email

        Args:
            requester (dict): Details of user making request
        Returns:
            None
        """
        from api.tasks.email_sender import Email

        title = 'Activo User Migration'
        andela_users = get_andela_users(headers)
        # only occur if andela api staging returns invalid response or error
        if not andela_users or len(andela_users[0]) < 5:
            message = http_errors['invalid_response'].format('api-staging')
            return Email.send_mail.delay(title, [requester['email']], message)

        skipped_records = create_or_skip(User, 'email', 'users', andela_users)

        # send email
        message_body = database_errors['skipped'].format(
            requester['first_name'], 'people', json.dumps(skipped_records))
        Email.send_mail.delay(title, [requester['email']], message_body)

    @staticmethod
    @celery_app.task(name='migrate_assets')
    def migrate_assets(requester, sheet_data, asset_category, center_id, assigned_by):
        from api.tasks.email_sender import Email
        asset_category_id = asset_category['id']
        category_name = asset_category['name'].title()
        title = f"{category_name} Asset Migration"

        # Filter and remove empty columns
        columns = list(filter(None, sheet_data[0]))

        skipped_records, success_records = populate_records_with_data(
            requester, sheet_data, columns, asset_category_id, center_id, assigned_by)
        success_report = data_to_file(success_records)
        failed_report = data_to_file(skipped_records)
        attachment_data = []
        for attachment in ((success_report, 'Migrated'), (failed_report,
                                                          'Unmigrated')):
            data = {
                'file': attachment[0],
                'name': f'{attachment[1]}-{category_name}.csv'
            }
            attachment_data.append(data)

        message_body = database_errors['asset_skipped'].format(
            requester['first_name'], category_name, 'asset')
        Email.send_mail(title, [requester['email']], message_body,
                        attachment_data)
