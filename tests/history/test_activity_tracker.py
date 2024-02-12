"""Test ActivityTracker Module"""
from api.utilities.history.activity_tracker import ActivityTracker
from api.utilities.messages.success_messages import HISTORY_MESSAGES
from api.models import Center


class TestActivityTrackerClass:
    """Test ActivityTracker
    """

    def test_generate_activity_message(self):
        """Test generate activity message
        """

        response = ActivityTracker.generate_activity_message("test", "POST")
        assert response == HISTORY_MESSAGES['added_resource']

        response = ActivityTracker.generate_activity_message("test", "DELETE")
        assert response == HISTORY_MESSAGES['removed_resource']

    def test_generate_column_message(self):
        """Test generate message for a column changed
        """
        column, new_value, old_value = "tag", "AND/TRM/001", "AND/TRM/777"
        msg = f"{column} changed from {old_value} to {new_value}, "

        response = ActivityTracker.generate_column_message(
            column, new_value, old_value)

        assert response == msg

    def test_compare_dict(self):
        """Test compare dicts and return the difference
        """
        new_dict, old_dict = {"test": "one"}, None

        response = ActivityTracker.compare_dict(new_dict, old_dict)

        assert response == "test attribute changed to one"

    def test_convert_id_to_name(self, init_db, new_center):
        """Test Id is converted to a name

        Args:
            init_db (db): initialize database
            new_center (fixture): fixture for new center
        """
        new_center.save()

        column, new_value, old_value = "center_id", new_center.id, "-Id"

        response = ActivityTracker.convert_id_to_name(column, new_value,
                                                      old_value)

        assert response == ('center', new_center.name, 'None')

    def test_get_column_model(self):
        """Test correct model is returned from a column name
        """

        response = ActivityTracker.get_column_model("center_id")

        assert response == ('center', Center)

    def test_remove_column_suffix(self):
        """Test '_id' suffix id removed from column name
        """

        response = ActivityTracker.remove_column_suffix("center_id")

        assert response == 'center'

    def test_humanize_model_name(self):
        """Test model repr is converted to readable form
        """

        response = ActivityTracker.humanize_model_name(
            ("<Center Epic Tower>", ))

        assert list(response) == ['Epic Tower']
