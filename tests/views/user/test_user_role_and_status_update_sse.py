import json
from unittest.mock import Mock

from config import AppConfig
from api.utilities.server_events import sse

API_V1_BASE_URL = AppConfig.API_BASE_URL_V1


class TestSseUserRoleStatusUpdate:
    def test_sse_on_user_status_update_succeeds(
            self, client, init_db, auth_header, new_user, user_with_role):
        """

        Should return a 200 status code when status valid field is
        supplied for update

        Parameters:
            client(FlaskClient): fixture to get flask test client
            init_db(SQLAlchemy): fixture to initialize the test database
            auth_header(dict): fixture to get token
            new_user(BaseModel): fixture for creating a user

        """
        new_user.save()
        new_user_with_role, _ = user_with_role
        new_user = new_user_with_role.save()
        """
        Update only status
        """
        user_update = {
            'status': 'disabled',
        }

        sse.publish = Mock()
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps(user_update))

        assert response.status_code == 200
        assert sse.publish.call_args[0][0].get("tokenId")
        assert sse.publish.call_args[0][0].get("status")

    def test_sse_on_user_role_update_succeeds(self, client, init_db,
                                              auth_header, new_user,
                                              user_with_role, new_role):
        """

            Should return a 200 status code when role valid field is
            supplied for update

            Parameters:
                client(FlaskClient): fixture to get flask test client
                init_db(SQLAlchemy): fixture to initialize the test database
                auth_header(dict): fixture to get token
                new_user(BaseModel): fixture for creating a user
                new_role(BaseModel): fixture for for creating a role
            """
        new_user.save()
        new_user_with_role, _ = user_with_role
        new_user = new_user_with_role.save()
        new_role = new_role.save()
        role_id = new_role.id
        """
            Update only role
            """
        user_update = {'roleId': role_id}
        sse.publish = Mock()
        response = client.patch(
            f'{API_V1_BASE_URL}/people/{new_user.token_id}',
            headers=auth_header,
            data=json.dumps(user_update))
        assert response.status_code == 200
        assert sse.publish.call_args[0][0].get("tokenId")
        assert sse.publish.call_args[0][0].get("roleId")
