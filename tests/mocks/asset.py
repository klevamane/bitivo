"""
A set of mock asset data for testing asset creation
"""
ASSET_TWO = {"tag": "Fred Macbook", "customAttributes": {}}
ASSET_THREE = {"tag": "King Macbook"}
ASSET_FOUR = {
    "tag": "Kingg Macbook",
    "custom_attributes": {
        "waranty": "10 yr"
    }
}
ASSET_FIVE = {"tag": "Kinngg Macbook"}

ASSET_NO_CUSTOM_ATTRS = {"tag": "Fred's Macbook"}

ASSET_NO_CUSTOM_ATTRS_TWO = {"tag": "Johns's Macbook"}

ASSET_NO_CUSTOM_ATTRS_THREE = {"tag": "Jane's Macbook"}

ASSET_EMPTY_CUSTOM_ATTRS = {"tag": "Fred's Macbook", "customAttributes": {}}

ASSET_NO_TAG = {"tag": ""}

ASSET_NONEXISTENT_CATEGORY = {
    "tag": "Fred's Macbook",
    "assetCategoryId": "-LEiS7lgOu3VmeEBg5cUtt"
}

ASSET_INVALID_CATEGORY_ID = {
    "tag": "Fred's Macbook",
    "assetCategoryId": "-%LEiS7lgOu3VmeEBg5cU"
}

ASSET_VALID_CUSTOM_ATTRS = {
    'tag': 'abcd1234',
    'custom_attributes': {
        'waranty': '9876A',
        'length': '12cm',
        'screen size': 'Red'
    }
}

ASSET_DATA_EDITS = {'tag': 'EditedTag123'}

UNRECONCILED_ASSETS = [{
    'id': '-LY7oCLuQGQvBKJHfovO',
    'name': 'Laptop',
    'stockCount': {
        'expectedBalance': 0,
        'actualBalance': {
            'date': '2019-02-07 16:35:56.350371',
            'count': 10
        },
        'difference': 10
    }
}]
GET_ALL_STATUS = {
    'ok-in use', 'inventory', 'available', 'ok-in store', 'fairly used', 'ok',
    'in - use', 'stolen', 'lost', 'assigned', 'in repairs', 'with it',
    'faulty', 'disposed with approval', 'faulty-in store'
}

GET_OK_STATUS = ('assigned', 'available', 'ok', 'ok-in store', 'ok-in use')

GET_RECONCILIATION_STATUS = ('available', 'ok-in store', 'inventory')
