SLACK_BOT_TOKEN = 'xoxp-330188647298-170092339671-125057470002-6k0f65cbc28v17dde998288624b1c091'
SLACK_CHANNEL = 'DEL99ZHK1'
ATTACHMENT = [{}]
MSG = 'Make a HotDesk Request:'
SLACK_USER = {
    "id": "UG871G3TQ",
    "team_id": "TFL57J56W",
    "name": "olusola.oseni",
    "deleted": False,
    "color": "9b3b45",
    "real_name": "Kenneth Oseni",
    "tz": "Africa/Algiers",
    "tz_label": "Central European Time",
    "tz_offset": 3600,
    "profile": {
        "title": "",
        "phone": "",
        "skype": "",
        "real_name": "Kenneth Oseni",
        "real_name_normalized": "Kenneth Oseni",
        "display_name": "kenneth",
        "display_name_normalized": "kenneth",
        "status_text": "",
        "status_emoji": "",
        "status_expiration": 0,
        "avatar_hash": "gb45d1e18a08",
        "email": "01u501a.053n1@andela.com",
        "image_24": "https://secure.gravatar.com/avatar/b45d1e18a08bcd266f9fda67075b3aa6.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0004-24.png",
        "image_32": "https://secure.gravatar.com/avatar/b45d1e18a08bcd266f9fda67075b3aa6.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0004-32.png",
        "image_48": "https://secure.gravatar.com/avatar/b45d1e18a08bcd266f9fda67075b3aa6.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0004-48.png",
        "image_72": "https://secure.gravatar.com/avatar/b45d1e18a08bcd266f9fda67075b3aa6.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0004-72.png",
        "image_192": "https://secure.gravatar.com/avatar/b45d1e18a08bcd266f9fda67075b3aa6.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0004-192.png",
        "image_512": "https://secure.gravatar.com/avatar/b45d1e18a08bcd266f9fda67075b3aa6.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2F00b63%2Fimg%2Favatars%2Fava_0004-512.png",
        "status_text_canonical": "",
        "team": "TFL57J56W"
    }
}

ACTIONS = [{'value': '1M 102'}]

HOT_DESK_REQUEST = {
    'id': '-LaUR7VXhPhMjSUwH78K',
    'deleted': False,
    'createdAt': '2019-03-21T08:49:06.083295+00:00',
    'updatedAt': None,
    'deletedAt': None,
    'createdBy': None,
    'updatedBy': None,
    'deletedBy': None,
    'email': 'testemail@andela.com',
    'status': 'pending',
    'hotDeskRefNo': '1st 102',
    'requester': {
        'name': 'Ayo',
        'imageUrl': 'http://some_url',
        'email': 'testemail@andela.com',
        'center': {
          'name': 'YtdJMr',
          'image': {
              'metadata': 'tTxlRK'
          },
            'id': '-LaUR7UNW-fvrhrR-qjd',
            'staffCount': 2
        },
        'role': {
            'description': 'reports to the operations coordinator',
            'title': 'Operations Intern',
            'id': '-LaUR7URXqojunC5j8iO'
        },
        'tokenId': '-LaUR5_1TWdCsINjcxTL'
    },
    'requestsCount': 2,
    'reason': None
}

APPROVAL_RESPONSE_WITH_ID = {
    SLACK_USER['profile']['email']:
        {
            'ok': True,
            'channel': 'HI3DJ7HDK',
            'ts': '1555882291.001400',
            'message': {
                'bot_id': 'GFKELS6YU',
                'type': 'message', 
                'text': 'Someone just booked an hotdesk',
                'user': 'HIJHDJHE',
                'ts': '1555882291.001400',
                'attachments': []
            }
    }
}


APPROVAL_RESPONSE = {
    'ok': True,
    'channel': 'HI3DJ7HDK',
    'ts': '1555882291.001400',
    'message': {
        'bot_id': 'GFKELS6YU',
        'type': 'message', 
        'text': 'Someone just booked an hotdesk',
        'user': 'HIJHDJHE',
        'ts': '1555882291.001400',
        'attachments': []
    }
}
