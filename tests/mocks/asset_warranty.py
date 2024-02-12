""" Mock data used when testing asset note"""

INVALID_ASSET_WARRANTY = {
    "start_date": "!@#$%^&*()&^%$#%^&*(&^%^&",
    "end_date": "!@#$%^&*()&^%$#%^&*(&^%^&",
    "status": "Yupssy"
}

VALID_ASSET_WARRANTY_PACKAGE = {
    "startDate": "2011-08-12",
    "endDate": "2019-08-12"
}

WARRANTY_WRONG_DATE_FORMAT = {
    "startDate": "201-08-12",
    "endDate": "2019-08-12"
}

WARRANTY_INVALID_DATE_RANGE = {
    "startDate": "2020-08-12",
    "endDate": "2019-08-12"
}
