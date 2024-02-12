"""Module to handle bot cancel actions"""

from bot.utilities.constants import CANCEL_MSG
from ...attachments.elements.reasons import cancel_reason_options


class CancelActions:
    """Handles actions that cancels hotdesk"""
    @classmethod
    def cancel_hotdesk_request(cls, **kwargs):
        """Instance method which handles cancel actions
        Args:
            self (Instance): ActionResource instance
        Returns:
        (dict): cancel message
        """
        return {'text': CANCEL_MSG}

    @classmethod
    def cancel_hot_desk_reason_options(cls, **kwargs):
        """Method that handles the pre-select options
        Args:
            **kwargs: data of the choice made
        Returns: (dict): reasons for leaving options
        """
        return cancel_reason_options()
