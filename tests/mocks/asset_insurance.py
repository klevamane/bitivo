""" Mock data used when testing asset insurance"""

INVALID_ASSET_INSURANCE = {
    'startDate': '2019-01-01',
    'endDate': '2019-12-31',
    'assetId': '!@#$%^&*()'
}

UPDATE_ASSET_INSURANCE_POLICY = {
    "company": "Asus insurance",
    "startDate": "2019-03-01",
    "endDate": "2019-12-31",
}

UPDATE_ASSET_INSURANCE_POLICY_WITH_INVALID_START_DATE = {
    "company": "Asus insurance",
    "startDate": "03-01-2019",
    "endDate": "2019-12-31",
}

UPDATE_ASSET_INSURANCE_POLICY_WITH_INVALID_END_DATE = {
    "company": "Asus insurance",
    "startDate": "2019-03-01",
    "endDate": "31-12-2019",
}

UPDATE_ASSET_INSURANCE_POLICY_WITH_COMPANY_ONLY = {
    "company": "Asus insurance"
}

UPDATE_ASSET_INSURANCE_POLICY_WITH_START_DATE_PAST_END_DATE = {
    "company": "Asus insurance",
    "startDate": "2020-03-01",
    "endDate": "2019-03-01",
}

VALID_ASSET_INSURANCE = {
    "company": "Leadway Insurance",
    "startDate": "2018-08-12",
    "endDate": "2020-08-12"
}

INSURANCE_WRONG_DATE_FORMAT = {
    "comapny": "Leadway Insurance",
    "startDate": "201-08-12",
    "endDate": "2019-08-12"
}

INSURANCE_INVALID_DATE_RANGE = {
    "comapny": "Leadway Insurance",
    "startDate": "2020-08-12",
    "endDate": "2019-08-12"
}
