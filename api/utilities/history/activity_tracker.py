"""Module to track activity of a resource"""
# system
import re

# library
from sqlalchemy.orm.attributes import get_history

# constants
from api.utilities.constants import EXCLUDED_FIELDS
from api.utilities.constants import PERMISSION_TYPES

# messages
from api.utilities.messages.success_messages import HISTORY_MESSAGES


class ActivityTracker():
    """Track Activity of a given resource
    """
    excluded = EXCLUDED_FIELDS.copy()
    excluded.extend(['updated_at', 'date_assigned', 'assignee_type'])

    @classmethod
    def record_history(cls, target, request, session):
        """Records an activity to the History model

        Args:
            target (object): instance of model created/updated/deleted
            request (object): request performed by user
            session (db): database session

        Returns:
            save to history model and log the activity
        """
        # imported here to avoid looping imports
        from api.models import History, User

        user_id = request.decoded_token['UserInfo']['id']
        action_verb = request.method

        # actor id should exist in the db
        # this check ensures actor is in the db
        User.get_or_404(user_id)

        msg = cls.generate_activity_message(target, action_verb)

        data = {
            "resource_id": target.id,
            "resource_type": target.__class__.__name__,
            "actor_id": user_id,
            "action": PERMISSION_TYPES[action_verb],
            "activity": msg
        }

        if msg:
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
            "POST": HISTORY_MESSAGES['added_resource'],
            "PATCH": cls.updated_columns,
            "DELETE": HISTORY_MESSAGES['removed_resource'],
        }

        if action == 'PATCH':
            return activity_mapper[action](target)

        return activity_mapper[action]

    @classmethod
    def updated_columns(cls, target):
        """Gets the updated columns

        Args:
            target (Object): The current model instance

        returns:
            String of updated columns
            Example:
                tag changed from EEE/AAA/012 to EEE/AAA/013
                'color attribute changed to blue' in custom attributes
                assingee changed from John to Doe
        """

        msg = ""

        for column in target.__table__.columns:
            column = column.key

            new_value, _, old_value = get_history(target, column)

            if new_value and column not in cls.excluded:
                msg += cls.generate_column_message(column, new_value[0],
                                                   old_value[0])

        return msg.strip(', ')

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

        def to_sentence_case(x):
            return ' '.join(x.split('_'))

        if isinstance(new_value, dict):
            changed_objects = cls.compare_dict(new_value, old_value)
            return f"'{changed_objects}' in {to_sentence_case(column)}, "

        if column.endswith('_id'):
            column, old_value, new_value = cls.convert_id_to_name(
                column, new_value, old_value)
            return f"{to_sentence_case(column)} changed from {old_value} to {new_value}, "

        return f"{to_sentence_case(column)} changed from {old_value} to {new_value}, "

    @classmethod
    def compare_dict(cls, new_value, old_value):
        """Compare value of new dict and value of old dict and returns keys changed

        Args:
            new_value (dict): value of new dict
            old_value (dict): value of old dict

        Returns:
            String
        """

        if not old_value:
            old_value = {}

        dict_difference = dict(new_value.items() - old_value.items())

        return ', '.join([
            '{0} attribute changed to {1}'.format(k, v)
            for k, v in dict_difference.items()
        ])

    @classmethod
    def convert_id_to_name(cls, column, new_value_id, old_value_id,
                           model=None):
        """Query db to get Resource 'name' from ID

        Args:
            column (String): table column
            new_value_id (String): resource id
            old_value_id (String): resource id
            model(object): database model e.g. User

        Returns:
            tuple: column, new_value_id, old_value_id
        """

        if model:
            column = cls.remove_column_suffix(column)
        else:
            column, model = cls.get_column_model(column)

        record = cls.query_new_and_old_value(model, new_value_id, old_value_id)

        old_value, new_value = cls.humanize_model_name(record)

        return column, old_value, new_value

    @classmethod
    def get_column_model(cls, column):
        """Get matching model from column

        Args:
            column (String): table column

        Returns:
            tuple
        """

        from api.models import tables

        column = cls.remove_column_suffix(column)

        model = [x for x in tables if x.__tablename__.startswith(column[:-1])]

        if model:
            model = model[0]

        return column, model

    @classmethod
    def remove_column_suffix(cls, column_name):
        """Removes column suffix to make it searchable in get_column_model()

        Args:
            column_name (String): name of the column
        Returns:
            String
        Example:
            converts center_id to center
        """

        regex = "(.*)_.*"
        matching_text = cls.search_regex(regex, column_name)
        return matching_text

    @classmethod
    def humanize_model_name(cls, names):
        """Convert model name to user friendly

        Args:
            name (String): model name
        Returns: String
        Example:
            converts <Center Epic Tower> to Epic Tower
        """

        regex = "^<\w+\s([^\[\]<>]{2,}).*"
        return (cls.search_regex(regex, str(name)) for name in names)

    @classmethod
    def search_regex(cls, regex, text):
        """Returns matching text from regex

        Args:
            regex (String): regular expression
            text (String): String to run regex on
        Returns: String
        """

        found = re.search(regex, text)
        if found:
            return found.group(1)
        return text

    @classmethod
    def query_new_and_old_value(cls, model, new_value_id, old_value_id):
        """Query new value id and old value id on it respective model

        Args:
            model (Model): class model of resource to query
            new_value_id (String): resource id
            old_value_id (String): resource id

        Returns:
            Dict

        Example:
            [<Center Lagos>, <Center Nairobi>]
        """

        new_value = model.get(new_value_id)
        old_value = model.get(old_value_id)

        return new_value, old_value
