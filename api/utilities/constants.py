import os
"""Module for storing constants"""

XLSX = 'xlsx'
CHARSET = 'utf-8'
MIMETYPE = 'application/json'
MIMETYPE_TEXT = 'text'
MIMETYPE_CSV = 'text/csv'
EXCLUDED_FIELDS = [
    'deleted', 'created_by', 'updated_by', 'deleted_by', 'deleted_at'
]
REDUNDANT_FIELDS = ['asset', 'status', 'updated_at', 'created_at']
MIMETYPE_FORM_DATA = 'multipart/form-data'
PERMISSION_TYPES = {
    'GET': 'View',
    'PATCH': 'Edit',
    'POST': 'Add',
    'DELETE': 'Delete'
}

HOT_DESK_HISTORY_MESSAGES = {
    'request_created': 'Hot desk request submitted',
    'pending_approval': 'Pending approval from ',
}
ASK_FEJI = 'Assignee not found. Ask Feji'

FULL_ACCESS = 'Full Access'

ASSET_REPORT_QUERIES = [
    'assetflow', 'assetinflow', 'assetoutflow', 'stocklevel', 'incidencereport'
]

HOT_DESK_REPORT_QUERIES = ['requests']

START_DATE = '2018-01-01'
STATS = 'stats'

DATE_COLUMNS = ['created_at', 'updated_at', 'deleted_at', 'warranty']

QUERY_COLUMNS = {
    'start': {
        'column': 'created_at',
        'filter': 'ge'
    },
    'end': {
        'column': 'created_at',
        'filter': 'le'
    },
    'warranty_start': {
        'column': 'warranty',
        'filter': 'ge'
    },
    'warranty_end': {
        'column': 'warranty',
        'filter': 'le'
    }
}

USER_SCHEMA_FIELDS = [
    'email', 'name', 'image_url', 'token_id', 'role.id', 'role.description',
    'role.title', 'center'
]

STORE = 'store'

REQUEST_TYPE_TIME_FIELDS = ['closureTime', 'responseTime', 'resolutionTime']
YOU = 'you'
ACTIVO_SYSTEM = 'Activo System'

REQUEST_TYPE_TIME_MAX_VALUES = {
    "days": 30,
    "hours": 24,
    "minutes": 60,
}

VALID_TIME_UNITS = REQUEST_TYPE_TIME_MAX_VALUES.keys()
HEADERS = [
    'Tag', 'Date of Purchase', 'Item description', 'Name of Manufacturer',
    'Model', 'Assignee', 'Maintenance Period',
    'Operation Maintenance Instructions', 'Warranty', 'Status', 'Initial cost'
]

REQUEST_FIELDS = [
    "subject", "description", "center_id", "request_type_id", "attachments"
]

INDEX_DATA = {
    'et chairs': {
        'tag': 0,
        'assignee': 7,
        'area_name': 0,
        'remove_cell': [0, 5, 12, 13]
    },
    'et workstations': {
        'tag': 0,
        'assignee': 8,
        'area_name': 1,
        'remove_cell': [0, 1, 6, 13, 14]
    }
}
COLUMN_REPLACER = {
    'r': 'S/N',
    'Code ID Ref.': 'Tag',
    'Location/Areas served': 'Assignee',
    'Condition': 'Status',
    'Warranty/Guarantee data': 'Warranty',
    'Maintenance period/History': 'Maintenance period'
}

AREA_DATA = [
    'KAMPALA', 'GOLD COAST', 'NAIJA', 'EKO', 'THE CITY BY THE BAY',
    'BIG APPLE WING', 'SAFARI', '5TH FLOOR EKO WING'
]
CELL_DATA = [
    31, 'WORK SPACE', 'OPEN WORK SPACE', 'MEETING ROOM',
    'PHONE BOOTHS & STUDIO', 'CHILL ZONES/QUIET ROOM', 'QUIET ROOM LOUNGE',
    'PHONE BOOTHS & QUIET ROOM', ''
]
CELL_REPLACER = {
    'Good': 'ok',
    'PEOPLE&CULTURE OFFICE': 'PEOPLE OFFICE',
    'N/A': ''
}

HOT_DESK_REPORT_QUERY_PARAMS = [
    'approvedrequests',
    'rejectedrequests',
    'pendingrequests',
    'currentallocations',
    'trendsallocations',
]

HOT_DESK_QUERY_PARAMS = [
    "requester", "cancel", "report", "responder", "count", "escalation"
]

HOT_DESK_TRUE_VALUE = ['true']

HOT_DESK_QUERY_KEYS = ['frequency', 'startDate', 'endDate', 'report']

HOT_DESK_REPORT_FREQUENCY = ['day', 'month', 'week', 'year', 'quarter']

HOT_DESK_EMAIL_TEMPLATE = 'hot_desk_email_template'

HOT_DESK_SCHEMA_FIELDS = [
    'id', 'created_at', 'updated_at', 'status', 'seat_number', 'requester'
]

RESPONDER_SCHEMA_FIELDS = ['name', 'token_id', 'image_url']

HOT_DESK_STATUS_VALUE = ['approved', 'rejected', 'missed']

HOT_DESK_CANCELLATION_VALUE = [
    'changedmymind', 'delayedapproval', 'leavingearly', 'seatchanged', 'others'
]

NO_ACCESS = 'No Access'

ALLOWED_FILE_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
