import pytest
from api.models import Role, ResourceAccessLevel
from api.middlewares.base_validator import ValidationError


class TestRoleModel:
    """
    Test
    """

    def test_new_role(self, init_db, new_role):
        role = new_role
        assert role == new_role.save()

    def test_count(self):
        assert Role.count() == 1

    def test_query(self):
        role_query = Role.query_()
        assert role_query.count() == 1
        assert isinstance(role_query.all(), list)

    def test_update(self, new_custom_role, request_ctx,
                    mock_request_two_obj_decoded_token, new_user):
        new_user.save()
        new_custom_role.update_(title='Talent Development Manager')
        assert new_custom_role.title == 'Talent Development Manager'

    def test_repr_method(self, new_role):
        assert repr(new_role) == f'<Role: {new_role.title}>'

    def test_adding_resource_access_levels_to_role_succeeds(
            self, init_db, new_permission, new_resource, new_role):
        """
        Should add resource access levels to a role successfully

        Parameters:
            new_permission (object): Fixture to create a new permission
            new_resource (object): Fixture to create a new resource
            new_role (object): Fixture to create a new role
        """
        permission = new_permission.save()
        resource = new_resource.save()
        access_level = ResourceAccessLevel(
            resource=resource, permissions=[permission])
        new_role.resource_access_levels.append(access_level)
        new_role.save()
        assert new_role.resource_access_levels.all() == [access_level]

    def test_delete(self, new_custom_role, request_ctx,
                    mock_request_two_obj_decoded_token):
        new_custom_role.save()
        new_custom_role.delete()
        assert Role.get(new_custom_role.id) is None
