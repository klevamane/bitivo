from .menu import cancel_button, back_button_action


whole_day_button = {
    "name": "The whole day",
    "type": "button",
    "value": "The whole day",
    "text": "The whole day",
    "style": "primary"
}

few_hours_button = {
    "name": "A few hours",
    "type": "button",
    "value": "A few hours",
    "text": "A few hours",
    "style": "primary"
}

whole_day_few_hours_btns = [{
    "fallback": "",
    "callback_id": "whole_day_few_hours_btns",
    "color": "#3AA3E3",
    "actions": [whole_day_button, few_hours_button,
                cancel_button
                ]
}, back_button_action]
