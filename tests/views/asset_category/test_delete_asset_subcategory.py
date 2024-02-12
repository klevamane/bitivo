"Module for asset category endpoint test" 
from flask import json  #pylint: disable=E0401

# models
from api.models import AssetCategory, Asset

# constants
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

api_v1_base_url = AppConfig.API_BASE_URL_V1  #pylint: disable=C0103


class TestAssetSubCategoriesEndpoint:  #pylint: disable=R0904
    """"
    Asset subcategory endpoints test
    """
    def test_delete_single_asset_subcategory_succeeds(
            self, client, init_db, new_user, auth_header, new_space):  #pylint: disable=R0201,W0613,C0103
        """
            Tests that a single asset subcategory can be deleted
        """
        asset_category = AssetCategory(name="TestLaptop4")
        asset_category.save()
        new_user.save()
        new_space.save()
        sub_category = AssetCategory(
            name="TestLaptop1", description="mac",
            parent_id=asset_category.id,
            image={"public_id": "hauvx56khbsyajkziw1c"})
        sub_category.save()
        asset = Asset(
            tag='abd',
            asset_category_id=sub_category.id,
            assignee_id=new_space.id,
            assignee_type='space')

        asset = asset.save() 
        response = client.delete(
            f'{api_v1_base_url}/subcategories/{sub_category.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert asset.deleted is True
        assert response.status_code == 200
        assert response_json["status"] == "success"
        assert response_json["message"] == "Subcategory successfully deleted"


    def test_delete_single_asset_category(self, client, init_db, new_user, auth_header):  #pylint: disable=R0201,W0613,C0103
        """
            Tests that 403 error is returned on delete of asset category
        """
        asset_category = AssetCategory(name="TestLaptop4")
        asset_category.save()
        new_user.save()
        response = client.delete(
            f'{api_v1_base_url}/subcategories/{asset_category.id}',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 403
        assert response_json["status"] == "error"
        assert response_json["message"] == "You are not authorised to delete this category please"

    def test_delete_single_asset_subcategory_invalid_id(  #pylint: disable=R0201,C0103
            self,
            client,
            new_user, auth_header):  #pylint: disable=W0613
        """
        Tests that 400 is returned when id is invalid
        """
        asset_category = AssetCategory(name="TestLaptop5")
        asset_category.save()

        new_user.save()

        response = client.delete(
            f'{api_v1_base_url}/subcategories/LX@', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == "Invalid id in parameter"

    def test_delete_single_asset_subcategory_not_found(  #pylint: disable=R0201,C0103
            self,
            client,
            new_user, auth_header):   #pylint: disable=W0613
        """
        Tests that 404 is returned when subcategory is not found
        """
        asset_category = AssetCategory(name="TestLaptop5")
        asset_category.save()
        new_user.save()

        response = client.delete(
            f'{api_v1_base_url}/subcategories/-LjLapZEi255LwOkSkT-', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json["message"] == "Asset category not found"
