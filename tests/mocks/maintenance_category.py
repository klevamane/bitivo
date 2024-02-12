""" Mock maintenance category data """

MAINTENANCE_CATEGORY = {
    "title": "hjk",
    "assetCategoryId": '_dfg',
    "centerId": '_LTif'
}
"""Module for maintenance category mock data"""

VALID_MAINTENANCE_CATEGORY_DATA = {
    "title": "Ac repairs",
    "centerId": "-LSkH67q4Jx6BfIWeTYT",
    "assetCategoryId": "-LSkH6iyQFboAFf65dvt",
    "assigneeId": "-LSkH6DChFpXq7TeTi",
}

DUPLICATE_MAINTENANCE_CATEGORY_DATA = {
    "title": "Servicing",
    "centerId": "-LSkH67q4Jx6BfIWeTYT",
    "assetCategoryId": "-LSkH6iyQFboAFf65dvt",
    "assigneeId": "-LSkH6DChFpXq7TeTi",
}

MAINTENANCE_CATEGORY_WITH_EMPTY_FIELDS = {
    "title": "",
    "centerId": "",
    "assetCategoryId": "",
}

MAINTENANCE_CATEGORY_WITH_MISSING_FIELDS = {"title": "Servicing"}

MAINTENANCE_CATEGORY_WITH_EMPTY_FIELDS = {
    "title": "",
    "centerId": "",
    "assetCategoryId": "",
}

MAINTENANCE_CATEGORY_WITH_MISSING_FIELDS = {"title": "Servicing"}

VALID_UPDATE_MAINTENANCE_CATEGORY_DATA = {
    "title": "Maintain this categor",
    "centerId": "-LZ-vOjGsTFvcOGRFkrM",
    "assetCategoryId": "-LZ-vOjTvlK04JNWtzn_"
}

VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA = {
    "title":
    "Maintain this category",
    "centerId":
    "-LZ-vOjGsTFvcOGRFkrM",
    "assetCategoryId":
    "-LZ-vOjTvlK04JNWtzn_",
    "workOrders": [{
        "title": "this is a title again and again t",
        "description": "this is a description",
        "status": "enabled",
        "startDate": "2019-1-14 21:00:00",
        "endDate": "2019-2-14 21:00:00",
        "assigneeId": "-LS-5BTjYWkL7Alp-ujV",
        "frequency": "daily",
        "customOccurence": {
            "repeat_days": ["Monday", "Tuesday"],
            "repeat_units": 2,
            "repeat_frequency": "weekly",
            "ends": {
                "after": 3
            }
        }
    }]
}

VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDERS_DATA = {
    "title":
    "Andela Laptops",
    "centerId":
    "-LZ-vOjGsTFvcOGRFkrM",
    "assetCategoryId":
    "-LZ-vOjTvlK04JNWtzn_",
    "workOrders": [{
        "title": "test title",
        "description": "this is a description",
        "workOrderId": "",
        "status": "enabled",
        "centerId": "-LZ-vOjGsTFvcOGRFkrM",
        "startDate": "2019-1-14 21:00:00",
        "endDate": "2019-2-14 21:00:00",
        "assigneeId": "-LS-5BTjYWkL7Alp-ujV",
        "frequency": "daily",
        "customOccurence": {
            "repeat_days": ["Monday", "Tuesday"],
            "repeat_units": 2,
            "repeat_frequency": "weekly",
            "ends": {
                "on": "2019-02-14"
            }
        }
    },
                   {
                       "title": "maintain monitors",
                       "description": "this is a description",
                       "centerId": "-LZ-vOjGsTFvcOGRFkrM",
                       "startDate": "2019-1-14 21:00:00",
                       "endDate": "2019-2-14 21:00:00",
                       "status": "enabled",
                       "assigneeId": "-LS-5BTjYWkL7Alp-ujV",
                       "frequency": "daily",
                       "customOccurence": {
                           "repeat_days": ["Monday", "Tuesday"],
                           "repeat_units": 2,
                           "repeat_frequency": "weekly",
                           "ends": {
                               "after": 3,
                               "on": "2019-02-14",
                               "never": 'True'
                           }
                       }
                   }]
}

VAlID_WORK_ORDER_DATA = [{
    "title": "test",
    "description": "new description fjvn",
    "workOrderid": "",
    "status": "enabled",
    "startDate": "2019-2-14 21:00:00",
    "endDate": "2019-3-14 21:00:00",
    "assigneeId": "-LS-5BTjYWkL7Alp-ujV",
    "frequency": "daily",
    "customOccurence": {
        "repeat_days": ["Monday", "Tuesday"],
        "repeat_units": 2,
        "repeat_frequency": "weekly",
        "ends": {
            "never": "true"
        }
    }
},
                         {
                             "title": "test",
                             "description": "new description fjvn",
                             "status": "enabled",
                             "startDate": "2019-2-14 13:00:00",
                             "endDate": "2019-3-14 15:00:00",
                             "assigneeId": "-LS-5BTjYWkL7Alp-ujV",
                             "frequency": "daily",
                             "customOccurence": {
                                 "repeat_days": ["Monday", "Tuesday"],
                                 "repeat_units": 2,
                                 "repeat_frequency": "weekly",
                                 "ends": {
                                     "on": "2019-02-14"
                                 }
                             }
                         }]

VALID_MAINTENANCE_CATEGORY_DATA_WITH_WORK_ORDER = {
    "title":
    "repairs",
    "centerId":
    "-LSkH67q4Jx6BfIWeTYT",
    "assetCategoryId":
    "-LSkH6iyQFboAFf65dvt",
    "assigneeId":
    "-LSkH6DChFpXq7TeTi",
    "workOrders": [{
        "title": "work order 1",
        "description": "description of work order",
        "assigneeId": "-LTY8T0N1_9gwLINyKuY",
        "status": 'enabled',
        "frequency": "custom",
        "startDate": "2019-01-9 21:00:00",
        "endDate": "2019-02-11 21:00:00",
        "customOccurrence": {
            "repeat_days": ["Monday", "Tuesday"],
            "repeat_units": 1,
            "repeat_frequency": "weekly",
            "ends": {
                "never": 'True',
            }
        }
    }]
}

VALID_MAINTENANCE_CATEGORY_AND_WORK_ORDER_DATA_WITH_INVALID_ENDS_FIELD = {
    "title":
    "repairs",
    "centerId":
    "-LSkH67q4Jx6BfIWeTYT",
    "assetCategoryId":
    "-LSkH6iyQFboAFf65dvt",
    "assigneeId":
    "-LSkH6DChFpXq7TeTi",
    "workOrders": [{
        "title": "work order 1",
        "description": "description of work order",
        "assigneeId": "-LTY8T0N1_9gwLINyKuY",
        "status": 'enabled',
        "frequency": "custom",
        "startDate": "2019-03-11 13:00:00",
        "endDate": "2019-05-11 15:00:00",
        "customOccurrence": {
            "repeat_days": ["Monday", "Tuesday"],
            "repeat_units": 1,
            "repeat_frequency": "weekly",
            "ends": {
                "never": True,
                "after": 5,
                "on": "2019-05-25"
            },
        }
    }]
}
