"""Module for hot desk email templates and sendgrid template ids

    Dictionaries defined here:
        hot_desk_email_templates: holds all hot desk transactional email templates.
                       The template information include an id and template_data. template_data
                       holds dynamic template variables.

"""

hot_desk_email_template = {
    'notify_ops_hotdesk': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_ops_hotdesk.html',
        },
        'default_data': {
            "username": "Camille",
            "floor": "1st",
            "seatNumber": "65",
            "requester_name": "Ayo",
        }
    },
    'escalate_email': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/escalate_email.html',
        },
        'default_data': {
            "username": "Ali",
            "floor": "3rd",
            "seatNumber": "43",
            "approverFName": "John",
            "approverLName": "Obi"
        }
    },
    'notify_hotdesk_rejection': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_hotdesk_rejection.html'
        },
        'default_data': {
            "requesterName": "Muche",
            "floor": "3rd Floor",
            "seatNumber": "3S",
            "firstName": "Sola",
            "lastName": "Oguntimehin"
        }
    },
    'notify_hotdesk_approval': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_hotdesk_approval.html',
        },
        'default_data': {
            "username": "Ali",
            "floor": "3rd",
            "seatNumber": "43",
            "firstName": "John",
            "lastName": "Obi"
        }
    },
    'notify_hotdesk_cancelling': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_hotdesk_cancelling.html',
        },
        'default_data': {
            "username": "Ali",
            "floor": "3rd",
            "seatNumber": "43",
            "firstName": "John",
            "lastName": "Obi"
        }
    }
}
