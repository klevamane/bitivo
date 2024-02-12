"""Module to handle bot spreadsheet handlers"""

from api.utilities.helpers.env_resource_adapter import adapt_resource_to_env
from bot.tasks.slack_bot import BotTasks


class SpreadsheetHandlers:
    """Handles everything related too handling the spreadsheet data"""

    @classmethod
    def update_spreadsheet_handler(cls, **kwargs):
        """Method that calls the update spreadsheet class method
        Args:
            cls (instance): class instance
            result (dict): dictionary containing action details.
        Returns:
            (dict): message
        """
        result = kwargs['result']

        if result['actions'][0]['name'] == 'approve':
            hot_desk_ref_no = ' '.join(
                result['original_message']['text'].split()[-2:])[-7:-1]
            requester = result['original_message']['text'].split()[0]

        adapt_resource_to_env(
            BotTasks.update_spreadsheet.send(result, hot_desk_ref_no))
        return {
            'text':
            f'Request by {requester} for *hot desk - {hot_desk_ref_no}* Approved! :smiley:'
        }
