"""
    Module with tests for update schedule endpoint
"""
# Third party libraries
from flask import json

# Constant
from api.utilities.constants import CHARSET

# Messages
from api.utilities.messages.error_messages import (database_errors, jwt_errors,
                                                   serialization_errors)
from api.utilities.enums import ScheduleStatusEnum

# app config
from config import AppConfig

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestUpdateScheduleEndpoint:
    """ Update schedule endpoint """

    def test_update_schedule_with_valid_data_succeeds(
            self, client, auth_header, init_db, new_schedule, new_user):
        """ Should pass with valid update data
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        new_user.save()
        data = json.dumps({'assigneeId': new_user.token_id, 'status': 'done'})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data']['status'] == ScheduleStatusEnum.done.value
        assert response.json['data']['assignee'][
            'tokenId'] == new_user.token_id

    def test_update_schedule_with_valid_attachments_succeeds(
            self, client, auth_header, init_db, new_schedule, new_user):
        """ Should pass with valid update attachment data
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 
         """
        schedule_attachments = ["cloudinary image attachments"]
        new_schedule.save()
        new_user.save()
        data = json.dumps({
            'attachments': schedule_attachments,
            'status': 'done'
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data']['status'] == ScheduleStatusEnum.done.value
        assert response.json['data']['assignee'][
            'tokenId'] == new_user.token_id
        assert response.json['data']['attachments'] == schedule_attachments

    def test_update_schedule_with_invalid_attachments_fails(
            self, client, auth_header, init_db, new_schedule, new_user):
        """ Should fail with invalid update attachment data
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 
         """
        schedule_attachments = "cloudinary image attachments"
        new_schedule.save()
        new_user.save()
        data = json.dumps({
            'attachments': schedule_attachments,
            'status': 'done'
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['message'] == serialization_errors[
            'invalid_data_type']

    def test_assignee_changes_on_update_succeeds(self, client, auth_header,
                                                 init_db, new_schedule,
                                                 new_user, second_user):
        """ Should pass with valid update data
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        second_user.save()
        new_user.save()
        data = json.dumps({
            "assigneeId": second_user.token_id,
            "status": "done"
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data']['status'] == ScheduleStatusEnum.done.value
        assert response.json['data']['assignee'][
            'tokenId'] == second_user.token_id

    def test_update_schedule_with_invalid_assignee_id_fails(
            self, client, init_db, auth_header, new_schedule, new_user):
        """Should fail if no update data is sent in the request
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        new_user.save()
        data = json.dumps({"assigneeId": "invalid", "status": "done"})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors']['assigneeId'][
            0] == serialization_errors['assignee_not_found']

    def test_update_schedule_with_empty_status_fails(
            self, client, init_db, auth_header, new_schedule, new_user):
        """Should return 400 with empty update status
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        new_user.save()
        data = json.dumps({"assigneeId": new_user.token_id, "status": ""})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        enum_values = ', '.join(ScheduleStatusEnum.get_all())
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert response.json['errors']['status'][0] == serialization_errors[
            'invalid_enum_value'].format(values=enum_values)
        assert response.json['message'] == 'An error occurred'

    def test_update_schedule_with_no_token_fails(self, client, init_db,
                                                 new_schedule, new_user):
        """Should fail with no token
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        new_user.save()
        data = json.dumps({"assigneeId": new_user.token_id, "status": "done"})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}', data=data)
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['NO_TOKEN_MSG']

    def test_update_schedule_with_invalid_token_fails(self, client, init_db,
                                                      new_schedule, new_user):
        """Should fail with no token
        
        Args:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        new_user.save()
        data = json.dumps({"assigneeId": new_user.token_id, "status": "done"})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers={'Authorization': "Bearer invalid"})
        assert response.status_code == 401
        assert response.json['status'] == 'error'
        assert response.json['message'] == jwt_errors['INVALID_TOKEN_MSG']

    def test_update_non_existing_schedule_fails(self, client, auth_header,
                                                init_db, new_user):
        """Should fail if schedule id doesn't exist
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_user(object): Fixture for a new user 

        """
        new_user.save()
        data = json.dumps({"assigneeId": new_user.token_id, "status": "done"})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/-djhf24943982',
            data=data,
            headers=auth_header)
        assert response.status_code == 404
        assert response.json['status'] == 'error'
        assert response.json['message'] == database_errors[
            'non_existing'].format('Schedule')

    def test_update_schedule_with_invalid_status_string_fails(
            self, client, auth_header, init_db, new_schedule, new_user):
        """ Should fail with valid status data
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.save()
        new_user.save()
        data = json.dumps({
            "assigneeId": new_user.token_id,
            "status": "efigjrjhbg"
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        enum_values = ', '.join(ScheduleStatusEnum.get_all())
        assert response.status_code == 400
        assert response.json['errors']['status'][0] == serialization_errors[
            'invalid_enum_value'].format(values=enum_values)
        assert response.json['message'] == 'An error occurred'
        assert response.json['status'] == 'error'

    def test_update_done_schedule_to_pending_succeeds(
            self, client, auth_header, init_db, new_schedule, new_user):
        """ Should pass with done schedule updated to pending
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_schedule.status = ScheduleStatusEnum.done
        new_schedule.save()
        new_user.save()
        data = json.dumps({
            'assigneeId': new_user.token_id,
            'status': 'pending'
        })
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data'][
            'status'] == ScheduleStatusEnum.pending.value
        assert response.json['data']['assignee'][
            'tokenId'] == new_user.token_id

    def test_update_pending_schedule_to_done_succeeds(
            self, client, auth_header, init_db, new_test_schedule, new_user):
        """ Should pass with pending schedule updated to done
        
        Args:
            client(FlaskClient): fixture to get flask test client
            auth_header(dict): fixture to get token
            init_db(SQLAlchemy): fixture to initialize the test database
            new_test_schedule (object): Fixture for a new schedule 
            new_user(object): Fixture for a new user 

        """
        new_test_schedule.save()
        new_user.save()
        data = json.dumps({'assigneeId': new_user.token_id, 'status': 'done'})
        response = client.patch(
            f'{API_V1_BASE_URL}/schedules/{new_test_schedule.id}',
            data=data,
            headers=auth_header)
        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['data']['status'] == ScheduleStatusEnum.done.value
        assert response.json['data']['assignee'][
            'tokenId'] == new_user.token_id
