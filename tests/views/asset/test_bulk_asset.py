"""Module for asset resource endpoints."""
from os import getenv

from flask import json

from unittest.mock import patch
from api.utilities.constants import CHARSET
from api.schemas.asset import AssetSchema
from api.utilities.enums import AssigneeType
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.helpers.bulk_asset_helper import BulkAssetHelper
from api.utilities.messages.error_messages.jwt_errors import error_dict
from api.utilities.messages.error_messages.serialization_error import error_dict as serial_dict

API_BASE_URL_V1 = getenv('API_BASE_URL_V1')


class TestBulkAssetPostEndpoint:
    """Class for Asset resource POST endpoint."""

    def test_create_bulk_asset_with_valid_data_succeeds(
            self, client, init_db, auth_header, test_asset_category, new_user,
            multiple_assets):
        """
        Test create asset with arguments for a
        category with no custom attributes
        Args:
            client(FlaskTestClient): used to call endpoints and test
            init_db(SqlAlchemyConnection): USed to sustain the db
            auth_header(dict): Authorisation headers
            test_asset_category(object): Asset category for test
            new_user(object): User object
            multiple_assets(dict): multiple assets dict
        """
        new_user.save()
        multiple_assets["assetCategoryId"] = test_asset_category.id
        for asset in multiple_assets["assets"]:
            asset["assigneeId"] = new_user.token_id
            asset["assigneeType"] = AssigneeType.user.value
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['created'].format(
            'Multiple assets')
        assert len(response_json["data"]["AddedAssets"]) == 4

    def test_create_bulk_assets_with_invalid_data_fails(
            self, client, init_db, auth_header, new_user, multiple_assets):
        """Non found asset category, repeated tag, invalid assignee type
        Args:
            client(FlaskTestClient): used to call endpoints and test
            init_db(SqlAlchemyConnection): USed to sustain the db
            auth_header(dict): Authorisation headers
            new_user(object): User object
            multiple_assets(dict): multiple assets dict
            """
        new_user.save()
        for index, asset in enumerate(multiple_assets["assets"]):
            asset["tag"] = asset["tag"] + str(index)
            asset["assetCategoryId"] = "dummy id"
            asset["assigneeId"] = "-L_lql3gAMVhOarf6HYc"
            asset["assigneeType"] = "invalid assignee"
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["data"][0]["errors"]["assetCategoryId"] == [
            serial_dict["not_found"].format("Asset category")
        ]
        assert response_json["data"][0]["errors"]["assigneeId"] == [
            serial_dict["assignee_not_found"]
        ]
        assert response_json["data"][0]["errors"]["assigneeType"] == [
            serial_dict["invalid_assignee_type"].format("invalid assignee")
        ]

    def test_create_bulk_assets_with_no_asset_category_fails(
            self, client, init_db, auth_header, new_user, multiple_assets):
        """Test creation of bulk assets with no asset category
        Args:
            client(FlaskTestClient): used to call endpoints and test
            init_db(SqlAlchemyConnection): USed to sustain the db
            auth_header(dict): Authorisation headers
            new_user(object): User object
            multiple_assets(dict): multiple assets dict
            """
        mock_assignee_type_is_space_method = patch(
            'api.utilities.helpers.bulk_asset_helper.BulkAssetHelper.handle_assignee_type_when_is_space'
        )
        method_mock = mock_assignee_type_is_space_method.start()
        method_mock.return_value = '666'
        new_user.save()
        del multiple_assets["assetCategoryId"]
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        for asset in response_json["data"]:
            asset["errors"]["assetCategoryId"] == \
            [serial_dict["required_field"].format("assetCategoryId")]
        mock_assignee_type_is_space_method.stop()

    def test_create_bulk_assets_with_invalid_repeated_tag_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
       Test create asset with arguments for a used tags and repeated tags
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category(object): Asset category for test
           new_user(object): User object
           multiple_assets(dict): multiple assets dict
       """
        new_user.save()
        for asset in multiple_assets["assets"]:
            asset["assetCategoryId"] = test_asset_category.id
            asset["assigneeId"] = new_user.token_id
            asset["assigneeType"] = AssigneeType.user.value
            asset["tag"] = "AND/634/12"
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["data"][1]["errors"]["tag"] == [
            serial_dict["exists"].format("This tag")
        ]

    def test_create_bulk_assets_with_un_required_attribute_and_unrelated_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
       Test create asset with invalid attributes
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category(object): Asset category for test
           new_user(object): User object
           multiple_assets(dict): multiple assets dict
       """
        new_user.save()
        multiple_assets["assetCategoryId"] = test_asset_category.id
        for index, asset in enumerate(multiple_assets["assets"]):
            asset["assetCategoryId"] = test_asset_category.id
            asset["assigneeId"] = new_user.token_id
            asset["assigneeType"] = AssigneeType.user.value
            asset["tag"] = asset["tag"] + str(index)

        multiple_assets["assets"][0].update({"length": "3", 'colour': 'blue'})
        multiple_assets["assets"][1].update({"waranty": "4", "statu": "done"})
        multiple_assets["assets"][2].update({"length": "3"})
        multiple_assets["assets"][2].pop("waranty")
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["data"]['NonAddedAssets'][0]["errors"][
            "waranty"] == [serial_dict["required_field"].format("waranty")]

    def test_create_bulk_assets_with_no_token_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
       Test create asset unauthorised user
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category(object): Asset category for test
           new_user(object): User object
           multiple_assets(dict): multiple assets dict
       """
        new_user.save()
        for index, asset in enumerate(multiple_assets["assets"]):
            asset["assetCategoryId"] = test_asset_category.id
            asset["assigneeId"] = new_user.token_id
            asset["assigneeType"] = AssigneeType.user.value
            asset["tag"] = "AND/634/12"
            asset["tag"] = asset["tag"] + str(index)
        data = json.dumps(multiple_assets)
        response = client.post(f'{API_BASE_URL_V1}/assets/bulk', data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json["status"] == "error"
        assert response_json["message"] == error_dict["NO_TOKEN_MSG"]

    def test_create_bulk_assets_with_empty_assets_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
       Test create asset with no assets
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category(object): Asset category for test
           new_user(object): User object
           multiple_assets(dict): multiple assets dict
       """
        data = json.dumps([])
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serial_dict["data_type"].format(
            "Assets", "dictionary")

    def test_create_bulk_assets_with_payload_containing_non_dict_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
        Test create asset with payload with non dict
        Args:
            client(FlaskTestClient): used to call endpoints and test
            init_db(SqlAlchemyConnection): USed to sustain the db
            auth_header(dict): Authorisation headers
            test_asset_category(object): Asset category for test
            new_user(object): User object
            multiple_assets(dict): multiple assets dict
        """
        mock_assignee_type_is_space_method = patch(
            'api.utilities.helpers.bulk_asset_helper.BulkAssetHelper.handle_assignee_type_when_is_space'
        )
        method_mock = mock_assignee_type_is_space_method.start()
        method_mock.return_value = '666'
        new_user.save()
        multiple_assets["assetCategoryId"] = test_asset_category.id
        multiple_assets["assets"].append([])
        multiple_assets["assets"].append(1)
        multiple_assets["assets"].append("Category")
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["data"][4]["errors"]["Asset"] == \
               [serial_dict["data_type"].format("Asset", "dictionary")]
        assert response_json["data"][5]["errors"]["Asset"] == \
               [serial_dict["data_type"].format("Asset", "dictionary")]
        assert response_json["data"][6]["errors"]["Asset"] == \
               [serial_dict["data_type"].format("Asset", "dictionary")]
        mock_assignee_type_is_space_method.stop()

    def test_create_bulk_assets_no_assets_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
       Test create asset unauthorised user
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category(object): Asset category for test
           new_user(object): User object
           multiple_assets(dict): multiple assets dict
       """
        new_user.save()
        multiple_assets.pop("assets")
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serial_dict[
            "required_field"].format("Assets payload")

    def test_create_bulk_assets_passing_not_array_fails(
            self, client, init_db, auth_header, new_user, test_asset_category,
            multiple_assets):
        """
       Test create asset unauthorised user
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category(object): Asset category for test
           new_user(object): User object
           multiple_assets(dict): multiple assets dict
       """
        new_user.save()
        multiple_assets["assets"] = {"user": "dennis"}
        data = json.dumps(multiple_assets)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serial_dict["data_type"].format(
            "Assets", "list")

    def test_create_bulk_assets_with_wrong_keys_fails(
            self,
            client,
            init_db,
            test_asset_category_with_custom_fields,
            auth_header,
            new_user,
    ):
        """
       Test create asset with invalid custom attributes
       Args:
           client(FlaskTestClient): used to call endpoints and test
           init_db(SqlAlchemyConnection): USed to sustain the db
           auth_header(dict): Authorisation headers
           test_asset_category_with_custom_fields(object): Asset category for test
           new_user(object): User object
       """

        json_data = {
            "assetCategoryId":
            test_asset_category_with_custom_fields.id,
            "assetCategoryName":
            "Dongles",
            "assets": [{
                "tag": "AND/051/KAS21",
                "assigneeId": new_user.token_id,
                "assigneeType": "user",
                "status": "ok",
                "color": "blue",
                "port": "nothing",
                "usage": "dont know",
                "serialNumber": 909,
                "DateOfPurchase": "nono"
            },
                       {
                           "tag": "AND/051/KAS22",
                           "assigneeId": new_user.token_id,
                           "assigneeType": "use",
                           "status": "ok",
                           "color": "black",
                           "port": "usb,usb-c,hdmi",
                           "usage": "old",
                           "serialNumber": 909,
                           "DateOfPurchase": "2017-06-09"
                       }]
        }

        data = json.dumps(json_data)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        response_json["data"][0]["errors"]["color"] = [
            serial_dict["not_choice"].format("blue", "grey,black")
        ]
        response_json["data"][0]["errors"]["port"] = [
            serial_dict["not_choice"].format("nothing", "usb,usb-c,hdmi,sd")
        ]
        response_json["data"][0]["errors"]["usage"] = serial_dict[
            "not_choice"].format("ont know", "old,new,moderate")
        response_json["data"][0]["errors"]["DateOfPurchase"] = serial_dict[
            "invalid_date"].format("nono")
        response_json["data"][1]["customAttributes"]["color"] = "black"
        response_json["data"][1]["customAttributes"]["port"] = "usb,usb-c,hdmi"
        response_json["data"][1]["customAttributes"]["usage"] = "old"
        response_json["data"][1]["customAttributes"][
            "DateOfPurchase"] = "2017-06-09"

    def test_create_bulk_assets_with_payload_containing_no_assigneeId_pass(
            self, client, init_db, auth_header, new_space_two,
            test_asset_category, multiple_assets2):
        """
            Test create asset with payload with non dict
            Args:
                client(FlaskTestClient): used to call endpoints and test
                init_db(SqlAlchemyConnection): USed to sustain the db
                auth_header(dict): Authorisation headers
                test_asset_category(object): Asset category for test
                new_space_two(object): Space object
                multiple_assets(dict): multiple assets dict
        """
        new_space_two.save()
        mock_assignee_type_is_space_method = patch(
            'api.utilities.helpers.bulk_asset_helper.BulkAssetHelper.handle_assignee_type_when_is_space'
        )
        method_mock = mock_assignee_type_is_space_method.start()
        method_mock.return_value = new_space_two.id
        multiple_assets2["assetCategoryId"] = test_asset_category.id
        for asset in multiple_assets2["assets"]:
            asset["assigneeId"] = method_mock()
            asset["assigneeType"] = AssigneeType.space.value
            asset["centerId"] = new_space_two.center_id
        data = json.dumps(multiple_assets2)
        response = client.post(
            f'{API_BASE_URL_V1}/assets/bulk', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES['created'].format(
            'Multiple assets')
        assert len(response_json["data"]["AddedAssets"]) == 2
        mock_assignee_type_is_space_method.stop()

    def test_handle_assignee_type_when_is_space_method(self, new_space_two,
                                                       multiple_assets2):
        """
            Test that the handle_assignee_type_when_is_space method adds assigneeId to the payload
            when assigneeType is space 
            Args:
                new_space_two(object): Space object
                multiple_assets2(dict): multiple assets dict
        """
        asset_helper_instance = BulkAssetHelper(multiple_assets2, AssetSchema)
        asset_helper_instance.handle_assignee_type_when_is_space(
            multiple_assets2, new_space_two)
        assert 'assigneeId' in multiple_assets2
        assert multiple_assets2['assigneeId'] == new_space_two.id
