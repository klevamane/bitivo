"""Module for email templates and sendgrid template ids

    Dictionaries defined here:
        email_templates: holds all activo transactional email templates hosted on Sendgrid.
                       The template information include an id and template_data. template_data
                       holds dynamic template variables.


"""

email_templates = {
    'low_in_stock': {
        'sendgrid': {
            'id': 'd-65e620a5dad14058bb37f17ba1319d68',
        },
        'local': {
            'template': '/email/low_in_stock.html',
        },
        'default_data': {
            'user_first_name': "Recipient's first name",
            'asset_category_name': "asset category name",
            'asset_count': 0,
            'asset_status': "Can be either 'running low' or 'low in stock' "
        }
    },
    'logged_category_request': {
        'sendgrid': {
            'id': 'd-113fec63dbf943d3b3216cef3546879d',
        },
        'local': {
            'template': '/email/logged_category_request.html',
        },
        'default_data': {
            "assignee_name": "Olamide",
            "request_category_name": "Plumbing",
            "requester": "Mutua"
        }
    },
    'assign_request_to_technician': {
        'sendgrid': {
            'id': 'd-537d2536d4d34a9fb5dc08a8e1a77b8c',
        },
        'local': {
            'template': '/email/assign_request_to_technician.html',
        },
        'default_data': {
            "username": "Recipient's name",
            "assignee": "the request_type assignee",
            'subject': 'the request subject'
        }
    },
    'requester_status': {
        'sendgrid': {
            'id': 'd-ab34c847a045479d92fe48664189977f',
        },
        'local': {
            'template': '/email/requester_status.html',
        },
        'default_data': {
            "username": "Maureen",
            "subject": "Plumbing Issues",
            "status": "In progress",
            "assignee": "James"
        }
    },
    'closed_by_system': {
        'sendgrid': {
            "id": "d-2352d2f61f654ed6b49bbf73f6303afd",
        },
        'local': {
            'template': '/email/closed_by_system.html',
        },
        'default_data': {
            "assignee": "Chigoziem",
            "subject": "Laptop repair"
        }
    },
    'request_type_assigned': {
        'sendgrid': {
            'id': 'd-578b5f31d0844fcb94931541ddb5ffef',
        },
        'local': {
            'template': '/email/request_type_assigned.html',
        },
        'default_data': {
            'username': 'assignee name',
            'request_category_name': 'asset category name',
            'user': 'assigner name',
        }
    },
    'request_comment': {
        'sendgrid': {
            'id': 'd-95dbbcc95f7f4ee5a56173c66bfc6166',
        },
        'local': {
            'template': '/email/request_comment.html',
        },
        'default_data': {
            "username": "Uche",
            "assignee": "Chika",
            "subject": "Faulty Apple Speaker"
        }
    },
    'notify_assignee_work_order': {
        'sendgrid': {
            'id': 'd-9b37dc76947644ad90fe73e4fb2cfd40',
        },
        'local': {
            'template': '/email/notify_assignee_work_order.html',
        },
        'default_data': {
            "assignerName": "Rachael Goldman",
            "username": "David",
            "workOrder": "Carpentary"
        }
    },
    'notify_assigner_work_order_overdue': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_assigner_work_order_overdue.html',
        },
        'default_data': {
            "assignee": "Rachael Goldman",
            "assigner": "David",
            "work_order": "Carpentary"
        }
    },
    'notify_assigner_work_order_complete': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_assigner_work_order_complete.html',
        },
        'default_data': {
            "assigner_name": "Rachael Goldman",
            "assignee_name": "Goldman Rachael Goldman",
            "work_order": "Carpentary"
        }
    },
    'reassignee_work_order': {
        'sendgrid': {
            'id': 'd-7178e545c3144c999d95b856a48545c3',
        },
        'local': {
            'template': '/email/work_order_user_reassignment.html',
        },
        'default_data': {
            "username": "Meeky",
            "newAssignee": "Chukwuemeka",
            "workOrderTitle": "Chairs Repair"
        }
    },
    'notify_assignee_or_assigner_on_comment': {
        'sendgrid': {
            'id': '',
        },
        'local': {
            'template': '/email/notify_assignee_or_assigner_on_comment.html',
        },
        'default_data': {
            "username": "James",
            "recipient": "Justus",
            "work_order": "Laptop repairs",
            "comment": "Are you done with this laptops?"
        }
    },
    'schedule_due_template': {
        'sendgrid': {
            'id': 'd-ae7ab702e86d4d43ae4ef7d22e68a98a',
        },
        'local': {
            'template': '/email/due_work_order_reminder.html',
        },
        'default_data': {
            "username": "Olamide",
            "tasks": ["Plumbing", "Repairs", "Cleaning"]
        }
    },
    'asset_bulk_template': {
        'local': {
            'template': '/email/asset_bulk.html'
        },
        'default_data': {
            'user': 'Dennis',
            'title': 'Example reasons',
            'response': 'invalid id'
        }
    }
}
