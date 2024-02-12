"""Buttons for displaying all centers
"""
from .menu import cancel_button
import math

def get_menu_buttons(centers_list, include_cancel_button=False):
    """function which generate menu buttons
    Args:
        centers_list (list): list containing action details.
    Returns: list
    """
    if include_cancel_button:
        centers_list.append(cancel_button)

    limit = 5
    count = math.ceil(len(centers_list) / limit)

    output = []

    for i in range(1, count + 1):

        if i == 1:
            entries = centers_list[0:limit]
        else:
            entries = centers_list[(limit * (i - 1)):(limit * i)]
        
        actions = [{
            "type": "button",
            "text": dict_['name'],
            "name": dict_['name'],
            "style": dict_.get('style', "primary"),
            "value": dict_['name']
        } for dict_ in entries]

    
        output.append({
                "fallback": "",
                "response_url": "",
                'message_type': 'main messa',
                "callback_id": "some_id",
                "color": "#3AA3E3",
                "actions": actions
            })

    return output


def add_cancel_button(centers_list):
    """function  which handles all adding of cancel button
    Args:
        centers_list (list): list containing action details.
    Returns: list
    """
    menu_buttons = get_menu_buttons(centers_list, include_cancel_button=True)
    return menu_buttons
