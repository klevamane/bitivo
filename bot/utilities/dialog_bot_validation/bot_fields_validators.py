""" Validates the bot dialog"""

from bot.utilities.dialog_serialization_errors import BOT_DIALOG_ERROR
from bot.utilities.helpers.bot_helpers import process_dialog_error_data


def cancel_hot_desk_dialog_validator(reason):
    """
    Method that validates the other cancel hot desk reason dialog
    Args:
        reason(str): reason for cancellation
    Return:
        Dict: Dictionary of the error
    """

    if not reason or not reason.strip():
        error_data = {
            'cancelled_reason': BOT_DIALOG_ERROR['not_empty']
        }

        return process_dialog_error_data(error_data=error_data)
