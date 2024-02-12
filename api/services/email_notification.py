"""Module for sending email notifications"""

# Standard Library
from sqlalchemy import text

# Models
from api.models import Role

# App config
from config import AppConfig

# Utilities
from api.tasks.notifications import SendEmail
from ..utilities.helpers.get_mailing_params import get_mailing_params
from ..utilities.emails.email_templates import email_templates
from ..utilities.sql_queries import sql_queries
from ..utilities.enums import AssetStatus
from api.models.database import db

# This import is commented out because the stock level notification mail
# feature has currently been disabled as a request by the Operations Associate team

# from . import celery_scheduler


def asset_counter(query):
    """Function to query all available assets

    Args:
        query (str): An SQL string statement to query the database
    """

    return list(db.engine.execute(text(query)))


# this decorator is commented out because the stock level notification mail
# feature has currently been disabled as a request by the Operations Associate team

# @celery_scheduler.task(name='low_asset_count_notifier')


def low_asset_count_notifier():
    """Function to notify users when asset category levels is running low"""

    role = Role.query_().filter_by(title='Operations Associate').first()

    users = role.users.all() if role else []

    query = sql_queries['check_asset_category_levels'].format(
        AssetStatus.OK_IN_STORE.value, AssetStatus.AVAILABLE.value,
        AssetStatus.INVENTORY.value)

    asset_count = asset_counter(query)

    notified = False

    for asset_category_name, running_low, low_in_stock, count in asset_count:
        if count <= running_low:
            notify_users(
                users, asset_category_name, count, low_in_stock,
                email_templates.get('low_in_stock').get('default_data'))
            notified = True
    return notified


def notify_users(*args):
    """Function to notify many users

    Args:
        *args: Variable length argument list and the mandatory position arguments for this list are:
            users (instance): an instance of User class
            asset_category_name (str): Asset category name
            count (int): An integer representing asset count
            low_in_stock (int): An integer representing the Asset_category low in stock threshold value
            data (dict): A transactional email template
    """
    users, asset_category_name, count, low_in_stock, data = args
    data['domain'] = AppConfig.DOMAIN

    for user in users:
        data["user_first_name"] = user.name
        data["asset_category_name"] = asset_category_name
        data["asset_count"] = count

        if count <= low_in_stock:
            data["asset_status"] = "low in stock"
        else:
            data["asset_status"] = "running low"

        title = f"{data['asset_category_name']} is {data['asset_status']}"
        params = get_mailing_params('low_in_stock', title, data)

        params = dict(recipient=user.email, **params)

        SendEmail.send_mail_with_template(**params)
