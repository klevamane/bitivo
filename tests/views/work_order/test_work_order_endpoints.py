"Module for request endpoints test"

from flask import json  #pylint: disable=E0401

# models
from api.models import Request

# constants
from api.utilities.constants import CHARSET, MIMETYPE

# messages
from api.utilities.messages.error_messages import (
    serialization_errors, jwt_errors, query_errors, filter_errors)
from api.utilities.messages.success_messages import SUCCESS_MESSAGES

# app config
from config import AppConfig

API_BASE_URL_V1 = AppConfig.API_BASE_URL_V1  #pylint: disable=C0103


class TestWorkOrderEndpoints:  #pylint: disable=R0904
    """"Work Order endpoints test"""

    def test_get_work_order_endpoint_succeeds(  #pylint: disable=R0201,C0103
            self,
            client,
            init_db,  #pylint: disable=W0613
            auth_header,
            new_work_order):
        """Test work order list endpoint
        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            auth_header (dict): fixture to get token
            new_work_order: fixture that contains the work order
        """
        work_order = new_work_order.save()
        response = client.get(
            f'{API_BASE_URL_V1}/work-orders', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))
        response_data = response_json['data'][0]

        assert response.status_code == 200
        assert len(response_json["data"][0]) <= 12
        assert response_data['id'] == work_order.id
        assert response_data['description'] == work_order.description
        assert response_data['title'] == work_order.title
        assert isinstance(response_data["assignee"], dict)
        assert isinstance(response_data["assignee"]['role'], dict)
        assert "startDate" in response_data
        assert "endDate" in response_data
        assert "name" in response_data["assignee"]
        assert "imageUrl" in response_data["assignee"]
        assert "email" in response_data["assignee"]
        assert "id" in response_data["assignee"]["role"]
        assert "title" in response_data["assignee"]["role"]
        assert "description" in response_data["assignee"]["role"]
        assert response_json['status'] == 'success'
        assert response_json['message'] == \
            SUCCESS_MESSAGES['fetched'].format('Work Orders')

    def test_work_order_endpoint_pagination_succeeds(self, client, init_db,
                                                     auth_header):
        """Test get work order list endpoint pagination
            Should return paginated list of work orders
            Args:
                client (FlaskClient): fixture to get flask test client
                init_db (SQLAlchemy): fixture to initialize the test database
                auth_header (dict): fixture to get token
        """
        response = client.get(
            f'{API_BASE_URL_V1}/work-orders', headers=auth_header)

        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 200
        assert 'meta' in response_json
        assert response_json['meta']['page'] == 1
        assert 'pagesCount' in response_json['meta']
        assert 'totalCount' in response_json['meta']
        assert response_json['status'] == 'success'
        assert isinstance(response_json['data'], list)
        assert len(response_json['data']) == 1

    def test_get_work_orders_endpoint_with_no_token_fails(
            self, client, init_db, new_work_order):
        """This test checks for getting work orders with no token fails

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_work_order(obj): fixture that contains the work order

        """
        work_order = new_work_order.save()
        response = client.get(f'{API_BASE_URL_V1}/work-orders')
        response_data = json.loads(response.data.decode(CHARSET))
        assert response_data['status'] == 'error'
        assert response_data['message'] == jwt_errors['NO_TOKEN_MSG']
        assert response.status_code == 401

    def test_get_work_orders_with_invalid_token_fail(self, client, init_db,
                                                     new_work_order):
        """This test checks for getting work orders with invalid token

        Args:
            client (FlaskClient): fixture to get flask test client
            init_db (SQLAlchemy): fixture to initialize the test database
            new_work_order(obj): fixture that contains the work order

        """
        new_work_order.save()
        response = client.post(
            f'{API_BASE_URL_V1}/work-orders',
            headers={
                'Authorization': "Bearer XXXX",
                'Content-Type': MIMETYPE,
                'Accept': MIMETYPE
            })
        response_json = json.loads(response.data.decode(CHARSET))
        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['INVALID_TOKEN_MSG']
