"Module for asset category endpoint test"

from urllib.parse import urlparse
from copy import deepcopy

from flask import json  # pylint: disable=E0401

# models
from api.models import AssetCategory, Asset, Attribute
from api.models.asset_category import Priority

# constants
from api.utilities.constants import CHARSET

# messages
from api.utilities.messages.error_messages import (serialization_errors,
                                                   query_errors, filter_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.enums import InputControlChoiceEnum

# app config
from config import AppConfig

# mock data
from tests.mocks.asset_category import (
    valid_asset_category_data, valid_asset_category_data_with_attr_keys,
    invalid_asset_category_data, valid_asset_category_data_without_attributes,
    valid_asset_category_data_with_subcategory,
    asset_category_data_without_choices,
    asset_category_with_two_wrong_input_control,
    asset_category_with_one_wrong_input_control,
    asset_category_with_choices_as_a_string, new_asset_category_data,
    asset_category_data_without_image,
    valid_asset_category_data_with_sub_categories,
    asset_category_data_without_image_url, valid_sub_category_data,
    asset_category_data_without_image_public_id)

api_v1_base_url = AppConfig.API_BASE_URL_V1  # pylint: disable=C0103


class TestAssetCategoriesEndpoints:  # pylint: disable=R0904
    """"
    Asset Category endpoints test
    """

    def test_create_asset_category_with_invalid_priority_fails(
            self, init_db, client, auth_header, new_user):
        new_user.save()
        payload = deepcopy(valid_asset_category_data)
        payload['priority'] = 'invalid'
        data = json.dumps(payload)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["errors"]["priority"][0] == \
            serialization_errors['invalid_priority']
        assert response_json["status"] == "error"

    def test_update_asset_category_with_invalid_priority_fails(
            self, client, auth_header, init_db):
        asset_category = AssetCategory(name="TestLaptop")
        asset_category.save()
        payload = deepcopy(valid_asset_category_data_without_attributes)
        payload['priority'] = 'invalid'
        data = json.dumps(payload)
        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["errors"]["priority"][0] == \
            serialization_errors['invalid_priority']
        assert response_json["status"] == "error"

    def test_create_asset_categories_endpoint_with_duplicate_valid_data_fails(  # pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """Should fail when an already existing asset category name is provided
        Args:
            client (func): Fixture to get flask test client
            new_asset_category (func): fixture to create a new asset category
            init_db (func): Fixture to initialize the test database
            auth_header (dict): Fixture to get token.
        Returns:
            None
        """
        new_asset_category.save()

        data = json.dumps(new_asset_category_data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'exists'].format('laptop')

    def test_asset_categories_stats_endpoint(  # pylint: disable=C0103,R0913,R0201
            self,
            client,
            new_user,
            new_asset_category,
            init_db,  # pylint: disable=W0613
            auth_header,
            request_ctx,  # pylint: disable=W0613
            mock_request_two_obj_decoded_token):  # pylint: disable=W0613
        """
        Should pass when getting asset categories stats
        """
        new_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0
        assert response_json["data"][0]["name"] == "Laptop"
        new_asset_category.delete()

    def test_create_asset_categories_endpoint_with_valid_data(  # pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """
        Should pass when valid data is provided
        """

        data = json.dumps(valid_asset_category_data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["data"]["name"] == valid_asset_category_data[
            "name"]
        assert response_json["data"][
            "runningLow"] == valid_asset_category_data["runningLow"]
        assert response_json["data"][
            "lowInStock"] == valid_asset_category_data["lowInStock"]
        assert response_json['data']["id"] != ""
        assert response_json["data"][
            "customAttributes"] == valid_asset_category_data[
                "customAttributes"]
        assert response_json["data"]["priority"] == \
            Priority.not_key.value.title()
        assert response_json["status"] == "success"

    def test_create_asset_categories_endpoint_with_subcategories_success(  # pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """
        Should pass when valid data is provided
        """

        data = json.dumps(valid_asset_category_data_with_sub_categories)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["data"]
        ["name"] == valid_asset_category_data_with_sub_categories["name"]
        assert response_json['data']["id"] != ""
        assert response_json["data"][
            "customAttributes"] == \
            valid_asset_category_data_with_sub_categories[
                "customAttributes"]
        assert response_json["status"] == "success"

    def test_create_asset_categories_without_image_fails(  # pylint: disable=C0103,R0201
            self, client, init_db, auth_header):  # pylint: disable=W0613
        """
        Test creating an asset category without an image fails
        Args:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db (SQLAlchemy): fixture to initialize the test database
        """

        data = json.dumps(asset_category_data_without_image)

        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["image"][0] == serialization_errors[
            "field_required"]

    def test_create_asset_categories_without_image_url_fails(  # pylint: disable=C0103,R0201
            self, client, init_db, auth_header):  # pylint: disable=W0613
        """
        Test creating an asset category without an image fails
        Args:
            client(object): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db (SQLAlchemy): fixture to initialize the test database
        """

        data = json.dumps(asset_category_data_without_image_url)

        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            "image_url_and_public_id_missing"]

    def test_create_asset_categories_without_image_public_id_fails(  # pylint: disable=C0103,R0201
            self, client, init_db, auth_header):  # pylint: disable=W0613
        """
            Test creating an asset category with an image missing public_id fails
            Args:
                client(object): fixture to get flask test client
                auth_header(dict): fixture to get token
                init_db (SQLAlchemy): fixture to initialize the test database
            """

        data = json.dumps(asset_category_data_without_image_public_id)

        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            "image_url_and_public_id_missing"]

    def test_create_asset_categories_endpoint_with_valid_data_without_attributes(  # pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  # #pylint: disable=W0613
        """
        Should fail when valid data without attributes is provided
        """
        data = valid_asset_category_data_without_attributes
        data["name"] = "Seun"
        data = json.dumps(data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json[
            "message"] == "Please provide at least one attribute"
        assert response_json["status"] == "error"

    def test_create_asset_categories_endpoint_without_asset_category_name(  # pylint: disable=R0201,C0103
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """
        Should fail when asset category name is not data is provided
        """

        data = json.dumps({})
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["name"][0] == serialization_errors[
            "field_required"]

    def test_create_asset_categories_endpoint_with_invalid_attributes_data(  # pylint: disable=R0201, C0103
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """
        Should fail when invalid attributes data is provided
        """

        data = invalid_asset_category_data
        data["name"] = "cat"
        data = json.dumps(data)

        data = json.dumps(invalid_asset_category_data)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["0"]["label"][
            0] == serialization_errors["field_required"]

    def test_update_asset_category(self, client, init_db, auth_header):  # pylint: disable=R0201,W0613
        """
            Test to Update an asset category without attribute
        """
        asset_category = AssetCategory(name="TestLaptop")
        asset_category.save()
        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["data"]["priority"] == \
            Priority.not_key.value.title()
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"]["customAttributes"], list)

    def test_update_asset_category_with_subcategory(self, client, init_db,
                                                    auth_header):
        """
            Test to update an asset with a sub category
        """
        asset_category = AssetCategory(name="TestLaptop")
        asset_category.save()
        data = json.dumps(valid_asset_category_data_with_subcategory)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"]["customAttributes"], list)
        assert isinstance(response_json["data"]["subCategories"], list)
        assert response_json["data"]["subCategories"][0][
            "name"] == valid_asset_category_data_with_subcategory[
                "subCategories"][0]["name"]

    def test_update_asset_category_with_two_wrong_input_controls(  # pylint: disable=R0201,C0103
            self, client, init_db, auth_header):  # pylint: disable=W0613
        """
        Test to Update an asset category without choices with two wrong input
        controls
        """
        asset_category = AssetCategory(name="TestLaptop b")
        asset_category.save()
        data = json.dumps(asset_category_with_two_wrong_input_control)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "An error occurred"
        assert response_json["errors"]["0"]["inputControl"][0] == \
            serialization_errors["input_control"].format(
                input_controls=str(InputControlChoiceEnum.get_all_choices()).strip('[]'))
        assert response_json["errors"]["1"]["inputControl"][0] == \
            serialization_errors["input_control"].format(
                input_controls=str(InputControlChoiceEnum.get_all_choices()).strip('[]'))

    def test_update_asset_category_with_one_wrong_input_controls(  # pylint: disable=R0201,C0103
            self, client, init_db, auth_header):  # pylint: disable=W0613
        """
        Test to Update an asset category without choices with one wrong input
        controls
        """
        asset_category = AssetCategory(name="TestLaptop b2")
        asset_category.save()
        data = json.dumps(asset_category_with_one_wrong_input_control)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "An error occurred"
        assert response_json["errors"]["1"]["inputControl"][0] == \
            serialization_errors["input_control"].format(
                input_controls=str(InputControlChoiceEnum.get_all_choices()).strip('[]'))

    def test_update_asset_category_without_choices(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613,C0103
            auth_header):
        """
        Test to Update an asset category without choices when multichoice
        input controls are selected
        """
        asset_category = AssetCategory(name="TestLaptop A")
        asset_category.save()
        data = json.dumps(asset_category_data_without_choices)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["errors"]["1"]["choices"][
            0] == serialization_errors['choices_required']  # pylint: disable=line-too-long

    def test_update_asset_category_with_fake_id(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Test to Update an asset category with fake id
        """

        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/-llllllll',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_update_asset_category_with_invalid_id(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Test to Update an asset category with invalid id
        """

        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/-llll@@@llll',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_update_asset_category_with_attribute(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Test to Update an asset category with an attribute
        """
        asset_category = AssetCategory(name="TestLaptop")
        attribute_data = valid_asset_category_data_with_attr_keys[
            "customAttributes"][0]
        attribute_data["_key"] = attribute_data["key"]
        attribute_data["is_required"] = attribute_data["isRequired"]
        attribute_data["input_control"] = attribute_data["inputControl"]
        attribute_data.__delitem__("key")
        attribute_data.__delitem__("isRequired")
        attribute_data.__delitem__("inputControl")
        attribute = Attribute(**attribute_data)
        asset_category.attributes.append(attribute)
        asset_category.save()

        attribute_data["id"] = attribute.id
        data = json.dumps({"attributes": [attribute_data]})

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]["customAttributes"]) > 0

    def test_update_asset_categories_with_duplicate_name(
            self, client, init_db, auth_header):
        """
            Test to handle the duplicate asset categories name
        """
        asset_category = AssetCategory.query.filter_by(name="Headset").first()
        data = json.dumps(valid_asset_category_data_without_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == "Seun already exists"

    def test_add_attributes_to_asset_categories_should_be_succesful_when_all_contions_are_met(
            self, client, init_db, auth_header):
        """
        Should return a 200 success when all the conditions
        are met
        """
        asset_category = AssetCategory(name="Headset")
        asset_category.save()
        data = json.dumps(valid_asset_category_data)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES["updated"].format(
            "Asset")
        assert isinstance(response_json["data"]["customAttributes"], list)
        assert len(response_json["data"]["customAttributes"]) == 2
        assert response_json["data"]["customAttributes"][0][
            'label'] == valid_asset_category_data["customAttributes"][0][
                'label']
        assert "id" in response_json["data"]["customAttributes"][0]
        assert "id" in response_json["data"]["customAttributes"][1]
        assert "choices" in response_json["data"]["customAttributes"][1]

    def test_add_attributes_to_asset_categories_should_fail_when_invalid_attributes_are_used(
            self, client, init_db, auth_header):
        """
        Should return a 400 error code when an invalid attribute
        is tried to be updated
        """
        asset_category = AssetCategory(name="Headsettt")
        asset_category.save()
        data = json.dumps(asset_category_with_one_wrong_input_control)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['errors']['1']['inputControl'][
            0] == serialization_errors["input_control"].format(
                input_controls=str(
                    InputControlChoiceEnum.get_all_choices()).strip('[]'))

    def test_add_attributes_to_asset_categories_should_be_succesful_when_updating_and_adding_attributes(
            self, client, init_db, auth_header):
        """
        Should return a 200 success code when updating and adding a new attribute
        """
        asset_category = AssetCategory(name="Headset")
        attribute_data = valid_asset_category_data_with_attr_keys[
            "customAttributes"][0]
        attribute = Attribute(**attribute_data)
        asset_category.attributes.append(attribute)
        asset_category.save()

        new_attributes = {
            "name":
            "New Category",
            "customAttributes": [{
                "id": attribute.id,
                "label": "color",
                "is_required": True,
                "inputControl": "dropdown",
                "choices": ["blue", "red", "black"]
            },
                                 {
                                     "label": "size",
                                     "isRequired": True,
                                     "_key": 'color',
                                     "inputControl": "textarea",
                                 }]
        }
        data = json.dumps(new_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES["updated"].format(
            "Asset")
        assert response_json["data"]["name"] == new_attributes["name"]
        assert len(response_json["data"]["customAttributes"]) == 2
        assert response_json["data"]["customAttributes"][1][
            "label"] == new_attributes["customAttributes"][1]["label"]
        assert response_json["data"]["customAttributes"][1][
            "inputControl"] == new_attributes["customAttributes"][1][
                "inputControl"]
        assert "id" in response_json["data"]["customAttributes"][1]
        assert response_json["data"]["customAttributes"][0][
            "id"] == attribute.id
        assert response_json["data"]["customAttributes"][0][
            "label"] == new_attributes["customAttributes"][0]["label"]
        assert response_json["data"]["customAttributes"][0][
            "inputControl"] == new_attributes["customAttributes"][0][
                "inputControl"]

    def test_add_attribute_should_fail_when_invalid_attribute_id_is_used(
            self, client, init_db, auth_header):
        """
        Should return a 400 error code when the attribute id is invalid
        """
        asset_category = AssetCategory(name="new asset categoryII")
        attribute_data = valid_asset_category_data_with_attr_keys[
            "customAttributes"][0]
        attribute = Attribute(**attribute_data)
        asset_category.attributes.append(attribute)
        asset_category.save()

        new_attributes = {
            "name":
            "new asset categoryII",
            "customAttributes": [{
                "id": "!@!!!%",
                "label": "color",
                "is_required": True,
                "inputControl": "dropdown",
                "choices": ["blue", "red", "black"]
            }]
        }
        data = json.dumps(new_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['errors']['0']['id'][0] == serialization_errors[
            'invalid_id_field'].format(
                new_attributes['customAttributes'][0]['id'])

    def test_add_attribute_should_fail_when_wrong_attribute_id_is_provided(
            self, client, init_db, auth_header):
        """
        Should return a 400 error code when wrong attribute id is used
        """
        asset_category = AssetCategory(name="New categoryI")
        attribute_data = valid_asset_category_data_with_attr_keys[
            "customAttributes"][0]
        attribute = Attribute(**attribute_data)
        asset_category.attributes.append(attribute)
        asset_category.save()

        new_attributes = {
            "name":
            "New categoryI",
            "customAttributes": [{
                "id": asset_category.id,
                "label": "color",
                "is_required": True,
                "inputControl": "textarea",
            }]
        }
        data = json.dumps(new_attributes)

        response = client.patch(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header,
            data=data)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'attribute_not_related'].format(
                attribute_id=new_attributes['customAttributes'][0]['id'],
                asset_category_id=asset_category.id)

    def test_get_one_asset_category(self, client, init_db, auth_header):  # pylint: disable=R0201,W0613
        """
        Tests that a single asset category can be retrieved
        """
        asset_category = AssetCategory(name="TestLaptop1")
        asset_category.save()
        sub_category = AssetCategory(
            name="TestLaptop1", description="mac", parent_id=asset_category.id)
        sub_category.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["data"]["name"] == "TestLaptop1"
        assert type(response_json["data"]["customAttributes"]) == list
        assert type(response_json["data"]["subCategories"]) == list
        assert response_json["data"]["subCategories"][0][
            'description'] == "mac"
        assert response_json["data"]["subCategories"][0]['assetsCount'] == 0
        assert response_json["data"]["subCategories"][0][
            'name'] == "TestLaptop1"

    def test_get_one_asset_category_with_attributes(
            self, client, init_db, auth_header, test_single_asset_category):  # pylint: disable=R0201,W0613
        """
        Tests a single asset category with attributes can be retrieved
        """
        asset_category = test_single_asset_category.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"]["customAttributes"], list)
        assert isinstance(
            response_json['data']["customAttributes"][1]["choices"], list)
        assert response_json['data']["customAttributes"][1]['choices'] == [
            '{Green', 'Red}'
        ]

    def test_get_one_asset_category_not_found(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Tests that 404 is returned for an asset category that does not exist
        """
        asset_category = AssetCategory(name="TestLaptop2")
        asset_category.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/-L2', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_get_one_asset_category_invalid_id(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Tests that 400 is returned for an invalid id
        """
        asset_category = AssetCategory(name="TestLaptop3")
        asset_category.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/L@@', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_delete_asset_category(self, client, init_db, auth_header):  # pylint: disable=R0201,W0613,C0103
        """
            Tests that a single asset category can be deleted
        """
        asset_category = AssetCategory(
            name="TestLaptop4", image={'public_id': 'some_public_id'})
        asset_category.save()

        response = client.delete(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"

    def test_delete_asset_category_and_dependent_resources(
            self, client, init_db, auth_header,
            new_asset_category_subcategory_asset):  #pylint: disable=R0201,W0613,C0103
        """
            Tests that a single asset category, its sub categories and 
            associated assets can be deleted
        """

        asset_category = new_asset_category_subcategory_asset
        response = client.delete(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"

    def test_delete_asset_category_not_found(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Tests that 404 is returned for a category that does not exist on delete
        """

        response = client.delete(
            f'{api_v1_base_url}/asset-categories/-L2', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_delete_asset_category_invalid_id(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Tests that 400 is returned when id is invalid
        """
        asset_category = AssetCategory(name="TestLaptop5")
        asset_category.save()

        response = client.delete(
            f'{api_v1_base_url}/asset-categories/LX@', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_get_assets_for_non_exisiting_category(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header):
        """
        Should return an 404 reponse when a wrong id is provided
        """

        asset_category_id = "wrongid"

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_get_asset_category_with_no_assets(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header_two):
        """
        Should return an empty list if no assets belong to an asset category
        """
        asset_category = AssetCategory(name="Apple Tv 1")
        asset_category.save()

        asset_category_id = asset_category.id

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets?include=deleted',
            headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 0
        assert response_json["message"] == serialization_errors[
            "asset_category_assets"].format(asset_category.name)

    def test_get_asset_category_assets(self, client, init_db, auth_header_two,
                                       new_user):  # pylint: disable=R0201,W0613,C0103
        """
        Should return lists of assets that belongs to an asset category
        """
        asset_category = AssetCategory(name="Apple Tv 2")
        new_user.save()
        asset = Asset(
            tag="abc", assignee_id=new_user.token_id, assignee_type='user')
        asset_category.assets.append(asset)
        asset_category.save()
        asset_category_id = asset_category.id

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets',
            headers=auth_header_two)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json["data"]) != 0
        assert response_json["message"] == serialization_errors[
            "asset_category_assets"].format(asset_category.name)

    def test_asset_categories_list_endpoint_succeeds(  # pylint: disable=R0201,C0103
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            asset_categories):
        """
        Test to asset asset_category list endpoint
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            asset_categories (BaseModel): fixture for querying all asset categories
        Returns:
            Assertion: Succeeds
        """
        asset_category = asset_categories.order_by(
            AssetCategory.created_at.desc()).first()

        response = client.get(
            f'{api_v1_base_url}/asset-categories', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0
        assert response_json["data"][0]["name"] == asset_category.name

    def test_asset_categories_list_endpoint_args(self, client, auth_header):  # pylint: disable=R0201,W0613,C0103,C0111
        asset_category = AssetCategory(name="Laptop6")
        asset_category2 = AssetCategory(name="Chairs")
        asset_category.save()
        asset_category2.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,like,chairs',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is 1
        assert response_json["data"][0]["name"] == "Chairs"

        invalid_response = client.get(
            f'{api_v1_base_url}/asset-categories?where=name,like.chairs',
            headers=auth_header)
        invalid_response_json = json.loads(
            invalid_response.data.decode(CHARSET))

        assert invalid_response.status_code == 400
        assert invalid_response_json["status"] == "error"
        asset_category.delete()
        asset_category2.delete()

    def test_eager_load_attributes(  # pylint: disable=R0201,C0103,C0111
            self,
            client,
            init_db,
            test_asset_category,  # pylint: disable=W0613
            auth_header):
        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"][0]["customAttributes"], list)
        assert len(response_json["data"][0]["customAttributes"]) is not 0

    def test_eager_load_attributes_with_invalid_param(  # pylint: disable=R0201,W0613,C0103,C0111
            self, client, auth_header, test_asset_category):  # pylint: disable=W0613

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert "customAttributes" in response_json["data"][0]

    def test_paginates_asset_categories_with_one_item(
            self, init_db, client, auth_header, new_asset_category):
        """
        Test paginating asset categories with a single data
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?page=1&limit=1',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json['data']) == 1

        assert urlparse(
            response_json["meta"]["nextPage"]).query == "page=2&limit=1"
        assert "page=1&limit=1" in response_json["meta"]["firstPage"]
        assert "page=1&limit=1" in response_json["meta"]["currentPage"]

    def test_asset_categories_pagination(self, init_db, client, auth_header):
        """
        Test paginating asset categories
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?page=1&limit=2',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert len(response_json['data']) == 2
        assert 'meta' in response_json
        assert 'currentPage' in response_json['meta']
        assert 'nextPage' in response_json['meta']
        assert 'previousPage' in response_json['meta']
        assert response_json['meta']['currentPage'].endswith('page=1&limit=2')
        assert len(response_json['meta']) == 7
        assert isinstance(response_json["meta"], dict)

    def test_paginate_asset_category_with_bad_query(self, init_db, client,
                                                    auth_header):
        """
        Test paginating asset category with bad query 'page=one'
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?page=one&limit=2',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('page', 'one')

    def test_paginate_asset_category_with_eager_attributes(
            self, init_db, client, auth_header, test_asset_category):
        """
        Test asset categories returns atrributes and is still paginated
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?page=1&limit=2&include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert "customAttributes" in response_json["data"][0]
        assert isinstance(response_json["data"][0]["customAttributes"], list)

    def test_sort_asset_category_with_invalid_order_query_fail(
            self,
            init_db,  # pylint: disable=W0613
            client,
            auth_header):
        """
        Test sorting asset category with invalid query 'order=descending'
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            Assertion: Fails
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?order=descending',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('order', 'descending')

    def test_sort_asset_category_with_invalid_sort_query_fail(
            self,
            init_db,  # pylint: disable=W0613
            client,
            auth_header):
        """
        Test sorting asset category with invalid sort query 'sort=invalid_column'
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            Assertion: Fails
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?sort=invalid_column',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == query_errors[
            'invalid_query_non_existent_column'].format(
                'invalid_column', 'AssetCategory')

    def test_sort_asset_category_with_valid_query_succeed(
            self,
            init_db,  # pylint: disable=W0613
            client,
            auth_header,
            asset_categories):
        """
        Test sorting asset category with valid query 'sort=asc' & 'sort=desc'
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            asset_categories (BaseModel): fixture for querying all asset categories
        Returns:
            Assertion: Succeeds
        """

        asc_asset_category = asset_categories.order_by(
            AssetCategory.id.asc()).first()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?sort=id&order=asc',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["data"][0]["name"] == asc_asset_category.name

        desc_asset_category = asset_categories.order_by(
            AssetCategory.id.desc()).first()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?sort=id&order=desc',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["data"][0]["name"] == desc_asset_category.name

    def test_sort_asset_category_with_attributes_succeed(
            self,
            init_db,  # pylint: disable=W0613
            client,
            auth_header):
        """
        Test asset categories returns atrributes and is still sorted
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_permissions (BaseModel): fixture for creating a permissions
        Returns:
            Assertion: Succeeds
        """
        response = client.get(
            f'{api_v1_base_url}/asset-categories?sort=id&order=asc&include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert "customAttributes" in response_json["data"][0]
        assert isinstance(response_json["data"][0]["customAttributes"], list)

    def test_get_asset_categories_with_stats_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a list of asset categories with side loaded stats
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        ok_stats = response_json['data'][0]['stats']['ok']
        not_ok_stats = response_json['data'][0]['stats']['notOk']
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' in response_json['data'][0]
        assert 'ok' in response_json['data'][0]['stats']
        assert 'notOk' in response_json['data'][0]['stats']
        assert 'totalAssets' in ok_stats
        assert 'assigned' in ok_stats
        assert 'stockCount' in ok_stats
        assert 'totalAssets' in not_ok_stats
        assert 'assigned' in not_ok_stats
        assert 'stockCount' in not_ok_stats
        assert 'space' in ok_stats['assigned']
        assert 'people' in ok_stats['assigned']
        assert 'total' in ok_stats['assigned']
        assert 'expectedBalance' in ok_stats['stockCount']
        assert 'actualBalance' in ok_stats['stockCount']
        assert 'difference' in ok_stats['stockCount']
        assert isinstance(response_json['data'], list)
        assert isinstance(ok_stats, dict)
        assert isinstance(not_ok_stats, dict)
        assert isinstance(ok_stats['assigned'], dict)
        assert isinstance(ok_stats['stockCount'], dict)
        assert isinstance(ok_stats['stockCount']['actualBalance'], dict)

    def test_get_asset_categories_with_stats_query_in_any_casing_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a list of
        asset categories side-loaded with stats
        wether upper or lower case query 'include=StAtS'
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=StAtS',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        ok_stats = response_json['data'][0]['stats']['ok']
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' in response_json['data'][0]
        assert 'ok' in response_json['data'][0]['stats']
        assert 'totalAssets' in ok_stats
        assert 'assigned' in ok_stats
        assert 'stockCount' in ok_stats
        assert 'space' in ok_stats['assigned']
        assert 'people' in ok_stats['assigned']
        assert 'total' in ok_stats['assigned']
        assert 'expectedBalance' in ok_stats['stockCount']
        assert 'actualBalance' in ok_stats['stockCount']
        assert 'difference' in ok_stats['stockCount']
        assert isinstance(response_json['data'], list)
        assert isinstance(ok_stats, dict)
        assert isinstance(ok_stats['assigned'], dict)
        assert isinstance(ok_stats['stockCount'], dict)
        assert isinstance(ok_stats['stockCount']['actualBalance'], dict)

    def test_get_asset_categories_with_stats_and_attributes_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a list of
        asset categories side-loaded stats and attributes
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&include=attributes',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' in response_json['data'][0]
        assert 'customAttributes' in response_json['data'][0]
        assert isinstance(response_json['data'], list)
        assert isinstance(response_json['data'][0]['stats'], dict)
        assert isinstance(response_json['data'][0]['customAttributes'], list)

    def test_get_asset_categories_with_stats_and_pagination_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a paginated list of
        asset categories side-loaded with stats
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&page=1&limit=3',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' in response_json['data'][0]
        assert len(response_json['data']) == 3
        assert isinstance(response_json['data'], list)
        assert isinstance(response_json['data'][0]['stats'], dict)

    def test_get_asset_categories_with_stats_attributes_and_pagination_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a paginated list of
        asset categories side-loaded with stats and customAttributes
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&include=attributes&page=1&limit=2',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' in response_json['data'][0]
        assert len(response_json['data']) == 2
        assert 'customAttributes' in response_json['data'][0]
        assert isinstance(response_json['data'], list)
        assert isinstance(response_json['data'][0]['stats'], dict)
        assert isinstance(response_json['data'][0]['customAttributes'], list)

    def test_get_asset_categories_with_wrong_stats_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and a list of
        asset categories without stats when query is invalid
        'include=statiiiii'
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=statiiiii',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' not in response_json['data'][0]
        assert 'customAttributes' not in response_json['data'][0]
        assert isinstance(response_json['data'], list)

    def test_get_asset_categories_with_invalid_query_parameter_fails(
            self, client, init_db, auth_header):
        """
        Should return a 400 response code and error message when an
        invalid parameter entered in the query
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?includegggg=stats',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert 'Invalid URL query' in response_json['message']

    def test_get_asset_categories_with_stats_and_invalid_sort_parameter_fails(
            self, client, init_db, auth_header):
        """
        Should return a 400 response code and error message when an
        invalid sort parameter is provided along with stats params
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&sort=novalid',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'invalid_query_strings'].format('sort query', 'novalid')

    def test_get_one_asset_category_with_attributes_and_side_loaded_stats_succeeds(
            self, client, init_db, auth_header, test_single_asset_category2):  # pylint: disable=R0201,W0613
        """
        Should return 200 and single asset category with attributes and side-loaded with stats
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            test_single_asset_category2 (Asset_Category): Fixture for getting
                test asset category data
        Returns:
            None
        """
        asset_category = test_single_asset_category2.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}?include=stats',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        ok_stats = response_json['data']['stats']['ok']
        customAttributes = response_json['data']['customAttributes']
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert 'stats' in response_json['data']
        assert 'ok' in response_json['data']['stats']
        assert 'totalAssets' in ok_stats
        assert 'assigned' in ok_stats
        assert 'stockCount' in ok_stats
        assert 'space' in ok_stats['assigned']
        assert 'people' in ok_stats['assigned']
        assert 'total' in ok_stats['assigned']
        assert 'expectedBalance' in ok_stats['stockCount']
        assert 'actualBalance' in ok_stats['stockCount']
        assert 'difference' in ok_stats['stockCount']
        assert isinstance(response_json['data'], dict)
        assert isinstance(ok_stats, dict)
        assert isinstance(ok_stats['assigned'], dict)
        assert isinstance(ok_stats['stockCount'], dict)
        assert isinstance(ok_stats['stockCount']['actualBalance'], dict)
        assert isinstance(customAttributes, list)
        assert isinstance(customAttributes[1]["choices"], list)
        assert customAttributes[1]['choices'] == ['{Green', 'Red}']

    def test_get_one_asset_category_with_stats_query_in_any_casing_succeeds(
            self, client, init_db, auth_header):  # pylint: disable=R0201,W0613
        """
        Should return a 200 response code and a single asset category side-loaded
        with stats wether upper or lower case query 'include=StAtS'
        """
        asset_category = AssetCategory(name="TestCategory").save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}?include=stATS',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        ok_stats = response_json['data']['stats']['ok']
        customAttributes = response_json['data']['customAttributes']
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert 'stats' in response_json['data']
        assert 'ok' in response_json['data']['stats']
        assert 'totalAssets' in ok_stats
        assert 'assigned' in ok_stats
        assert 'stockCount' in ok_stats
        assert 'space' in ok_stats['assigned']
        assert 'people' in ok_stats['assigned']
        assert 'total' in ok_stats['assigned']
        assert 'expectedBalance' in ok_stats['stockCount']
        assert 'actualBalance' in ok_stats['stockCount']
        assert 'difference' in ok_stats['stockCount']
        assert isinstance(response_json['data'], dict)
        assert isinstance(ok_stats, dict)
        assert isinstance(ok_stats['assigned'], dict)
        assert isinstance(ok_stats['stockCount'], dict)
        assert isinstance(ok_stats['stockCount']['actualBalance'], dict)
        assert isinstance(customAttributes, list)

    def test_get_an_asset_category_with_wrong_stats_query_succeeds(
            self, client, init_db, auth_header):
        """
        Should return a 200 response code and an asset category
        without stats when query value is invalid 'include=statiiiii'
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        asset_category = AssetCategory(name="NewCategory").save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category.id}?include=statiiiii',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert 'stats' not in response_json['data']
        assert 'customAttributes' in response_json['data']
        assert isinstance(response_json['data'], dict)

    def test_asset_categories_with_dynamic_filters_succeeds(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and dynamic filter
        Should return only asset categories that match the filter
        query
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&name=TestLaptop3',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        asset_category = response_json['data'][0]
        assert response.status_code == 200
        assert asset_category['name'] == 'TestLaptop3'

    def test_asset_categories_with_dynamic_filters_no_match_succeeds(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and dynamic filter
        Should return an empty list when no asset category matches
        dynamic filter value
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&runningLow=1000000000',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) == 0

    def test_asset_categories_with_invalid_dynamic_filters_fails(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and dynamic filter
        Should return a 400 response code and error message when an
        invalid when filter key is not valid
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&unknown=TestLaptop3',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == query_errors[
            'invalid_query_non_existent_column'].format(
                'unknown', 'AssetCategory')

    def test_asset_categories_with_where_filters_succeeds(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and where filters
        Should return only asset categories that match the where filter
        values query
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&where=lowInStock,ge,0&where=assetsCount,eq,0',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        asset_category = response_json['data'][0]
        assert response.status_code == 200
        assert asset_category['lowInStock'] >= 0
        assert asset_category['assetsCount'] == 0

    def test_asset_categories_with_where_filter_no_match_succeeds(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and where filter
        Should return an empty list when no asset category matches
        where filter value
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f"{api_v1_base_url}/asset-categories?include=stats&where=name,eq,'Canesuger'",
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) == 0

    def test_asset_categories_with_invalid_where_filters_fails(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and where filter
        Should return a 400 response code and error message when an
        invalid when where filter key is not valid
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats&where=noField,eq,33',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == filter_errors[
            'INVALID_COLUMN'].format('no_field')

    def test_create_asset_categories_endpoint_single_input_control_and_choices(  # pylint: disable=C0103,R0201
            self, client, new_asset_category, init_db, auth_header):  # pylint: disable=W0613
        """
        Should not pass when choices is a set and not a list
        new_asset_category (BaseModel): fixture for creating a new asset category
        Returns:
            Assertion: Succeeds
        """

        data = json.dumps(asset_category_with_choices_as_a_string)
        response = client.post(
            f'{api_v1_base_url}/asset-categories',
            data=data,
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert 'choices' not in response_json['data']['customAttributes'][0]

    def test_asset_categories_with_valid_where_lt_filters_success(
            self, client, init_db, auth_header):
        """Test asset categories endpoint with stats and where filter
        Should return a 200 response code
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats?where=runningLow,lt,450',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json["data"], list)

    def test_asset_categories_with_valid_where_gt_filters_success(
            self, client, init_db, auth_header):
        """
        Test asset categories endpoint with stats and where filter
        Should return a 200 response code
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
        Returns:
            None
        """

        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats?where=lowInStock,gt,450',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert isinstance(response_json["data"], list)

    def test_asset_categories_stats_with_include_deleted_params(  # pylint: disable=C0103,R0913,R0201
            self,
            client,
            new_asset_category,
            init_db,  # pylint: disable=W0613
            auth_header,
            request_ctx,  # pylint: disable=W0613
            mock_request_two_obj_decoded_token):  # pylint: disable=W0613
        """
        Should pass when getting asset categories stats
        """

        new_asset_category.save()
        new_asset_category.delete()
        response = client.get(
            f'{api_v1_base_url}/asset-categories/stats?include=deleted',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        for stat in response_json["data"]:
            assert stat['deleted'] or 'deleted' in stat.keys()
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0

    def test_get_asset_category_deleted_assets(
            self, request_ctx, client, init_db, auth_header,
            mock_request_two_obj_decoded_token, new_user):  # pylint: disable=R0201,W0613,C0103
        """
        Should return lists of assets that belongs to an asset category
        """
        new_user.save()
        asset_category = AssetCategory(
            name="Apple Tv 2", created_by=new_user.token_id)
        asset = Asset(
            tag="abcd",
            assignee_id=new_user.token_id,
            assignee_type='user',
            created_by=new_user.token_id)

        asset_category.assets.append(asset)
        asset_category.save()
        asset.delete()
        asset_category_id = asset_category.id

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{asset_category_id}/assets?include=deleted',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["data"][0]['deleted']
        assert response_json["status"] == "success"
        assert len(response_json["data"]) != 0 and isinstance(
            response_json["data"], list)
        assert response_json["message"] == serialization_errors[
            "asset_category_assets"].format(asset_category.name)

    def test_asset_categories_with_include_deleted_params(  # pylint: disable=C0103,R0913,R0201
            self,
            client,
            new_asset_category,
            init_db,  # pylint: disable=W0613
            auth_header,
            request_ctx,  # pylint: disable=W0613
            mock_request_two_obj_decoded_token):  # pylint: disable=W0613
        """
        Should pass when getting asset categories stats
        """

        new_asset_category.save()
        new_asset_category.delete()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=deleted',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert isinstance(response_json["data"], list)
        assert len(response_json["data"]) is not 0
        for category in response_json["data"]:
            category['deleted'] or 'deleted' in category.keys()

    def test_get_one_asset_category_with_assets(
            self, client, init_db, auth_header_two,
            new_asset_category_with_one_asset):  # pylint: disable=R0201,W0613
        """
        Tests that a single asset category with assets can be retrieved
        """
        new_asset_category_with_one_asset.save()

        response = client.get(
            f'{api_v1_base_url}/asset-categories/{new_asset_category_with_one_asset.id}/assets',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["data"]["name"] == "Laptop0"
        assert response_json[
            "message"] == "Assets for category Laptop0 fetched successfully"
        assert response_json["data"]["subCategoryCount"] == 0
        assert response_json["data"]["assetsCount"] == 1
        assert response_json["data"]["assets"][0]["status"] == "ok"
        assert response_json["data"]["assets"][0]["assignedBy"] == "Ayo"

    def test_get_asset_categories_with_stats_query_by_non_super_user_fails(
            self,
            client,
            init_db,  # pylint: disable=W0613
            auth_header,
            request_ctx,  # pylint: disable=W0613
            mock_request_two_obj_decoded_token,
            new_user,
            auth_header_two):
        """
        Test to get a list of asset categories with side loaded stats 
        by a no `super_user`

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header_two (dict): fixture to get token

        Returns:
            None
        """
        new_user.save()
        response = client.get(
            f'{api_v1_base_url}/asset-categories?include=stats',
            headers=auth_header_two)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json['data'], list)
