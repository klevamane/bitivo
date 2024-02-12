import pytest
import random
from unittest.mock import Mock, MagicMock, patch

from api.middlewares.base_validator import ValidationError
from api.models import Asset, AssetCategory, Center, WorkOrder, User
from api.models.base.base_policy import BasePolicy
from api.utilities.helpers.check_user_role import is_super_user


class TestBasePolicy(object):
    """Class to test model delete validator."""

    def test_delete_center_when_owner_or_super_user_succeeds(
            self, init_db, new_user_three, request_ctx,
            mock_request_three_obj_decoded_token, new_work_order):
        """Test delete on model when owner or super user succeeds"""
        new_user_three.save()
        new_work_order.save()
        new_work_order.delete()
        super_user = is_super_user(new_user_three.token_id)
        assert super_user == True
        assert WorkOrder.get(new_work_order.id) is None

    def test_delete_center_when_not_super_user_or_super_user_fails(
            self, init_db, new_user_three, request_ctx,
            mock_request_three_obj_decoded_token, test_center_with_users):
        """Test delete on model when not owner or super user fails """
        new_user_three.save()
        test_center_with_users.save()
        with pytest.raises(ValidationError):
            test_center_with_users.delete()

    def test_check_policy(self, init_db, new_user_three, request_ctx,
                          mock_request_three_obj_decoded_token):
        """Test check the check_policy"""
        request_type = 'patch'
        new_user_three.save()
        check = BasePolicy.check_policy(request_type, User,
                                        'make changes to this')
        assert request_type == 'patch'
        assert check is None

    def test_check_request(self, init_db, new_user_three, request_ctx,
                           mock_request_three_obj_decoded_token):
        """Test check the request_type """
        request_type = 'patch'
        new_user_three.save()
        check = BasePolicy.check_request_type(request_type, User)
        assert request_type == 'patch'

    def test_delete_check_policy(self, init_db, new_user_three, request_ctx,
                                 mock_request_three_obj_decoded_token):
        """Test delete fails when user is not authorized to perform action """
        request_type = 'delete'
        new_user_three.save()
        with pytest.raises(ValidationError):
            BasePolicy.check_policy(request_type, Center,
                                    'make changes to this')
