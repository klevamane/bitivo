# library
from sqlalchemy.orm.attributes import get_history

# constants
from api.utilities.constants import HOT_DESK_HISTORY_MESSAGES
from api.utilities.constants import EXCLUDED_FIELDS

# enum
from api.utilities.enums import HotDeskRequestStatusEnum

# Tracker
from .activity_tracker import ActivityTracker


class HotDeskTracker(ActivityTracker):
    """Track Activity of a Hot Desk Request"""
    excluded = EXCLUDED_FIELDS.copy()
    excluded.extend([
        'complaint_created_at',
    ])

    @classmethod
    def record_history(cls, target, session, action):
        """Records an activity to the History model
        Args:
            target (object): instance of model created/updated/deleted
            session (db): database session
            action (str): request action undertaken

        Returns:
            save to history model and log the activity
        """
        from api.models import History
        msg = cls.generate_activity_message(target, action)
        data = {
            "resource_id": target.id,
            "resource_type": target.__class__.__name__,
            "actor_id": cls.get_actor_id(target),
            "action": cls.generate_action(target),
            "activity": msg
        }

        if msg:
            history = History(**data)
            session.add(history)
        if action == 'POST':
            data['actor_id'] = target.assignee_id
            data['action'] = HotDeskRequestStatusEnum.pending.value
            data['activity'] = HOT_DESK_HISTORY_MESSAGES['pending_approval'] + \
                cls.convert_id_to_name(target.assignee_id)
            history = History(**data)
            session.add(history)

    @classmethod
    def generate_activity_message(cls, target, action):
        """Creates and returns the activity message
        Args:
            action (String): action performed by user
            target (Object): The current model instance

        Returns: String
        """
        activity_mapper = {
            "POST": cls.create_columns,
            "PATCH": cls.updated_columns,
        }
        if action in ('PATCH', 'POST'):
            return activity_mapper[action](target)

    @classmethod
    def get_actor_id(cls, target):
        """Get the actor ID of the current user in relation to the action being performed
        Args:
            target (Object): The current model instance
        Returns: String 
        """
        new_value, _, _ = cls.get_column_history(target, 'complaint')
        if new_value:
            return target.requester_id
        new_value, _, _ = cls.get_column_history(target, 'status')
        if new_value and (
                new_value[0] == (HotDeskRequestStatusEnum.pending
                                 or HotDeskRequestStatusEnum.cancelled)):
            return target.requester_id
        return target.assignee_id

    @classmethod
    def get_column_history(clas, target, column_name):
        """Creates and returns the activity message
        Args:
            target (Object): The current model instance
            column_name (String): Column to get history from

        Returns: String
        """
        for column in target.__table__.columns:
            column = column.key
            if column == column_name:
                return get_history(target, column)

    @classmethod
    def generate_action(cls, target):
        """Creates and returns the activity message
        Args:
            target (Object): The current model instance
        Returns: String
        """
        new_value, _, _ = cls.get_column_history(target, 'complaint')
        if new_value:
            return 'complaint'
        new_value, current_value, old_value = cls.get_column_history(
            target, 'status')
        if new_value and new_value[0] == HotDeskRequestStatusEnum.pending:
            return f'created'
        return new_value[0].value if new_value else current_value[0].value

    @classmethod
    def create_columns(cls, target):
        """Creates and returns an activity message
            when a hot desk request is created
        Args:
            target (Object): The current model instance
        Returns: String
        """
        message = HOT_DESK_HISTORY_MESSAGES['request_created']
        return f'{message}'

    @classmethod
    def generate_column_message(cls, column, new_value, old_value):
        """Generate msg for each column that was updated
        Args:
            column (String): column changed
            new_value (dict): value of new dict
            old_value (dict): value of old dict
        Returns:
            String
        """
        if isinstance(new_value, HotDeskRequestStatusEnum):
            return cls.get_status(new_value)
        if column.endswith('_id'):
            name = cls.convert_id_to_name(new_value)
            message = HOT_DESK_HISTORY_MESSAGES['pending_approval']
            return f"{message}{name}, "
        if column == 'complaint':
            return f'Complaint: {new_value}'
        return '' if new_value == '' else f"Reason: {new_value}, "

    @classmethod
    def get_status(cls, status):
        """Get the status change message

        Args:
            status (String): Incoming status of the request

        Returns:
            string: Message upon status change
        """
        if status == HotDeskRequestStatusEnum.approved:
            return 'Request approved'
        return "Request cancelled, " if status == HotDeskRequestStatusEnum.cancelled else "Request rejected, "

    @classmethod
    def convert_id_to_name(cls, user_id):
        """Query db to get User 'name' from ID
        Args:
            user_id (String): User ID
        Returns:
            string: name of the user
        """
        from api.models import User
        return User.query_().filter_by(token_id=user_id).first().name
