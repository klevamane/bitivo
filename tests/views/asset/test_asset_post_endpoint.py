"""Module for asset resource endpoints."""
from flask import json

from api.utilities.helpers.random_string_gen import gen_string
from api.utilities.constants import CHARSET
from api.utilities.enums import AssigneeType
from api.models import Asset
from api.utilities.enums import AssigneeType
from tests.mocks.asset import (
    ASSET_NO_CUSTOM_ATTRS, ASSET_NONEXISTENT_CATEGORY,
    ASSET_INVALID_CATEGORY_ID, ASSET_TWO, ASSET_THREE, ASSET_FOUR, ASSET_FIVE,
    ASSET_NO_TAG)

from api.utilities.messages.error_messages import serialization_errors

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetPostEndpoint:
    """Class for Asset resource POST endpoint."""

    def test_create_asset_with_invalid_category(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_user):
        """
        Tests create asset if the supplied asset_category_id exists
        in the database
         """

        new_user.save()
        ASSET_NONEXISTENT_CATEGORY['assigneeId'] = new_user.token_id
        ASSET_NONEXISTENT_CATEGORY['assigneeType'] = 'user'
        data = json.dumps(ASSET_NONEXISTENT_CATEGORY)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"

    def test_create_asset_with_invalid_category_id(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header):
        """
        Tests if a supplied asset_category_id is in the right format. If it is
        not in the right format, there is no need to make database call
        """

        data = json.dumps(ASSET_INVALID_CATEGORY_ID)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "This asset category id is invalid"

    def test_create_asset_with_missing_tag(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_user):
        """
        Tests if a standard attribute is missing in the supplied asset object.
        The asset cartegory does not have custom_attributes
        """

        new_user.save()
        ASSET_NO_TAG["assigneeId"] = new_user.token_id
        ASSET_NO_TAG["assigneeType"] = AssigneeType.user.value
        ASSET_NO_TAG["assetCategoryId"] = test_asset_category.id
        data = json.dumps(ASSET_NO_TAG)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['attribute_required'].format('tag')

    def test_create_asset_with_valid_data(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_user):
        """
        Test create asset with valid tag for a
        cartegory with no custom attributes
        """
        new_user.save()
        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS["assigneeId"] = new_user.token_id
        ASSET_NO_CUSTOM_ATTRS["assigneeType"] = AssigneeType.user.value
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"

    def test_create_asset_with_space_type_store_returns_assignee_type_of_space(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_space_two):
        """
        Test create asset with space type store returns assignee_type space
        """
        new_space_two.save()
        ASSET_NO_CUSTOM_ATTRS_COPY = ASSET_NO_CUSTOM_ATTRS.copy()
        ASSET_NO_CUSTOM_ATTRS_COPY["tag"] = gen_string()
        ASSET_NO_CUSTOM_ATTRS_COPY["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS_COPY["assigneeId"] = new_space_two.id
        ASSET_NO_CUSTOM_ATTRS_COPY["assigneeType"] = 'space'
        ASSET_NO_CUSTOM_ATTRS_COPY["centerId"] = new_space_two.center_id
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS_COPY)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["data"][
            "assigneeType"] == AssigneeType.space.value

    def test_create_asset_without_custom_attr(  #pylint: disable=C0103
            self,
            auth_header,
            init_db,  #pylint: disable=W0613
            client,
            test_asset_category,
            new_user):
        """
        Test create asset when all standard attributes are supplied and no
        custom attribute is supplied
        """
        new_user.save()
        ASSET_TWO["assetCategoryId"] = test_asset_category.id
        ASSET_TWO["assigneeId"] = new_user.token_id
        ASSET_TWO["assigneeType"] = AssigneeType.user.value
        ASSET_TWO["customAttributes"] = {}
        data = json.dumps(ASSET_TWO)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['attribute_required'].format('waranty')

    def test_create_asset_without_required_custom_attr(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_user):
        """
        Test create asset when the standard atributes and optional custom
        attributes are supplied but required custome attributes are not
        supplied
        """
        new_user.save()
        ASSET_THREE["assetCategoryId"] = test_asset_category.id
        ASSET_THREE["assigneeId"] = new_user.token_id
        ASSET_THREE["assigneeType"] = AssigneeType.user.value
        ASSET_THREE["customAttributes"] = {"length": "15"}
        data = json.dumps(ASSET_THREE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == \
            serialization_errors['attribute_required'].format('waranty')

    def test_create_asset_with_all_custom_attr(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_user):
        """
        Test create asset when all standard and custom attributes are
        supplied
        """
        new_user.save()
        ASSET_THREE["assetCategoryId"] = test_asset_category.id
        ASSET_THREE["assigneeId"] = new_user.token_id
        ASSET_THREE["assigneeType"] = AssigneeType.user.value
        ASSET_THREE["customAttributes"] = {
            "waranty": "expired",
            "length": "100"
        }
        data = json.dumps(ASSET_THREE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "Asset successfully created"

    def test_create_asset_without_optional_custom_attr(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_user):
        """
        Test create asset when standard attributes and required
        custom attribute is supplied. The asset is still created even
        though an optional custom attribute is missing
        """
        new_user.save()
        ASSET_TWO["assetCategoryId"] = test_asset_category.id
        ASSET_TWO["assigneeId"] = new_user.token_id
        ASSET_TWO["assigneeType"] = AssigneeType.user.value
        ASSET_TWO["tag"] = "new tag"
        ASSET_TWO["customAttributes"] = {"waranty": "expired"}
        data = json.dumps(ASSET_TWO)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == "Asset successfully created"

    def test_create_asset_with_unrelated_custom_attr(  #pylint: disable=C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            test_asset_category,
            new_user):
        """
        Test asset creation with an attribute that is neither a standard
        attribute nor custom attribute of the asset category
        """
        new_user.save()
        ASSET_FOUR["assetCategoryId"] = test_asset_category.id
        ASSET_FOUR["assigneeId"] = new_user.token_id
        ASSET_FOUR["assigneeType"] = AssigneeType.user.value
        ASSET_FOUR["customAttributes"] = {
            "color": "indigo",
            "waranty": "expired"
        }
        data = json.dumps(ASSET_FOUR)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "The attribute color is not"\
            " related to this asset category"

    def test_create_asset_with_invalid_request_type(  #pylint: disable=C0103
            self, client, init_db, auth_header_text, test_asset_category):  #pylint: disable=W0613
        """
        Test create asset when all standard and custom attributes are
        supplied
        """
        ASSET_NO_CUSTOM_ATTRS["assetCategoryId"] = test_asset_category.id
        ASSET_NO_CUSTOM_ATTRS["customAttributes"] = {
            "waranty": "expired",
            "length": "100"
        }
        data = json.dumps(ASSET_NO_CUSTOM_ATTRS)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header_text, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Content-Type should be " \
                                           "application/json"

    def test_create_asset_with_duplicate_tag(
            self,
            client,
            init_db,  #pylint: disable=C0103,W0613
            auth_header,
            new_asset_category,
            new_user):
        """
        Test creation of assets with duplicate tag.
        """
        new_user.save()
        new_asset_category.save()
        ASSET_FIVE["asset_category_id"] = new_asset_category.id
        ASSET_FIVE["assignee_id"] = new_user.token_id
        ASSET_FIVE["assignee_type"] = AssigneeType.user.value
        del ASSET_FIVE["assetCategoryId"]
        asset_object = Asset(**ASSET_FIVE)
        asset_object.save()
        del ASSET_FIVE["asset_category_id"]
        del ASSET_FIVE["assignee_id"]
        del ASSET_FIVE["assignee_type"]
        ASSET_FIVE["assetCategoryId"] = new_asset_category.id
        ASSET_FIVE["assigneeId"] = new_user.token_id
        ASSET_FIVE["assigneeType"] = "user"
        data = json.dumps(ASSET_FIVE)
        response = client.post(
            f'{API_BASE_URL_V1}/assets', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 409
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset with the tag Kinngg Macbook"\
            " already exists"

    def test_search_asset_endpoint(
            self,
            client,
            init_db,
            auth_header,  #pylint: disable=W0613
            new_asset_category,
            new_user):
        """
         Test that a list of asset is returned when a search query is provided
        """
        new_user.save()
        asset1 = Asset(
            tag='AND/345/EWH',
            assignee_id=new_user.token_id,
            assignee_type=AssigneeType.user.value,
            custom_attributes={'warranty': '2017-11-09'})
        asset2 = Asset(
            tag='AND/245/EkL',
            assignee_id=new_user.token_id,
            assignee_type=AssigneeType.user.value,
            custom_attributes={'warranty': '2018-11-09'})
        new_asset_category.assets.append(asset1)
        new_asset_category.assets.append(asset2)
        new_asset_category.save()
        asset1.save()
        asset2.save()

        response = client.get(
            f'''{API_BASE_URL_V1}/assets/search?start={(asset1.created_at).date()}&\
end={(asset2.created_at).date()}&warranty_start={asset1.custom_attributes['warranty']}&\
warranty_end={asset1.custom_attributes['warranty']}''',
            headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert len(response_json['data']) > 0  #pylint: disable=C1801
        assert type(response_json['data']) == list  #pylint: disable=C0123
