""" Mock data used when testing comments"""

MISSING_FIELD_COMMENT = {
    # Missing parentId field
    "body": "This is a test for comment body",
    "parentType": "Request"
}

INVALID_REQUEST_ID_COMMENT = {
    "parentId": "invalid_id",
    "body": "This is a test for comment body",
    "parentType": "Request"
}

INVALID_PARENT_TYPE_COMMENT = {
    "body": "This is a test for comment body",
    "parentType": "Invalid"
}

EMPTY_BODY_MESSAGE = {"body": ""}
COMMENT_UPDATE_BODY = {"body": "this is updated"}
