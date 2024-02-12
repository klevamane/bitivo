"""
A set of mock role data for testing role creation
"""

VALID_PERMISSION = {
    "permissionIds": ['-LJyuBgwu7weqZKeVx_e'],
    "resourceId": '-LJyuBgwu7weqZKeVx_e'
}

VALID_ROLE_TITLE_DESCRIPTION = {
    "title": "software developer",
    "description":
        "They build working applications following industry standards",
}
VALID_ROLE_TITLE_DESCRIPTION_TWO = {
    "title": "Country Director",
    "description": "Reports to the board"
}

VALID_ROLE_TITLE_DESCRIPTION_THREE = {
    "title": "Operations Assistant Manager",
    "description": "reports to the operations Manager"
}


VALID_ROLE_TITLE_DESCRIPTION_FOUR = {
    "title": "software Engineer",
    "description":
        "They build working applications following industry standards",
}
ROLE_DATA_WITH_RESOURCE_ACCESS_LEVEL= {
    "title": "software developer",
    "description":
        "They build working applications following industry standards",
    "resourceAccessLevels": VALID_PERMISSION
}

ROLE_DATA_WITH_EMPTY_TITLE = {
    "title": "",
    "description":
        "They build working applications following industry standards",
    "resourceAccessLevels": VALID_PERMISSION
}

ROLE_DATA_WITH_EMPTY_DESCRIPTION = {
    "title": "software developer",
    "description": "",
    "resourceAccessLevels": VALID_PERMISSION
}

ROLE_DATA_WITH_INVALID_TITLE = {
    "title": ".",
    "description":
        "They build working applications following industry standards",
    "resourceAccessLevels": VALID_PERMISSION
}

ROLE_DATA_WITH_INVALID_DESCRIPTION = {
    "title": "software developer",
    "description": "_",
    "resourceAccessLevels": VALID_PERMISSION
}

VALID_ROLE_DATA_TITLE = {"title": "Country Director"}
VALID_DESCRIPTION = {"description": "Reports to the board"}

VALID_ROLE_DATA_TWO = {"title": "Country Director",
                       "resourceAccessLevels": VALID_PERMISSION}


VALID_ROLE_WITHOUT_TITLE = {"description": "Reports to the board",
                            "resourceAccessLevels": VALID_PERMISSION}

VALID_ROLE_DATA = {
    "title": "Learning Facilitator Andela",
    "description": "Reports to Learning Facilitator",
    "resourceAccessLevels": VALID_PERMISSION
}


VALID_UPDATE_ROLE_DATA_DUPLICATED = {"title": "Operations Assistant Manager"}

TEMPLATE_UPDATE_PERMISSION_DATA = {
    "resourceAccessLevels": [{
        "resourceId": "TO_BE_MODIFIED",
        "permissionIds": ["TO_BE_MODIFIED"]
    }]
}

VALID_ROLE_WITH_EMPTY_PERMISSION = {
    **VALID_ROLE_TITLE_DESCRIPTION, "resourceAccessLevels": []
}

VALID_ROLE_WITH_EMPTY_OBJECT_PERMISSION = {
    **VALID_ROLE_TITLE_DESCRIPTION, "resourceAccessLevels": [{}]
}

# Invalid data

ROLE_WITH_INVALID_PERMISSION = {
    **VALID_ROLE_TITLE_DESCRIPTION, "resourceAccessLevels": ['']
}

ROLE_WITH_INVALID_RESOURCE_ACCESS_LEVEL = {
    **VALID_ROLE_TITLE_DESCRIPTION_FOUR, "resourceAccessLevels": ''
}

ROLE_WITH_DUPLICATE_PERMISSIONS = {
    **VALID_ROLE_TITLE_DESCRIPTION, "resourceAccessLevels": [{
        "permissionIds": ['-LJyuBgwu7weqZKeVx_e', '-LJyuBgwu7weqZKeVx_e']
    }]
}

ROLE_WITH_DUPLICATE_RESOURCES = {
    **VALID_ROLE_TITLE_DESCRIPTION, "resourceAccessLevels": [{
        "permissionIds": ['-LJyuBgwu7weqZKeVx_e'],
        "resourceId":
            '-LJyuBgwu7weqZKeVx_e'
    },
        {
            "permissionIds":
                ['-LJyuBgwu7weqZKeVx_e'],
            "resourceId":
                '-LJyuBgwu7weqZKeVx_e'
        }]
}

VALID_ROLE_DATA_TO_MUTATE = {
    "title": "software developer",
    "description":
        "They build working applications following industry standards"
}

VALID_ROLE_DATA_THREE = {
    "title": "software developer two",
    "description":
        "They build working applications following industry standards"
}

VALID_ROLE_DATA_FOUR = {
    "title": "software developer three",
    "description":
        "They build working applications following industry standards"
}

VALID_ROLE_DATA_TO_MUTATE_TWO = {
    "title": "software engineer",
    "description":
        "They build working applications following industry standards"
}

