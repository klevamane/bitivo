"""Module to handle bot response actions"""


class ResponseActions:
    """Handles all message related actions"""

    def persist_reject_payload(self, choice_name, result, action_dict={}):
        """Method that saves dialog submission action payload into action_dict
        Args:
            choice_name(str): name of interactive button clicked
            result(list): dialog submission action payload
            action_dict(dict): a combination of interactive action payload and dialog submission action payload
        Returns:
            None
        """
        if choice_name == 'reject':
            action_dict.update(result)


