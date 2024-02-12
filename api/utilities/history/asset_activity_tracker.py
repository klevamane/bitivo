"""Module to track activities on an Asset"""
# library
from sqlalchemy import or_

# Tracker
from .activity_tracker import ActivityTracker


class AssetActivityTracker(ActivityTracker):
    """Track Activity of an Asset
    """

    @classmethod
    def convert_id_to_name(cls, column, new_value_id, old_value_id):
        """Query db to get Resource 'name' from ID

        Args:
            column (String): table column
            new_value_id (String): resource id
            old_value_id (String): resource id

        Returns:
            tuple
        """
        # imported here to avoid looping imports
        from api.models import User, Space

        # assignee can be User or Space
        if column == 'assignee_id':
            return cls.get_assignee(column, new_value_id, old_value_id)

        column, model = cls.get_column_model(column)

        new_value, old_value = cls.query_new_and_old_value(
            model, new_value_id, old_value_id)

        new_value, old_value = cls.humanize_model_name((new_value, old_value))

        return column, old_value, new_value

    @classmethod
    def get_assignee(cls, column, new_value_id, old_value_id):
        """Get matching model from column

        Args:
            column (String): table column
            new_value_id (String): new id string
            old_value_id (String): old id string

        Returns:
            tuple
        """
        # imported here to avoid looping imports
        from api.models import User, Space

        column = cls.remove_column_suffix(column)

        for model in (User, Space):
            new_value, old_value = cls.query_new_and_old_value(
                model, new_value_id, old_value_id)

            if new_value and old_value:
                new_name, old_name = cls.humanize_model_name((new_value,
                                                              old_value))
                return column, old_name, new_name

        return cls.get_assignee_for_different_models(column, new_value_id,
                                                     old_value_id)

    @classmethod
    def get_assignee_for_different_models(cls, column, new_value_id,
                                          old_value_id):
        """Get assignee names when old and new values are from different models

        Args:
            column (String): table column
            new_value_id (String): new id string
            old_value_id (String): old id string

        Returns:
            tuple
        """
        # imported here to avoid looping imports
        from api.models import User, Space

        record = User.get(new_value_id)

        if record:
            new_name = record
            old_name = Space.get(old_value_id)
        else:
            new_name = Space.get(new_value_id)
            old_name = User.get(old_value_id)

        new_name, old_name = cls.humanize_model_name((new_name, old_name))

        return column, old_name, new_name
