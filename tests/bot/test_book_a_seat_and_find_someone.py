"""Module to test book a seat and find someone buttons."""

# AvailableActions
from bot.views.bot_actions.available_actions import AvailableActions


class TestBookSeatFindSomeone:
    """Tests book a seat and find someone buttons."""

    def test_book_a_seat_and_find_someone_button_display_success(self, client, init_db):
        """ Tests book a seat and find someone buttons.
            Args:
                self(Instance): TestBookSeatFindSomeone instance
                init_db (object): Initialize the test database
            Returns:
                None
        """
        choice = {'choice': 'lagos'}
        available_actions_obj = AvailableActions
        response = available_actions_obj.get_book_seat_find_someone_buttons(**choice)

        assert response['text'] == 'What will you like to do today?'
        assert response['attachments'][0]['actions'][0]['name'] == 'Book a seat'
        assert response['attachments'][0]['actions'][1]['name'] == 'Find someone'
