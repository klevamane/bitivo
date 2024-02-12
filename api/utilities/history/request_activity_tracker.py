# Tracker
from .activity_tracker import ActivityTracker


class RequestTracker(ActivityTracker):
    """Track Activity of a Request
    """

    @classmethod
    def convert_id_to_name(cls, column, new_value_id, old_value_id):
        """Query db to get Resource 'name' from ID

        Args:
            column (String): table column
            new_value_id (String): resource id
            old_value_id (String): resource id

        Returns:
            tuple: column, new_value_id, old_value_id
        """
        if column in ['assignee_id', "requester_id", "responder_id"]:
            # imported here to avoid cyclic dependancy
            from api.models import User

            return super().convert_id_to_name(column, new_value_id,
                                              old_value_id, User)

        return super().convert_id_to_name(column, new_value_id, old_value_id)
