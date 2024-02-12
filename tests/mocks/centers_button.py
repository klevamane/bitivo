center_buttons = [{
    "fallback":
    "",
    "response_url": "",
    'message_type':
    'main messa',
    "callback_id":
    "some_id",
    "color":
    "#3AA3E3",
    "actions": [{
        "type": "button",
        "text": "Andela Lagos",
        "name": "lagos",
        "style": "primary",
        "value": "lagos"
    },
                {
                    "type": "button",
                    "text": "Andela Uganda",
                    "name": "kampala",
                    "style": "primary",
                    "value": "kampala"
                },
                {
                    "type": "button",
                    "text": "Andela Kenya",
                    "name": "nairobi",
                    "style": "primary",
                    "value": "nairobi"
                },
                {
                    "name": "cancel",
                    "type": "button",
                    "value": "cancel",
                    "text": "Cancel",
                    "style": "danger",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Are you sure you don't want an Hot Desk?",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }]
}]
