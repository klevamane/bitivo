# Celery
import csv
from io import StringIO

from flask import request

from api.models import Center, AssetCategory
from api.models.database import db
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
# utilities
from api.utilities.helpers.get_mailing_params import get_mailing_params
from main import celery_app
from . import SendEmail


class NamedStringIO(StringIO):
    """The aim of this class is to add an attribute name for
    file being written"""

    def __init__(self, content, name):
        """Ands and attribute name to StringIO"""
        super().__init__(content)
        self.name = name


class CreateCSV:
    """Convert a python tuple to a simple file format CSV"""

    def __init__(self, attributes):
        """Initialises titles for assets categories"""
        common_csv_title = ["assigneeType", 'tag', 'assignedBy'] + attributes
        self.fieldnames_errors = [
            "assetCategoryId", "assigneeId", 'centerId', "errors"
        ] + common_csv_title
        self.fieldnames_clean = [
            'id',
            'createdAt',
            'updatedAt',
            "assignee",
            "Asset Category",
            "Centers",
            'dateAssigned',
        ] + common_csv_title
        self.centers = self.get_centers()

    def clean_assets_to_csv_handler(self, assets_to_add):
        """Will prepare clean assets by converting id to names
        Args:
            assets_to_add(list) list of assets dicts
            for asset category
        Returns:
            StringIO: Will call a function that will convert assets to CSV
        """
        asset_category = AssetCategory.get(assets_to_add[0]["assetCategoryId"])
        asset_category_name = asset_category.name
        for asset in assets_to_add:
            asset["Asset Category"] = asset_category_name
            asset["assignee"] = asset["assignee"]["name"]
            asset["Centers"] = self.centers.get(asset["centerId"])
        return self.generate_csv_from_dict(assets_to_add,
                                           self.fieldnames_clean)

    def get_centers(self):
        """Will get all centers from DB as send as a dict
        Returns:
            dict: key centerId and center name dict
        """
        centers_details = db.session.query(Center.id, Center.name).all()
        return dict((id, name) for id, name in centers_details)

    def assets_with_errors_handler(self, assets_with_errors):
        """This function will first convert errors
         from dict to a string seperated by ,
         Args:
             assets_with_errors(list) list of assets dict
        Returns:
            StringIO: a function call that will converts assets
             dict to StringIO
         """
        for asset in assets_with_errors:
            errors_list = []
            for field_error in asset["errors"].values():
                errors_list = errors_list + field_error
            asset["errors"] = ",".join(map(str, errors_list))
        return self.generate_csv_from_dict(assets_with_errors,
                                           self.fieldnames_errors)

    def generate_csv_from_dict(self, items, titles):
        """Covert a tuple to CSV
        Args:
            items(list): List of dictionaries
            titles(list): list of titles
        Returns:
            String: CSV in form of a string
            """
        online_csv = StringIO()
        writer = csv.DictWriter(
            online_csv, titles, restval="N/A", extrasaction='ignore')
        writer.writeheader()
        for asset in items:
            custom_attribute = asset.get("customAttributes")
            if custom_attribute:
                asset.update(custom_attribute)
                asset.pop("customAttributes")
            writer.writerow(asset)
        return online_csv.getvalue()


class AssetBulkNotifications(CreateCSV):
    """Send notification to user on the status of the asset creation"""

    @staticmethod
    def send_bulk_assets_mail_handler(clean_assets, assets_with_errors,
                                      custom_attributes):
        """Will format data to CSV and call the mail to send them
        Args:
            clean_assets(list): dictionaries of added assets
            assets_with_errors(dict) dictionary of failed assets
            custom_attributes(List): List of tuples with attribute label,
            is_required, attribute key
        """
        attributes = [attribute[2] for attribute in custom_attributes]
        user_email = request.decoded_token['UserInfo']['email']
        user_name = request.decoded_token['UserInfo']['name']
        notify_uploader = adapt_resource_to_env(
            AssetBulkNotifications.send_asset_bulk_notification.delay)
        create_csv = CreateCSV(attributes)
        clean_data_csv = None if not clean_assets else \
            create_csv.clean_assets_to_csv_handler(clean_assets)
        errors_csv = None if not assets_with_errors else create_csv.assets_with_errors_handler(
            assets_with_errors)
        notify_uploader(user_email, user_name, "CSVs", errors_csv,
                        clean_data_csv)

    @staticmethod
    @celery_app.task(name='notify_user_on_asset_bulk')
    def send_asset_bulk_notification(*args):
        """sends email notification to user when process of creating bulk assets terminates.
        Args:
            args:
                user_email(str): Email of the person creating bulk assets
                user_name (str): Name of the person creating bulk assets
                status (str): Either failure or success of the process of
                creating bulk asset
                title (str): Reasons for failure
                errors_csv (str): CSV errors in string format
                clean_data_csv(str) CSV data in string format
        """
        user_email, user_name, title, errors_csv, clean_data_csv = args
        attachments = []
        if errors_csv:
            attachments.append(("attachment",
                                NamedStringIO(errors_csv,
                                              "assets_errors.csv")))
        if clean_data_csv:
            attachments.append((
                "attachment",
                NamedStringIO(clean_data_csv, "assets_added.csv"),
            ))
        template_data = {'user': user_name, 'title': title}
        params = get_mailing_params('asset_bulk_template',
                                    'Massive Asset Upload Report',
                                    template_data)
        params = dict(recipient=user_email, **params, attachments=attachments)
        SendEmail.send_mail_with_template(**params)
