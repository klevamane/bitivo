from bot.utilities.user_hot_desk import get_pending_or_approved_hot_desk, cancel_hot_desk_by_id
from api.utilities.messages.success_messages import SUCCESS_MESSAGES
    
class TestUserHotDesk:
    """Tests the user hot dest data in db"""

    def test_get_pending_or_approved_hot_desk_succeeds(self, 
        init_db, new_user, new_today_hot_desk):
        """ Tests get pending or approved hot desk of a user
        Args:
            self(instance): Instance of TestUserHotDesk
            init_db (SQLAlchemy): fixture to initialize the test database
            new_user (User): fixture to create requester
            new_today_hot_desk (HotDesk): fixture for creating an hot desk
        """

        new_today_hot_desk.save()
        response = get_pending_or_approved_hot_desk(new_user.email)

        assert response['hotDeskRefNo'] == new_today_hot_desk.hot_desk_ref_no
        assert response['status'] == 'approved'
        assert response['requester']['tokenId'] == new_today_hot_desk.requester_id
        assert response['deleted'] == False


    def test_get_delete_hot_desk_by_id_succeeds(self, init_db, 
        new_user, new_today_hot_desk):
        """ Tests delete an hot desk with of a user
        Args:
            self(instance): Instance of TestUserHotDesk
            new_user (User): fixture to create requester
            init_db (SQLAlchemy): fixture to initialize the test database
            new_today_hot_desk (HotDesk): fixture for creating an hot desk
        """
        
        new_today_hot_desk.save()
        hot_desk = get_pending_or_approved_hot_desk(new_user.email)
        hot_desk_id = hot_desk['id']
        reason = 'hello'
        response = cancel_hot_desk_by_id(hot_desk_id, reason)

        assert response == SUCCESS_MESSAGES['deleted'].format('Hot desk') 
