import json
from api.utilities.messages.error_messages import query_errors, jwt_errors
from api.utilities.constants import CHARSET

# app config
from config import AppConfig

BASE_URL = AppConfig.API_BASE_URL_V1


class TestExportUsersAsCsv:
    """
    Tests for exporting users as csv
    """

    def assert_csv_success(self, response, expected_csv):
        """
        Helper function to assert whether a csv file has been
        successfully generated
        """
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert expected_csv in response.data.decode('utf-8')

    def test_export_users_as_csv_with_no_query_should_succeed(
            self, init_db, client, auth_header_two, new_user):
        """
        Should return csv data file with user information.

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header_two(dict): fixture to get token
            new_user(User): fixture to create user
        """

        # Test endpoint returns csv data when users are saved in the db
        new_user.save()

        response = client.get(f'{BASE_URL}/people/export', headers=auth_header_two)

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/csv'
        assert b'center,email,image url,name,role,status' in response.data
        assert new_user.name in response.data.decode()
        assert new_user.email in response.data.decode()
        assert new_user.center.name in response.data.decode()
        assert new_user.role.title in response.data.decode()

    def test_export_filtered_users_as_csv_with_valid_queries_succeeds(
            self, client, init_db, auth_header, new_user):
        """
        Test that users are filtered and a csv file is generated when valid
        queries are passed. The valid queries are name, email, centerId,
        roleId, status and imageUrl.
        """

        url = f'{BASE_URL}/people/export'
        new_user.save()
        expected_csv = 'center,email,image url,name,role,status\r\n' \
                       f'{new_user.center.name},{new_user.email},' \
                       f'{new_user.image_url},{new_user.name},' \
                       f'{new_user.role.title},{new_user.status.name}\r\n'

        response = client.get(
            f'{url}?name={new_user.name}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)
        response = client.get(
            f'{url}?email={new_user.email}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)
        response = client.get(
            f'{url}?status={new_user.status.name}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)
        response = client.get(
            f'{url}?centerId={new_user.center_id}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)
        response = client.get(
            f'{url}?roleId={new_user.role_id}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)
        response = client.get(
            f'{url}?imageUrl={new_user.image_url}', headers=auth_header)
        self.assert_csv_success(response, expected_csv)
        response = client.get(
            f'{url}?centerId={new_user.center_id}&name={new_user.name}'
            f'&email={new_user.email}&roleId={new_user.role_id}'
            f'&status={new_user.status.name}&imageUrl={new_user.image_url}',
            headers=auth_header)
        self.assert_csv_success(response, expected_csv)

    def test_export_filtered_users_as_csv_does_not_return_deleted_users(
            self, client, init_db, new_user_two, auth_header_two):
        """
        Make sure that deleted users are not returned in the filtered
        results
        """

        new_user_two.deleted = True
        new_user_two.save()
        response = client.get(
            f'{BASE_URL}/people/export?name={new_user_two.name}',
            headers=auth_header_two)
        assert response.headers['Content-Type'] == 'text/csv'
        assert response.data.decode(CHARSET) == ''

    def test_export_filtered_users_as_csv_with_invalid_query_fails(
            self, client, new_user, auth_header):
        """
        Test that an error is returned when an invalid query is provided
        """

        response = client.get(
            f'{BASE_URL}/people/export?nam={new_user.name}',
            headers=auth_header)
        assert response.status_code == 400
        actual_message = json.loads(response.data)['message']
        expected_message = query_errors['invalid_query_non_existent_column']\
            .format('nam', 'User')
        assert actual_message == expected_message
        response = client.get(
            f'{BASE_URL}/people/export?status=invalid', headers=auth_header)
        assert response.status_code == 400
        err_message = json.loads(response.data)['message']
        assert err_message == query_errors['invalid_query_wrong_value']\
            .format('status', 'invalid')

    def test_export_user_as_csv_with_no_token_should_fail(
            self, client, init_db):
        """
        Should return a 401 status code and an error message if authorization
        token is not provided in the request header

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
        """

        response = client.get(f'{BASE_URL}/people/export')
        response_json = json.loads(response.data.decode(CHARSET))

        assert response.status_code == 401
        assert response_json['status'] == 'error'
        assert response_json['message'] == jwt_errors['NO_TOKEN_MSG']
