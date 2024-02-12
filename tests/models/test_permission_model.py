import pytest
from api.models import Permission
from api.middlewares.base_validator import ValidationError

class TestPermissionModel:
    """
    Test permission model
    """
    def test_new_permission(self, init_db, new_permission):
        permission = new_permission
        assert permission == new_permission.save()

    def test_count(self):
        assert Permission.count() == 1

    def test_query(self):
        permission_query = Permission.query_()
        assert permission_query.count() == 1
        assert isinstance(permission_query.all(), list)

    def test_update(self, new_permission):
        new_permission.update_(type='Modify')
        assert new_permission.type == 'Modify'

    def test_delete(self, new_permission, request_ctx,
                    mock_request_obj_decoded_token):
        new_permission.delete()
        assert Permission.get(new_permission.id) is None

    def test_permission_model_string_representation(self, new_permission):
        """ Should compute the string representation of a permission

        Args:
            new_permission (object): Fixture to create a new permission
        """
        assert repr(new_permission) == f'<Permission {new_permission.type}>'
