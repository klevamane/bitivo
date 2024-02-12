

def yes_or_no_button(yes_name, yes_value='yes', no_name='cancel',no_value='no'):
    """Method which creates a yes or no button

        Args:
            yes_name (str): name of the yes action
            yes_value (str): value of the yes action
            no_name (str):  name of the no action
            no_value (str):  value of the yes action

        Returns: yes or no button
    """
    return [{
        "fallback":
        "",
        "callback_id":
        "yes_or_no_buttons",
        "color":
        "danger",
        "actions": [
            {
                "type": "button",
                "text": "Yes",
                "name": yes_name,
                "style": "primary",
                "value": yes_value
            },
            {
                "type": "button",
                "text": "No",
                "name": no_name,
                "style": "primary",
                "value": no_value,
            }
            ]
        }]
