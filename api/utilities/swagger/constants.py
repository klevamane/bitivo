EXPORT_USER_REQUEST_PARAMS = {
    "name": {"description": "The name of the user"},
    "email": {"description": "Email of the user"},
    "centerId": {"description": "centerId of user"},
    "roleId": {"description": "roleId of user"},
    "status": {"description": "status of user"},
    "imageUrl": {"description": "imageUrl of user"}
}

PAGINATION_PARAMS = {
    "page": {"description": "page number"},
    "limit": {"description": "limit number of items"}
}

USER_REQUEST_PARAMS = {}
USER_REQUEST_PARAMS.update(EXPORT_USER_REQUEST_PARAMS)
USER_REQUEST_PARAMS.update(PAGINATION_PARAMS)

REQ_REQUEST_PARAMS = {
    "description": {"description": "description of the request"},
    "subject": {"description": "subject of request"},
    "sort": {"description": "filters requests"},
    "order": {"description": "orders by asc or desc"},
    "requestTypeId": {"description": "id of request type"},
    "status": {"description": "status of request"},
}
REQ_REQUEST_PARAMS.update(PAGINATION_PARAMS)


ANALYTICS_REQUEST_PARAMS = {
    "report": {"description": "The value of the report query"},
    "startDate": {"description": "The start date in the format (YYYY-MM-DD)"},
    "endDate": {"description": "The end date in the format (YYYY-MM-DD)"}
}


HOTDESK_REQUEST_PARAMS = {
    "requester": {"description": "The requester's token_id"},
    "responder": {"description": "The responder's token_id"},
    "count": {"description": "True or False"},
    "escalation": {"description": "True or False"}
}

HOTDESK_REQUEST_PARAMS.update(PAGINATION_PARAMS)

HOTDESK_CANCEL_REQUEST = {
    "reason": {"description": "Reason for cancellation",
               "enum": ['changedmymind',
                        'leavingearly',
                        'delayedapproval',
                        'seatchanged',
                        'others']}
}
HOTDESK_CANCEL_REQUEST.update(PAGINATION_PARAMS)

SPACE_REQUEST_PARAMS = {
    "centerId": {"description": "center ID"},
    "buildingId": {"description": "building ID"}
}

ASSET_REQUEST_PARAMS = {
    "sort": {"description": "asset attribute"},
    "order": {"description": "sort order"}
}

ASSET_REQUEST_PARAMS.update(PAGINATION_PARAMS)

ASSET_ANALYTICS_REQUEST_PARAMS = {
    "report": {"description": "The value of the report query"},
    "startDate": {"description": "The start date in the format (YYYY-MM-DD)"},
    "endDate": {"description": "The end date in the format (YYYY-MM-DD)"},
}
ASSET_ANALYTICS_REQUEST_PARAMS.update(PAGINATION_PARAMS)

SEARCH_ASSET_BY_DATE_AND_WARRANTY_REQUEST_PARAMS = {
    "start": {"description": "The start date in the format (YYYY-MM-DD)"},
    "end": {"description": "The end date in the format (YYYY-MM-DD)"},
    "warranty_start": {"description": "The warranty start date in the format (YYYY-MM-DD)"},
    "warranty_end": {"description": "The warranty end date in the format (YYYY-MM-DD)"}
}

CATEGORY_REQUEST_PARAMS = {
    "include": "The value of the include query",
    "sort": {"description": "asset category attribute"},
    "order": {"description": "sort order"}
}
CATEGORY_REQUEST_PARAMS.update(PAGINATION_PARAMS)

SINGLE_ASSET_CATEGORY_REQUEST_PARAMS = {
    "include": "The value of the include query"
}

SINGLE_USER_REQUEST_PARAMS = {
    "include": "The value of the include query"
}

HISTORY_REQUEST_PARAMS = {
    "resourceId": {"description": "The resource ID"},
    "resourceType": {"description": "The reource type"}
}
HISTORY_REQUEST_PARAMS.update(PAGINATION_PARAMS)

SINGLE_REQUEST_PARAMS = {
    "include": "The value of the include query"
}

SCHEDULE_REQUEST_PARAMS = {
    "created_by": {"description": "Schedule created by"}
}
SCHEDULE_REQUEST_PARAMS.update(PAGINATION_PARAMS)

HOTDESK_ANALYTICS_REQUEST_PARAMS = {
    "report": {"description": "The value of the report query"},
    "frequency": {"description": "The value of the frequency query"},
    "startDate": {"description": "The start date in the format (YYYY-MM-DD)"},
    "endDate": {"description": "The end date in the format (YYYY-MM-DD)"}
}

MAINTENANCE_CATEGORY_REQUEST_PARAMS = {
    "centerId": {"description": "center ID"},
    "title": {"description": "The value of the title query"},
}
MAINTENANCE_CATEGORY_REQUEST_PARAMS.update(PAGINATION_PARAMS)
