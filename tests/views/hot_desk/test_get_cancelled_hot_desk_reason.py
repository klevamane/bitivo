from datetime import datetime
import json

  # Local Module
from api.utilities.constants import CHARSET
from api.utilities.messages.error_messages import serialization_errors
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
from api.utilities.constants import HOT_DESK_CANCELLATION_VALUE

  # app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestGetCancelledHotDeskForParticularReason:
  """Test get cancelled hot desk request by user"""

  def test_get_cancelled_hot_desk_for_particular_reason_succeeds(
    self, client, auth_header, new_hot_desk_request_with_complaint, new_user):
      """Tests that cancelled hot desk requests for a particular reason is successfully fetched
      client (func): Flask test client
      auth_header (func): Authentication token
      new_hot_desk_request_with_complaint (Fixture): a fixture to create a new hot desk request
      new_user (Fixture): Fixture to create a new user
      Returns:
          None
      """

      new_user.save()
      new_hot_desk_request_with_complaint.created_at = datetime.utcnow()
      new_hot_desk_request_with_complaint.save()
      response = client.get(
                  BASE_URL + '/hot-desks/cancelled/?reason={}'.format('others'), headers=auth_header)
                  
      response_json = json.loads(response.data.decode(CHARSET))

      assert isinstance(response_json, dict)
      assert isinstance(response_json['meta'], dict)
      assert isinstance(response_json['data'], dict)
      assert isinstance(response_json['data']['others'], list)
      assert response.status_code == 200
      assert response_json['status'] == 'success'
      assert response_json['message'] == SUCCESS_MESSAGES['cancelled_hot_desk_reason'].format(
          'others')
      assert response_json['data']['others'][0]['requester']['tokenId'] == new_hot_desk_request_with_complaint.requester_id
      assert response_json['data']['others'][0]['approver']['tokenId'] == new_hot_desk_request_with_complaint.assignee_id
      assert f'{BASE_URL}/hot-desks/cancelled/?reason=others&page=1&limit=10' in response_json['meta']['firstPage']
      assert f'{BASE_URL}/hot-desks/cancelled/?reason=others' in response_json['meta']['currentPage']
      assert response_json['meta']['pagesCount'] == 1

  def test_get_cancelled_hot_desk_for_particular_reason_with_params_succeeds(
    self, client, auth_header, new_hot_desk_cancelled, new_user):
      """Tests that cancelled hot desk requests for a particular reason with params is successfully fetched
      client (func): Flask test client
      auth_header (func): Authentication token
      new_hot_desk_cancelled (Fixture): a fixture to create a new hot desk request
      new_user (Fixture): Fixture to create a new user
      Returns:
          None
      """

      new_user.save()
      new_hot_desk_cancelled.created_at = datetime.utcnow()
      new_hot_desk_cancelled.save()
      response = client.get(
                  BASE_URL + '/hot-desks/cancelled/?startDate={}&pagination=False&reason={}'.format(
                      '2019-4-1', 'changedmymind'), headers=auth_header)
      response_json = json.loads(response.data.decode(CHARSET))

      assert isinstance(response_json, dict)
      assert isinstance(response_json['data'], dict)
      assert isinstance(response_json['data']['changedmymind'], list)
      assert response.status_code == 200
      assert response_json['status'] == 'success'
      assert response_json['message'] == SUCCESS_MESSAGES['cancelled_hot_desk_reason'].format(
          'changedmymind')
      assert response_json['data']['changedmymind'][0]['requester']['tokenId'] == new_hot_desk_cancelled.requester_id
      assert response_json['data']['changedmymind'][0]['approver']['tokenId'] == new_hot_desk_cancelled.assignee_id
      assert response_json['meta'] is None

  def test_get_cancelled_hot_desk_for_particular_reason_with_invalid_reason_fails(
    self, client, auth_header, new_user):
      """Tests that cancelled hot desk requests with invalid reason fails
      client (func): Flask test client
      auth_header (func): Authentication token
      new_user (Fixture): Fixture to create a new user
      Returns:
          None
      """

      new_user.save()
      response = client.get(
                  BASE_URL + '/hot-desks/cancelled/?reason={}'.format('invalid'), headers=auth_header)
      response_json = json.loads(response.data.decode(CHARSET))

      assert response.status_code == 400
      assert response_json['status'] == 'error'
      assert response_json['message'] == serialization_errors['invalid_request_param'].format( \
              'cancellation reason param value', ', '.join(HOT_DESK_CANCELLATION_VALUE))

  def test_get_cancelled_hot_desk_for_particular_reason_with_no_reason_fails(
    self, client, auth_header, new_user):
      """Tests that cancelled hot desk requests with no reason fails
      client (func): Flask test client
      auth_header (func): Authentication token
      new_user (Fixture): Fixture to create a new user
      Returns:
          None
      """

      new_user.save()
      response = client.get(
                  BASE_URL + '/hot-desks/cancelled/?reason={}'.format(''), headers=auth_header)
      response_json = json.loads(response.data.decode(CHARSET))

      assert response.status_code == 400
      assert response_json['status'] == 'error'
      assert response_json['message'] == serialization_errors['required_param_key'].format( \
              'cancellation reason', ', '.join(HOT_DESK_CANCELLATION_VALUE))
