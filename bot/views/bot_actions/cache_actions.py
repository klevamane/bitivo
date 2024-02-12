"""Module to handle bot cache actions"""
from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env


class CacheActions:
    """Handles all cache related actions"""

    def check_availability_of_cached_data(self, slack_floors):
        """Method that checks if cached data is available
        Args:
            slack_floors(list):
        Returns:
            None
        """
        if slack_floors is None:

            from bot.views.slack_bot import initialize_bot

            # initialize_bot_data = adapt_resource_to_env(initialize_bot.delay)
            initialize_bot_data = adapt_resource_to_env(initialize_bot.send)
            initialize_bot_data(True)
