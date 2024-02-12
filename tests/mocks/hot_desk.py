"""Module for hot desk mock data"""

VALID_HOT_DESK_DATA = {
    "requester_id": "",
    "status": "pending",
    "hot_desk_ref_no": "1G 54",
    "assigneeId": "-LSkH6DChFpXq7TeTi",
    "reason": ""
}


class MyDict(dict):
    """
    Class that overrides the builtin dict object
    """
    pass


SHEET = MyDict()
row = MyDict()

INVALID_HOT_DESK_DATA = {
    "requester_id": "-L594949uy9",
    "assigneeId": "-LSkH6DChFpXq7TeTi",
}
VALID_HOT_DESK_COMPLAINT = {"complaint": "This is a complaint"}
INVALID_HOT_DESK_COMPLAINT = {"complaint": "It"}
INVALID_HOT_DESK_EMPTY_COMPLAINT = {"complaint": ""}
INVALID_HOT_DESK_REQUESTER_ID = {
    "requester_id": "",
    "status": "pending",
    "hot_desk_ref_no": "1G 54",
    "assigneeId": "-LSkH6DChFpXq7TeTi",
    "reason": ""
}

VALID_STATUS_DATA = ["pending", "approved", "rejected"]

VALID_REASON = {"reason": "I will not report to work today"}

INVALID_REASON = {"status": "I will not report to work today"}

REQUESTER_NAME = 'Peace George'

HOTDESK_GOOGLE = ([
    {
        'S/N': 26,
        'Room/Bay': 'Aliyu Abdullahi ',
        'Floor': '',
        '# of seats': '',
        'Name': '',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 27,
        'Room/Bay': 'Inumidun Amao',
        'Floor': '',
        '# of seats': '',
        'Name': '',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 28,
        'Room/Bay': 'Daniel James',
        'Floor': '',
        '# of seats': '',
        'Name': 'Hot desk',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 82,
        'Room/Bay': 'Ofor Chinedu',
        'Floor': '',
        '# of seats': '',
        'Name': 'Hot desk',
        'Hot desk': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 623,
        'Room/Bay': 'Oluwafemi Adeosun',
        'Floor': '',
        '# of seats': '',
        'Name': 'Hot desk',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 632,
        'Room/Bay': 'Philips Blessing',
        'Floor': '',
        '# of seats': '',
        'Name': '',
        'Hot Desk': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 643,
        'Room/Bay': 'Usman Ibrahim',
        'Floor': '',
        '# of seats': '',
        'Name': 'Hot desk',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 626,
        'Room/Bay': 'Chinedu Daniel ',
        'Floor': '',
        '# of seats': '',
        'Name': 'Yahya',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 646,
        'Room/Bay': 'Eguonoghene Efekemo',
        'Floor': '',
        '# of seats': '',
        'Name': 'Dennis',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 642,
        'Room/Bay': 'Olalekan Eyiowuawi',
        'Floor': '',
        '# of seats': '',
        'Name': 'Fegi',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 627,
        'Room/Bay': 'Taiwo Adedotun',
        'Floor': '',
        '# of seats': '',
        'Name': 'Mike',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 634,
        'Room/Bay': 'Michael Ikechi',
        'Floor': '',
        '# of seats': '',
        'Name': 'Faniyi',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 38,
        'Room/Bay': 'Joshua Azemoh',
        'Floor': '',
        '# of seats': '',
        'Name': 'James',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 39,
        'Room/Bay': 'Nnenanya Obinna',
        'Floor': '',
        '# of seats': '',
        'Name': 'Walker',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 40,
        'Room/Bay': 'Ugonna Ofoegbu',
        'Floor': '',
        '# of seats': '',
        'Name': 'Elis',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 41,
        'Room/Bay': 'Abisoye Oke-Lawal',
        'Floor': '',
        '# of seats': '',
        'Name': 'Mike',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 42,
        'Room/Bay': 'Seun Owonikoko',
        'Floor': '',
        '# of seats': '',
        'Name': '',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
    {
        'S/N': 43,
        'Room/Bay': 'Mayowa Makinde',
        'Floor': '',
        '# of seats': '',
        'Name': '',
        'Team': '',
        '': '',
        'Utilisation dashboard': ''
    },
], SHEET)

SLACK_INTERACTIVE_PAYLOAD = {
    "type": "interactive_message",
    "actions": [{
        "name": "Lagos"
    }],
    'channel': {
        'id': 'DJSK2347P',
        'name': 'directmessage'
    },
    "callback_id": "some_id",
    "user": {
        "id": "UJPJ7PW5S",
        "name": "joshua.moracha"
    },
}

SLACK_THE_WHOLE_DAY_PAYLOAD = {
    "type": "interactive_message",
    "actions": [{
        "name": "The whole day"
    }],
    'channel': {
        'id': 'DJSK2347P',
        'name': 'directmessage'
    },
    "callback_id": "some_id",
    "user": {
        "id": "UJPJ7PW5S",
        "name": "joshua.moracha"
    },
}

SLACK_FEW_HOURS_PAYLOAD = {
    "type": "interactive_message",
    "actions": [{
        "name": "A few hours"
    }],
    'channel': {
        'id': 'DJSK2347P',
        'name': 'directmessage'
    },
    "callback_id": "some_id",
    "user": {
        "id": "UJPJ7PW5S",
        "name": "joshua.moracha"
    },
}

SLACK_BOOK_A_SEAT_PAYLOAD = {
    "type": "interactive_message",
    "actions": [{
        "name": "Book a seat"
    }],
    'channel': {
        'id': 'DJSK2347P',
        'name': 'directmessage'
    },
    "callback_id": "some_id",
    "user": {
        "id": "UJPJ7PW5S",
        "name": "joshua.moracha"
    },
}
