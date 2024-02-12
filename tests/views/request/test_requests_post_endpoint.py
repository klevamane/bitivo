"""
Module of tests for request post endpoint
"""
# Flask
from flask import json

# Utilities
from api.utilities.constants import CHARSET
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.messages.error_messages import (serialization_errors)

# Mock
from tests.mocks.requests import (
    VALID_REQUEST_DATA, INCOMPLETE_REQUEST_DATA, INVALID_REQUEST_DATA,
    INVALID_REQUEST_ATTACHMENT_DATA, EMPTY_REQUEST_SUBJECT_DATA,
    EMPTY_REQUEST_DESCRIPTION_DATA, VALID_REQUEST_DATA_WITH_ASSIGNEE_ID,
    INVALID_REQUEST_DATA_LONG_DESCRIPTION)

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestRequestPostEndpoints:
    """
    TestRequest resource POST endpoint
    """

    def test_create_request_with_valid_data_succeeds(self, client, init_db,
                                                     auth_header, new_user,
                                                     new_request_type_two):
        """Should return a 201 status code and new request
        data when data provided in request is valid.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type_two (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type_two.save()
        VALID_REQUEST_DATA['centerId'] = new_user.center_id
        VALID_REQUEST_DATA['requesterId'] = new_user.token_id
        VALID_REQUEST_DATA['requestTypeId'] = new_request_type_two.id
        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == \
               SUCCESS_MESSAGES['created'].format('Request')
        assert response_json['data']['subject'] == VALID_REQUEST_DATA[
            'subject']
        assert response_json['data']['requestType'][
                   'id'] == new_request_type_two.id
        assert response_json['data']['centerId'] == new_user.center_id
        assert response_json['data']['description'] == VALID_REQUEST_DATA[
            'description']
        assert response_json['data']['requester'][
                   'tokenId'] == new_user.token_id

    def test_create_request_with_assignee_valid_data_succeeds(self,
                                                              init_db, client,
                                                              auth_header,
                                                              new_user,
                                                              new_request_type_two):
        """Should return a 201 status code and new request data when
        data provided in request is valid
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type_two (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type_two.save()
        VALID_REQUEST_DATA_WITH_ASSIGNEE_ID['centerId'] = new_user.center_id
        VALID_REQUEST_DATA_WITH_ASSIGNEE_ID['requesterId'] = new_user.token_id
        VALID_REQUEST_DATA_WITH_ASSIGNEE_ID['assigneeId'] = new_user.token_id
        VALID_REQUEST_DATA_WITH_ASSIGNEE_ID[
            'requestTypeId'] = new_request_type_two.id
        data = json.dumps(VALID_REQUEST_DATA_WITH_ASSIGNEE_ID)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 201
        assert response_json["status"] == "success"
        assert response_json["message"] == \
               SUCCESS_MESSAGES['created'].format('Request')
        assert response_json['data']['subject'] == VALID_REQUEST_DATA[
            'subject']
        assert response_json['data']['requestType'][
                   'id'] == new_request_type_two.id
        assert response_json['data']['centerId'] == new_user.center_id
        assert response_json['data']['description'] == VALID_REQUEST_DATA[
            'description']
        assert response_json['data']['requester'][
                   'tokenId'] == new_user.token_id
        assert response_json['data']['assignee'][
                   'imageUrl'] == new_user.image_url

    def test_create_request_with_invalid_data_fails(self, client, init_db,
                                                    auth_header, new_user,
                                                    new_request_type_two):
        """Should return a 201 status code and new request
        data when data provided in request is valid.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type_two (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type_two.save()
        INVALID_REQUEST_ATTACHMENT_DATA['centerId'] = new_user.center_id
        INVALID_REQUEST_ATTACHMENT_DATA['requesterId'] = new_user.token_id
        INVALID_REQUEST_ATTACHMENT_DATA[
            'requestTypeId'] = new_request_type_two.id
        data = json.dumps(INVALID_REQUEST_ATTACHMENT_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == serialization_errors[
            'invalid_data_type']

    def test_create_request_with_missing_required_field_fails(self, client,
                                                              init_db, auth_header,
                                                              new_user,
                                                              new_request_type):
        """Should return a 400 status code and new request data has
        some missing fields.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        VALID_REQUEST_DATA['requesterId'] = new_user.token_id
        VALID_REQUEST_DATA['requestTypeId'] = new_request_type.id
        data = json.dumps(INCOMPLETE_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['centerId'][0] == serialization_errors[
            'field_required']

    def test_create_request_with_invalid_request_type_id_fails(self,
                                                               client, init_db,
                                                               auth_header,
                                                               new_user,
                                                               new_request_type):
        """Should return a 400 status code and new request data has
        invalid request type id.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        data = json.dumps(INCOMPLETE_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['requestTypeId'][
                   0] == serialization_errors['not_found'].format('Request type')

    def test_create_request_with_invalid_id_string_fails(self, client, init_db,
                                                         auth_header,
                                                         new_user,
                                                         new_request_type):
        """Should return a 400 status code and new request data has
        invalid id strings.
        
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        VALID_REQUEST_DATA['requestTypeId'] = INVALID_REQUEST_DATA[
            'requestTypeId']
        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['requestTypeId'][
                   0] == serialization_errors['invalid_id_field']

    def test_create_request_with_invalid_center_id_fails(self, client, init_db,
                                                         auth_header, new_user,
                                                         new_request_type):
        """Should return a 400 status code and new request data has
        invalid center id.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        VALID_REQUEST_DATA['centerId'] = "-LSkH67q4Jx6BfIWeTYTjkjkj"
        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['centerId'][0] == serialization_errors[
            'not_found'].format('Center')

    def test_create_request_with_invalid_requester_id_fails(self, client,
                                                            init_db, auth_header,
                                                            new_user,
                                                            new_request_type):
        """Should return a 400 status code and new request
        data has invalid requester id.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        VALID_REQUEST_DATA['centerId'] = new_user.center_id
        VALID_REQUEST_DATA['requestTypeId'] = new_request_type.id
        VALID_REQUEST_DATA['requesterId'] = "-LSkH67q4Jx6BfIWeTYTjvjkll"
        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['requesterId'][
                   0] == serialization_errors['requester_not_found']

    def test_create_request_with_requester_id_not_in_a_center_fails(self, client,
                                                                    init_db,
                                                                    auth_header,
                                                                    new_user,
                                                                    test_center_with_users,
                                                                    new_request_type):
        """Should return a 400 status code when new request data has requester
        id that is not in requester center.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
            test_center_with_users(dict): fixture to create a new center with users
        """
        new_user.save()
        test_center_with_users.save()
        new_request_type.save()
        VALID_REQUEST_DATA['centerId'] = test_center_with_users.id
        VALID_REQUEST_DATA['requesterId'] = new_user.token_id
        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['requesterId'][
                   0] == serialization_errors['requester_not_found_in_center']

    def test_create_request_with_request_type_id_not_in_user_center_fails(self, client, init_db,
                                                                          auth_header, new_user,
                                                                          new_request_type,
                                                                          new_request_type_three):
        """Should return a 400 status code when new request data has request
        type id that is not in the requester center.
            
            Args:
                client(FlaskClient): fixture to get flask test client
                init_db(SQLAlchemy): fixture to initialize the test database
                auth_header(dict): fixture to get token
                new_user (dict): fixture to create a new user
                new_request_type (dict): fixture to create a new request type
            """
        new_user.save()
        new_request_type.save()
        new_request_type_three.save()
        VALID_REQUEST_DATA['centerId'] = new_user.center_id
        VALID_REQUEST_DATA['requesterId'] = new_user.token_id
        VALID_REQUEST_DATA['requestTypeId'] = new_request_type_three.id

        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['requestType'][
                   0] == serialization_errors['request_type_not_found_in_center']

    def test_create_request_with_requester_id_same_as_responder_id_fails(self, client,
                                                                         init_db, auth_header,
                                                                         new_user,
                                                                         new_request_type_two,
                                                                         new_request_type):
        """Should return a 400 status code when new request data has requester
         id same as responder id.
            
            Args:
                client(FlaskClient): fixture to get flask test client
                init_db(SQLAlchemy): fixture to initialize the test database
                auth_header(dict): fixture to get token
                new_user (dict): fixture to create a new user
                new_request_type (dict): fixture to create a new request type
            """
        new_user.save()
        new_request_type.save()
        new_request_type_two.save()
        VALID_REQUEST_DATA['centerId'] = new_user.center_id
        VALID_REQUEST_DATA['requesterId'] = new_request_type_two.assignee_id
        VALID_REQUEST_DATA['requestTypeId'] = new_request_type_two.id
        data = json.dumps(VALID_REQUEST_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response_json['errors']['requesterId'][
                   0] == serialization_errors['requester_cannot_be_responder']

    def test_create_request_with_empty_subject_fails(self, client, init_db,
                                                     auth_header, new_user,
                                                     new_request_type):
        """Should return a 400 status code and new request data
        has empty subject.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        data = json.dumps(EMPTY_REQUEST_SUBJECT_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response.json['errors']['subject'][0] == serialization_errors[
            'not_empty']

    def test_create_request_with_empty_description_fails(self, client, init_db,
                                                         auth_header, new_user,
                                                         new_request_type):
        """Should return a 400 status code and new request
        data has empty description.
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type.save()
        data = json.dumps(EMPTY_REQUEST_DESCRIPTION_DATA)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == 'An error occurred'
        assert response.json['errors']['description'][
                   0] == serialization_errors['not_empty']

    def test_create_request_with_invalid_data_description_fails(self, client, init_db,
                                                                auth_header, new_user,
                                                                new_request_type_two):
        """Should return a 400 status code and the an error message stating
           Field must be 1000 characters or less.

        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user (dict): fixture to create a new user
            new_request_type_two (dict): fixture to create a new request type
        """
        new_user.save()
        new_request_type_two.save()
        INVALID_REQUEST_DATA_LONG_DESCRIPTION['centerId'] = new_user.center_id
        INVALID_REQUEST_DATA_LONG_DESCRIPTION['requesterId'] = new_user.token_id
        INVALID_REQUEST_DATA_LONG_DESCRIPTION['requestTypeId'] = new_request_type_two.id
        data = json.dumps(INVALID_REQUEST_DATA_LONG_DESCRIPTION)
        response = client.post(
            f'{BASE_URL}/requests', headers=auth_header, data=data)
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 400
        assert response_json["status"] == "error"
        assert response_json["message"] == 'An error occurred'
        assert response_json['errors']['description'][0] == serialization_errors['string_length'].format(1000)
