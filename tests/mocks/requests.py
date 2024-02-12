""" Request data for the Request model"""

INVALID_REQUEST_DATA = {
    "subject": "subject of request",
    "requestTypeId": "<request_type_id>",
    "centerId": "<center_id>",
    "description": "description_of_request",
    "requesterId": "<token_id>",
    "status": "doremifasolatido",
}

VALID_ATTACHMENTS = [
    '{"url": "https://somerandomimage.com/image.jpg"}',
    '{"url": "https://somerandomimage.com/image.jpg"}'
]

VALID_JSON_ATTACHMENTS = [{
    "url": "https://somerandomimage.com/image.jpg"
}, {
    "url": "https://somerandomimage.com/image.jpg"
}]

EXPECTED_REQUEST_RESPONSE_KEYS = [
    "id", "subject", "serialNumber", "requestType", "centerId", "description",
    "attachments", "requester", "responder", "assignee", "status",
    "closedBySystem", "inProgressAt", "completedAt", "closedAt", "dueBy",
]

VALID_REQUEST_DATA = {
    "subject":
    "subject of request",
    "requestTypeId":
    "-LSkH6iyQFboAFf65dvt",
    "centerId":
    "-LSkH67q4Jx6BfIWeTYT",
    "description":
    "description of request",
    "attachments": [
        '{"image_url": "https://somerandomimage.com/image.jpg"}',
        '{"image_url": "https://somerandomimage.com/image.jpg"}'
    ],
    "requesterId":
    "-LSkH6DChFpXqox7TeTi"
}

VALID_REQUEST_DATA_WITH_ASSIGNEE_ID = {
    "subject":
    "subject of request",
    "requestTypeId":
    "-LSkH6iyQFboAFf65dvt",
    "centerId":
    "-LSkH67q4Jx6BfIWeTYT",
    "description":
    "description of request",
    "attachments": [
        '{"image_url": "https://somerandomimage.com/image.jpg"}',
        '{"image_url": "https://somerandomimage.com/image.jpg"}'
    ],
    "requesterId":
    "-LSkH6DChFpXqox7TeTi",
    "assigneeId":
    "-LSkH6DChFpXqox7TeTi",
    "status":
    "open"
}

INVALID_REQUEST_ATTACHMENT_DATA = {
    "subject": "subject99_of_request_checking_well well______well",
    "requestTypeId": "-LSkH6iyQFboAFf65dvt",
    "centerId": "-LSkH67q4Jx6BfIWeTYT",
    "description": "description_of_request ",
    "attachments": "attachments",
    "requesterId": "-LSkH6DChFpXqox7TeTi"
}

INCOMPLETE_REQUEST_DATA = {
    "subject":
    "subject99_of_request_checking_well well______well",
    "requestTypeId":
    "-LSkH6iyQFboAFf65dvtfgg",
    "description":
    "description_of_request ",
    "attachments": [
        '{"image_url": "https://somerandomimage.com/image.jpg"}',
        '{"image_url": "https://somerandomimage.com/image.jpg"}'
    ],
    "requesterId":
    "-LSkH6DChFpXqox7TeTi"
}

EMPTY_REQUEST_SUBJECT_DATA = {
    "subject":
    "                        ",
    "requestTypeId":
    "-LSkH6iyQFboAFf65dvtfgg",
    "description":
    "description_of_request ",
    "attachments": [
        '{"image_url": "https://somerandomimage.com/image.jpg"}',
        '{"image_url": "https://somerandomimage.com/image.jpg"}'
    ],
    "requesterId":
    "-LSkH6DChFpXqox7TeTi"
}
EMPTY_REQUEST_DESCRIPTION_DATA = {
    "subject":
    "some data here",
    "requestTypeId":
    "-LSkH6iyQFboAFf65dvtfgg",
    "description":
    "        ",
    "attachments": [
        '{"image_url": "https://somerandomimage.com/image.jpg"}',
        '{"image_url": "https://somerandomimage.com/image.jpg"}'
    ],
    "requesterId":
    "-LSkH6DChFpXqox7TeTi"
}

SUMMARY_REQUEST = {
    'requestSummary': {
        'totalClosedRequests': 0,
        'totalInProgressRequests': 0,
        'totalOpenRequests': 1,
        'totalOverdueRequests': 0,
        'totalRequests': 1,
        'totalCompletedRequests': 0
    }
}

INVALID_REQUEST_DATA_LONG_DESCRIPTION = {
    "subject":
    "subject of request",
    "requestTypeId":
    "-LSkH6iyQFboAFf65dvt",
    "centerId":
    "-LSkH67q4Jx6BfIWeTYT",
    "description":
    "description of request"*500,
    "attachments": [
        '{"image_url": "https://somerandomimage.com/image.jpg"}',
        '{"image_url": "https://somerandomimage.com/image.jpg"}'
    ],
    "requesterId":
    "-LSkH6DChFpXqox7TeTi"
}
