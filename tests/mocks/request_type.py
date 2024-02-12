""" Request data for model RequestType. """

# Helpers
from api.utilities.helpers.generate_time import generate_time

RESPONSE_TIME = generate_time()
RESOLUTION_TIME = generate_time()
CLOSURE_TIME = generate_time()
INVALID_REQUEST_TYPE_DATA = {
    "title": "Title of Request type",
    "centerId": "CENTER_ID",
    "assigneeId": "TOKEN_ID",
    "responseTime": RESPONSE_TIME,
    "resolutionTime": RESOLUTION_TIME,
    "closureTime": CLOSURE_TIME
}

VALID_REQUEST_TYPE_DATA = {
    "title": "Plumber maintenance",
    "assigneeId": "ASSIGNEE_ID",
    "centerId": "CENTER_ID",
    "responseTime": RESPONSE_TIME,
    "resolutionTime": RESOLUTION_TIME,
    "closureTime": CLOSURE_TIME
}

REQUEST_TYPE_WITH_MISSING_FIELDS = {
    "title": "Computer damage",
    "responseTime": {
        "hours": 4,
        "minutes": 5,
    },
    "resolutionTime": {
        "days": 3,
        "minutes": 5,
    },
    "closureTime": CLOSURE_TIME
}
REQUEST_TYPE_WITH_MISSING_RESOLUTION_TIME = {
    "title": "Computer damage",
    "resolutionTime": {
        "days": 3,
        "minutes": 5,
    },
    "closureTime": CLOSURE_TIME
}

REQUEST_TYPE_WITH_RESPONSE_TIME = {
    "title": "New Computer",
    "resolutionTime": {
        "days": 3,
        "minutes": 5,
    },
    "closureTime": CLOSURE_TIME
}
SUCCESS_RESPONSE = {
    "data": {
        "title": "Plumber maintenance",
        "responseTime": RESPONSE_TIME,
        "resolutionTime": RESOLUTION_TIME,
        "closureTime": CLOSURE_TIME
    },
    "status": "success",
    "message": "Request type successfully created"
}

VALID_REQUEST_TYPE_UPDATE_DATA = {
    "assigneeId": "ASSIGNEE_ID",
    "centerId": "CENTER_ID"
}
