""" Module for work order mock data """
from api.utilities.enums import CustomFrequencyEnum

VALID_WORK_ORDER_DATA = {
    "title": "Engine Oil",
    "description": "The generator engine oil should be changed twice",
    "maintenanceCategoryId": "-LSkH6iyQFboAFf65dvt",
    "assigneeId": "-LSkH6DChFpXq7TeTi",
    "status": 'enabled',
    "frequency": "weekly",
}

INVALID_WORK_ORDER_DATA = {
    "assigneeId": "-LSkH6DChFpXq7TeTi",
}

VALID_WORK_ORDER = {
    "title": "work order 1",
    "description": "description of work order",
    "assigneeId": "-LTY8T0N1_9gwLINyKuY",
    "maintenanceCategoryId": "-LVhdheqE_oS663ARkBQ",
    "status": 'enabled',
    "frequency": "custom",
    "startDate": "2019-01-9 13:00:00",
    "endDate": "2019-02-11 15:30:00",
    "customOccurrence": {
        "repeat_days": ["Monday", "Tuesday"],
        "repeat_units": 1,
        "repeat_frequency": "weekly",
        "ends": {
            "on": "2019-02-11"
        }
    }
}

INVALID_WORK_ORDER_DATETIME = {
    "title": "work order 1",
    "description": "description of work order",
    "assigneeId": "-LTY8T0N1_9gwLINyKuY",
    "maintenanceCategoryId": "-LVhdheqE_oS663ARkBQ",
    "status": 'enabled',
    "frequency": "custom",
    "startDate": "2019-01-9 21:00:00",
    "endDate": "2019-02-11",
    "customOccurrence": {
        "repeat_days": ["Monday", "Tuesday"],
        "repeat_units": 1,
        "repeat_frequency": "weekly",
        "ends": {
            "after": 3
        }
    }
}

DUPLICATE_WORK_ORDER = {
    "title": 'work order 2',
    'description': 'A very long description',
    'assigneeId': "-LTY8T0N1_9gwLINyKuY",
    "maintenanceCategoryId": "-LVhdheqE_oS663ARkBQ",
    "status": 'enabled',
    'startDate': '2011-08-12 13:00:00',
    'endDate': '2019-08-12 15:30:00',
    'frequency': 'weekly',
}

WORK_ORDER_WITH_MISSING_FIELDS = {
    "title": '',
    'description': '',
    'assigneeId': '',
    "maintenanceCategoryId": '',
    "status": '',
    'startDate': '',
    'endDate': '',
    'frequency': '',
}

WORK_ORDER_SCHEMA_MESSAGES = {
    'date':
    'Invalid date time format {}. Please use a valid date time using the following format: YYYY-MM-DD HH:MM:SS',
    'repeat_days':
    'Please provide one of this Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday',
    'maintenanceCategoryId':
    "Invalid id in parameter",
    'frequency':
    'Please provide one of no_repeat, daily, weekly, weekday, custom',
    'invalid_date_time':
    "Invalid date time format {}. Please use a valid date time using the following format: YYYY-MM-DD HH:MM:SS"
}

INVALID_REPEAT_DAYS = ['shksvks', 'ckhsbvs']
VALID_REPEAT_DAYS = ["Monday", "Tuesday"]
DAYS = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
    'Sunday'
]

VALID_CUSTOMOCCURRENCE_DETAILS = {
    "repeat_days": ["Monday", "Tuesday"],
    "repeat_units": 2,
    "repeat_frequency": CustomFrequencyEnum.weekly,
    "ends": {
        "after": 3,
    }
}

INVALID_CUSTOMOCCURRENCE_DETAILS = {
    "repeat_days": [' hsfvh', 'hvjhf'],
    "repeat_units": 'fvh',
    "repeat_frequency": 'vhjfvhk',
    "ends": {
        "after": 'jfvdf',
        "on": 'hfvhkf',
        "never": 'True'
    }
}

WORK_ORDER_WITH_INVALID_CUSTOM_OCCURRENCE = {
    "title": "work order 1",
    "description": "description of work order",
    "assigneeId": "-LTY8T0N1_9gwLINyKuY",
    "maintenanceCategoryId": "-LVhdheqE_oS663ARkBQ",
    "status": 'enabled',
    "frequency": "custom",
    "startDate": "2019-01-9 21:00:00",
    "endDate": "2019-02-11 21:00:00",
    "customOccurrence": {
        "repeat_days": ["Monday", "Tuesday"],
        "repeat_units": 0,
        "repeat_frequency": "weeklysd",
        "ends": {
            "after": 0
        }
    }
}

WORK_ORDER_WITH_INVALID_REPEAT_DAYS = {
    "title": "work order 1",
    "description": "description of work order",
    "assigneeId": "-LTY8T0N1_9gwLINyKuY",
    "maintenanceCategoryId": "-LVhdheqE_oS663ARkBQ",
    "status": 'enabled',
    "frequency": "custom",
    "startDate": "2019-01-9 21:00:00",
    "endDate": "2019-02-11 21:00:00",
    "customOccurrence": {
        "repeat_days": ["Monday", "Tuesdayl"],
        "repeat_units": 1,
        "repeat_frequency": "weekly",
        "ends": {
            "never": True
        }
    }
}

VALID_WORK_ORDER_UPDATE = {
    'title': 'Update Work Order',
    'description': 'A very long description',
    'frequency': 'daily',
    'assigneeId': '',
    'startDate': '2011-08-12 21:00:00',
    'endDate': '2019-08-12 21:00:00',
    'maintenanceCategoryId': '',
}

VALID_WORK_ORDER_WITH_SAME_TITLE_UPDATE = {
    'title': '',
    'description': 'An updated description',
    'frequency': 'weekly',
    'assigneeId': '',
    'startDate': '2011-08-12 21:00:00',
    'endDate': '2019-08-12 21:00:00',
    'maintenanceCategoryId': '',
}

FREQUENCY_NO_REPEAT = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2018-12-12 21:00:00',
    'end_date': '2019-02-1 21:00:00',
    'frequency': 'no-repeat'
}

FREQUENCY_DAILY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 21:00:00',
    'end_date': '2019-03-20 21:00:00',
    'frequency': 'daily'
}

FREQUENCY_WEEKLY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2018-12-12 21:00:00',
    'end_date': '2019-02-1 21:00:00',
    'frequency': 'weekly'
}

FREQUENCY_WEEKDAY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-25 00:00:00',
    'end_date': '2019-03-20 00:00:00',
    'frequency': 'weekday'
}

FREQUENCY_CUSTOM_DAILY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 00:00:00',
    'end_date': '2019-03-25 00:00:00',
    'frequency': 'custom',
    "custom_occurrence": {
        "repeat_days": ["Tuesday"],
        "ends": {
            "never": True
        },
        "repeat_frequency": "daily"
    }
}

FREQUENCY_CUSTOM_WEEKLY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 00:00:00',
    'end_date': '2019-03-25 00:00:00',
    'frequency': 'custom',
    "custom_occurrence": {
        "repeat_days": ["Tuesday", "Thursday"],
        "ends": {
            "never": True
        },
        "repeat_frequency": "weekly"
    }
}

FREQUENCY_CUSTOM_MONTHLY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 00:00:00',
    'end_date': '2019-03-25 00:00:00',
    'frequency': 'custom',
    "custom_occurrence": {
        "repeat_days": ["Tuesday", "Thursday"],
        "ends": {
            "on": "2019-03-25 21:00:00"
        },
        "repeat_frequency": "monthly"
    }
}

FREQUENCY_CUSTOM_YEARLY = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 00:00:00',
    'end_date': '2019-03-25 00:00:00',
    'frequency': 'custom',
    "custom_occurrence": {
        "repeat_days": ["Tuesday", "Thursday"],
        "ends": {
            "on": "2019-03-25 21:00:00"
        },
        "repeat_frequency": "yearly"
    }
}

FREQUENCY_NO_CUSTOM_OCCURRENCE = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 00:00:00',
    'end_date': '2019-03-25 00:00:00',
    'frequency': 'custom',
    "custom_occurrence": {
        "repeat_days": ["Tuesday", "Thursday"],
        "ends": {
            "never": True,
        },
        "repeat_frequency": "weekly"
    }
}

FREQUENCY_WITH_COUNT = {
    'title': 'Fuel Level',
    'description': 'change the fuel of the car',
    'maintenance_category_id': '',
    'assignee_id': '',
    'start_date': '2019-02-20 00:00:00',
    'end_date': '2019-03-25 00:00:00',
    'frequency': 'custom',
    "custom_occurrence": {
        "repeat_days": ["Tuesday", "Thursday"],
        "ends": {
            "after": 5,
        },
        "repeat_frequency": 'yearly'
    }
}
