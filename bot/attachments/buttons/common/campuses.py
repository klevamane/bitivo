from .menu import cancel_button, back_button_action

lagos_buildings = [{
    "fallback":
    "",
    "callback_id":
    "lagos_buttons",
    "color":
    "#3AA3E3",
    "actions": [
        {
            "type": "button",
            "text": "ET",
            "name": "et",
            "style": "primary",
            "value": "et"
        },
        cancel_button
    ]
}, back_button_action]
