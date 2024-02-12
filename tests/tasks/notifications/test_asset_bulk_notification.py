import json
from io import StringIO
# System
from os import getenv
from unittest.mock import Mock

# Services
from api.tasks.notifications.asset_bulk import AssetBulkNotifications
from api.utilities.constants import CHARSET

API_BASE_URL_V1 = getenv('API_BASE_URL_V1')
from api.tasks.notifications.asset_bulk import SendEmail


class TestAssetBulkSendEmailNotifications:
    """Test send email notification when asset bulk creation fails"""

    def test_send_email_when_asset_bulk_creation_fails(
            self, client, init_db, auth_header, new_user, multiple_assets,
            test_asset_category):
        """Non found asset category, repeated tag, invalid assignee type
        Args:
            client(FlaskTestClient): used to call endpoints and test
            init_db(SqlAlchemyConnection): USed to sustain the db
            auth_header(dict): Authorisation headers
            new_user(object): User object
            multiple_assets(dict): multiple assets dict
            """

        new_user.save()
        multiple_assets["assetCategoryId"] = test_asset_category.id
        for index, asset in enumerate(multiple_assets["assets"]):
            asset["tag"] = asset["tag"] + str(index)
            asset["assetCategoryId"] = test_asset_category.id
            asset["assigneeId"] = new_user.token_id
            asset["assigneeType"] = "user"
        multiple_assets["assets"][0]["assigneeType"] = "dsnjds"
        AssetBulkNotifications.send_asset_bulk_notification.delay = Mock(
            side_effect=AssetBulkNotifications.send_asset_bulk_notification)
        SendEmail.send_mail_with_template = Mock()
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        json.loads(response.data.decode(CHARSET))
        del AssetBulkNotifications.send_asset_bulk_notification.delay
        template_data = SendEmail.send_mail_with_template.call_args[1]
        assert response.status_code == 201
        assert template_data['recipient'] == 'test_user@andela.com'
        assert template_data['mail_subject'] == 'Massive Asset Upload Report'
        assert template_data['mail_html_body']
        assert issubclass(type(template_data["attachments"][0][1]), StringIO)
        assert template_data["attachments"][0][0] == "attachment"
        assert issubclass(type(template_data["attachments"][1][1]), StringIO)
        assert template_data["attachments"][1][0] == "attachment"
