"""Module for testing asset supporting document resources"""
import os
from flask import json

from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import serialization_errors, jwt_errors
from api.utilities.enums import AssetSupportingDocumentTypeEnum, get_enum_fields

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1


class TestAssetSupportingDocument:
    """Class for testing asset supporting document
    resources
    """

    def test_get_asset_supporting_documents_succeeds(
        self,
        client,
        init_db,
        auth_header,
        new_asset_supporting_document
    ):
        """
        Test getting supporting document for specific asset succeeds
        """

        new_asset_supporting_document.save()
        response = client.get(
            f'{API_BASE_URL_V1}/assets/{new_asset_supporting_document.asset_id}/documents',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert isinstance(response_json, dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES[
            'fetched'].format('Asset supporting documents')
        assert response_json["data"][
            "documents"][0]["documentName"] == \
            new_asset_supporting_document.document_name

    def test_get_supporting_documents_with_invalid_asset_id_fails(
            self,
            client,
            init_db,
            auth_header):
        """
        Test getting supporting documents for specific asset with invalid asset
        id fails
        """
        response = client.get(
            f'{API_BASE_URL_V1}/assets/-LjXY8QptIssfEtZl3Ty/documents',
            headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json["status"] == "error"
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset')

    def test_create_supporting_document_succeeds(self, client, init_db, request_ctx, mock_request_obj_decoded_token, auth_header_form_data, new_asset_supporting_document):

        file = "mock-image.png"
        document = os.path.join(
            os.path.dirname(__file__), f"../../tasks/cloudinary/{file}")

        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_asset_supporting_document.asset_id}/documents',
            headers=(auth_header_form_data),
            data={
                "documentName": "HP Printer",
                "documentType": "purchase receipts",
                "document": (document, file)
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 201
        assert isinstance(response_json, dict)
        assert isinstance(response_json["data"]["creator"], dict)
        assert response_json["status"] == "success"
        assert response_json["message"] == SUCCESS_MESSAGES["created"].format(
            "Asset Supporting Document")

    def test_create_supporting_document_for_nonexisting_asset_fails(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token, auth_header_form_data, new_asset_supporting_document):

        file = "mock-image.png"
        document = os.path.join(
            os.path.dirname(__file__), f"../../tasks/cloudinary/{file}")

        response = client.post(
            f'{API_BASE_URL_V1}/assets/-LjubRhqDc_h3qaMyh1s/documents',
            headers=(auth_header_form_data),
            data={
                "documentName": "HP Printer",
                "documentType": "purchase receipts",
                "document": (document, file)
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == "An error occurred"
        assert response_json["errors"]["assetId"][0] == serialization_errors[
            'asset_not_found']

    def test_create_supporting_document_fails_with_json_content_type(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token, auth_header, new_asset_supporting_document):

        file = "mock-image.png"
        document = os.path.join(
            os.path.dirname(__file__), f"../../tasks/cloudinary/{file}")

        response = client.post(
            f'{API_BASE_URL_V1}/assets/{new_asset_supporting_document.asset_id}/documents',
            headers=(auth_header),
            data={
                "documentName": "HP Printer",
                "documentType": "purchase receipts",
                "document": (document, file)
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response_json["status"] == "error"
        assert response_json["message"] == "Content-Type should be multipart/form-data"

    def test_soft_delete_asset_supporting_document_success(
            self, client, new_asset_supporting_document, auth_header):
        """
            Tests for soft deleting a supporting document
        """
        new_asset_supporting_document.save()

        response = client.delete(f'{API_BASE_URL_V1}/documents/{new_asset_supporting_document.id}',
                                 headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == SUCCESS_MESSAGES[
            'deleted'].format('Asset supporting document')

    def test_delete_asset_supporting_document_found(self, client, auth_header):
        """
            Tests that 404 is returned for an attempt to delete a
            non-existent supporting document
        """

        response = client.delete(
            f'{API_BASE_URL_V1}/documents/-L6YY54rfd98GTY', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 404
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors[
            'not_found'].format('Asset supporting document')

    def test_delete_asset_supporting_document_invalid_id(self, client, auth_header):
        """
        Tests that 400 is returned when id is invalid
        """
        response = client.delete(
            f'{API_BASE_URL_V1}/documents/-LX%%%tghrfe5', headers=auth_header)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == serialization_errors['invalid_id']

    def test_delete_asset_supporting_document_without_token(self, client, new_asset_supporting_document):
        """
        Tests that 401 is returned when token is not provided
        """
        new_asset_supporting_document.save()

        response = client.delete(
            f'{API_BASE_URL_V1}/documents/{new_asset_supporting_document.id}')
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_create_supporting_document_with_invalid_document_type_fails(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token, auth_header_form_data, new_asset_supporting_document):
        """
        Tests that a 400 response is returned when an invalid file type is sent to the API
        """

        file = "test_cloudinary_file_handler.py"
        document = os.path.join(
            os.path.dirname(__file__), f"../../tasks/cloudinary/{file}")

        response = client.post(
            f'{API_BASE_URL_V1}/assets/-LjubRhqDc_h3qaMyh1s/documents',
            headers=(auth_header_form_data),
            data={
                "documentName": "HP Printer",
                "documentType": "purchase receipts",
                "document": (document, file)
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_file_type'].format('document')

    def test_create_supporting_document_without_document_fails(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token, auth_header_form_data, new_asset_supporting_document):
        """
        Tests that a 400 response is returned when no file is sent to the API
        """

        response = client.post(
            f'{API_BASE_URL_V1}/assets/-LjubRhqDc_h3qaMyh1s/documents',
            headers=(auth_header_form_data),
            data={
                "documentName": "HP Printer",
                "documentType": "purchase receipts",
                "document": ""
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'required_field'].format('document')

    def test_create_supporting_document_with_document_type_not_provided_fails(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token,
            auth_header_form_data, new_asset_supporting_document):
        """
        Tests that a 400 response is returned when request with document type
        not provided is sent to the API
        """

        file = "test_cloudinary_file_handler.py"
        document = os.path.join(
            os.path.dirname(__file__), f"../../tasks/cloudinary/{file}")

        response = client.post(
            f'{API_BASE_URL_V1}/assets/-LjubRhqDc_h3qaMyh1s/documents',
            headers=(auth_header_form_data),
            data={
                "documentName": "HP Printer",
                "documentType": "",
                "document": (document, file)
            })
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["errors"] == {'documentType': [
            serialization_errors['not_empty']
        ]}

    def test_create_supporting_document_with_document_type_not_in_enum_fails(
            self, client, init_db, request_ctx, mock_request_obj_decoded_token,
            auth_header_form_data, new_asset_supporting_document):
        """
        Tests that a 400 response is returned when a file type not in enum is
        sent to the API
        """

        file = "test_cloudinary_file_handler.py"
        document = os.path.join(
            os.path.dirname(__file__), f"../../tasks/cloudinary/{file}")

        response = client.post(
            f'{API_BASE_URL_V1}/assets/-LjubRhqDc_h3qaMyh1s/documents',
            headers=(auth_header_form_data),
            data={
                "documentName": "HP Printer",
                "documentType": "not in enum",
                "document": (document, file)
            })
        response_json = json.loads(response.data.decode(CHARSET))
        document_types = get_enum_fields(AssetSupportingDocumentTypeEnum)
        choices = str(document_types).strip('[]')
        assert response.status_code == 400
        assert isinstance(response_json, dict)
        assert response_json["status"] == "error"
        assert response_json["errors"] == {
            'documentType': [
                serialization_errors[
                    'invalid_document_type'].format(
                    choices=choices)
            ]
        }
