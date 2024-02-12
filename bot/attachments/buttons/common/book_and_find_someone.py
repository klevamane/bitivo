""" Module for book a seat and find someone button. """

# Cancel and Back buttons
from .menu import cancel_button, back_button_action

book_seat_find_someone_buttons = [{
    "fallback": "",
    "callback_id": "book_seat_find_person",
    "color": "#3AA3E3",
    "actions": [
        {
            "name": "Book a seat",
            "type": "button",
            "value": "Book a seat",
            "text": "Book a seat",
            "style": "primary"
        },
        {
            "name": "Find someone",
            "type": "button",
            "value": "Find someone",
            "text": "Find someone",
            "style": "primary"
        },
        cancel_button
    ]
}, back_button_action]
