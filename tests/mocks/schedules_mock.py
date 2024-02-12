"""mocks for schedules generations"""
import datetime

NO_REPEAT = [datetime.datetime(2018, 12, 12, 0, 0)]
DAILY_MOCKS = [
    datetime.datetime(2019, 2, 20, 0, 0),
    datetime.datetime(2019, 2, 21, 0, 0),
    datetime.datetime(2019, 2, 22, 0, 0),
    datetime.datetime(2019, 2, 23, 0, 0),
    datetime.datetime(2019, 2, 24, 0, 0),
    datetime.datetime(2019, 2, 25, 0, 0),
    datetime.datetime(2019, 2, 26, 0, 0),
    datetime.datetime(2019, 2, 27, 0, 0),
    datetime.datetime(2019, 2, 28, 0, 0),
    datetime.datetime(2019, 3, 1, 0, 0),
    datetime.datetime(2019, 3, 2, 0, 0),
    datetime.datetime(2019, 3, 3, 0, 0),
    datetime.datetime(2019, 3, 4, 0, 0),
    datetime.datetime(2019, 3, 5, 0, 0),
    datetime.datetime(2019, 3, 6, 0, 0),
    datetime.datetime(2019, 3, 7, 0, 0),
    datetime.datetime(2019, 3, 8, 0, 0),
    datetime.datetime(2019, 3, 9, 0, 0),
    datetime.datetime(2019, 3, 10, 0, 0),
    datetime.datetime(2019, 3, 11, 0, 0),
    datetime.datetime(2019, 3, 12, 0, 0),
    datetime.datetime(2019, 3, 13, 0, 0),
    datetime.datetime(2019, 3, 14, 0, 0),
    datetime.datetime(2019, 3, 15, 0, 0),
    datetime.datetime(2019, 3, 16, 0, 0),
    datetime.datetime(2019, 3, 17, 0, 0),
    datetime.datetime(2019, 3, 18, 0, 0),
    datetime.datetime(2019, 3, 19, 0, 0),
    datetime.datetime(2019, 3, 20, 0, 0)
]

WEEKLY_MOCKS = [
    datetime.datetime(2018, 12, 12, 0, 0),
    datetime.datetime(2018, 12, 19, 0, 0),
    datetime.datetime(2018, 12, 26, 0, 0),
    datetime.datetime(2019, 1, 2, 0, 0),
    datetime.datetime(2019, 1, 9, 0, 0),
    datetime.datetime(2019, 1, 16, 0, 0),
    datetime.datetime(2019, 1, 23, 0, 0),
    datetime.datetime(2019, 1, 30, 0, 0)
]

WEEKDAY_MOCKS = [
    datetime.datetime(2019, 2, 25, 0, 0),
    datetime.datetime(2019, 2, 26, 0, 0),
    datetime.datetime(2019, 2, 27, 0, 0),
    datetime.datetime(2019, 2, 28, 0, 0),
    datetime.datetime(2019, 3, 1, 0, 0),
    datetime.datetime(2019, 3, 4, 0, 0),
    datetime.datetime(2019, 3, 5, 0, 0),
    datetime.datetime(2019, 3, 6, 0, 0),
    datetime.datetime(2019, 3, 7, 0, 0),
    datetime.datetime(2019, 3, 8, 0, 0),
    datetime.datetime(2019, 3, 11, 0, 0),
    datetime.datetime(2019, 3, 12, 0, 0),
    datetime.datetime(2019, 3, 13, 0, 0),
    datetime.datetime(2019, 3, 14, 0, 0),
    datetime.datetime(2019, 3, 15, 0, 0),
    datetime.datetime(2019, 3, 18, 0, 0),
    datetime.datetime(2019, 3, 19, 0, 0),
    datetime.datetime(2019, 3, 20, 0, 0)
]
CUSTOM_DAILY_MOCKS = [
    datetime.datetime(2019, 2, 20, 0, 0),
    datetime.datetime(2019, 2, 21, 0, 0),
    datetime.datetime(2019, 2, 22, 0, 0),
    datetime.datetime(2019, 2, 23, 0, 0),
    datetime.datetime(2019, 2, 24, 0, 0),
    datetime.datetime(2019, 2, 25, 0, 0),
    datetime.datetime(2019, 2, 26, 0, 0),
    datetime.datetime(2019, 2, 27, 0, 0),
    datetime.datetime(2019, 2, 28, 0, 0),
    datetime.datetime(2019, 3, 1, 0, 0),
    datetime.datetime(2019, 3, 2, 0, 0),
    datetime.datetime(2019, 3, 3, 0, 0),
    datetime.datetime(2019, 3, 4, 0, 0),
    datetime.datetime(2019, 3, 5, 0, 0),
    datetime.datetime(2019, 3, 6, 0, 0),
    datetime.datetime(2019, 3, 7, 0, 0),
    datetime.datetime(2019, 3, 8, 0, 0),
    datetime.datetime(2019, 3, 9, 0, 0),
    datetime.datetime(2019, 3, 10, 0, 0),
    datetime.datetime(2019, 3, 11, 0, 0),
    datetime.datetime(2019, 3, 12, 0, 0),
    datetime.datetime(2019, 3, 13, 0, 0),
    datetime.datetime(2019, 3, 14, 0, 0),
    datetime.datetime(2019, 3, 15, 0, 0),
    datetime.datetime(2019, 3, 16, 0, 0),
    datetime.datetime(2019, 3, 17, 0, 0),
    datetime.datetime(2019, 3, 18, 0, 0),
    datetime.datetime(2019, 3, 19, 0, 0),
    datetime.datetime(2019, 3, 20, 0, 0),
    datetime.datetime(2019, 3, 21, 0, 0),
    datetime.datetime(2019, 3, 22, 0, 0),
    datetime.datetime(2019, 3, 23, 0, 0),
    datetime.datetime(2019, 3, 24, 0, 0),
    datetime.datetime(2019, 3, 25, 0, 0)
]

CUSTOM_WEEKLY_MOCKS = [
    datetime.datetime(2019, 2, 21, 0, 0),
    datetime.datetime(2019, 2, 26, 0, 0),
    datetime.datetime(2019, 2, 28, 0, 0),
    datetime.datetime(2019, 3, 5, 0, 0),
    datetime.datetime(2019, 3, 7, 0, 0),
    datetime.datetime(2019, 3, 12, 0, 0),
    datetime.datetime(2019, 3, 14, 0, 0),
    datetime.datetime(2019, 3, 19, 0, 0),
    datetime.datetime(2019, 3, 21, 0, 0)
]

CUSTOM_MONTHLY_MOCKS = [
    datetime.datetime(2019, 2, 20, 0, 0),
    datetime.datetime(2019, 3, 20, 0, 0),
    datetime.datetime(2019, 4, 20, 0, 0),
    datetime.datetime(2019, 5, 20, 0, 0),
    datetime.datetime(2019, 6, 20, 0, 0),
    datetime.datetime(2019, 7, 20, 0, 0),
    datetime.datetime(2019, 8, 20, 0, 0),
    datetime.datetime(2019, 9, 20, 0, 0),
    datetime.datetime(2019, 10, 20, 0, 0),
    datetime.datetime(2019, 11, 20, 0, 0),
    datetime.datetime(2019, 12, 20, 0, 0),
    datetime.datetime(2020, 1, 20, 0, 0)
]

CUSTOM_YEARLY_MOCKS = [
    datetime.datetime(2019, 2, 20, 0, 0),
    datetime.datetime(2020, 2, 20, 0, 0),
    datetime.datetime(2021, 2, 20, 0, 0),
    datetime.datetime(2022, 2, 20, 0, 0),
    datetime.datetime(2023, 2, 20, 0, 0),
    datetime.datetime(2024, 2, 20, 0, 0),
    datetime.datetime(2025, 2, 20, 0, 0)
]

CUSTOM_WEEKLY_NEVER = [
    datetime.datetime(2019, 12, 3, 0, 0),
    datetime.datetime(2019, 12, 5, 0, 0),
    datetime.datetime(2019, 12, 10, 0, 0),
    datetime.datetime(2019, 12, 12, 0, 0),
    datetime.datetime(2019, 12, 17, 0, 0),
    datetime.datetime(2019, 12, 19, 0, 0),
    datetime.datetime(2019, 12, 24, 0, 0),
    datetime.datetime(2019, 12, 26, 0, 0),
    datetime.datetime(2019, 12, 31, 0, 0)
]

WEEKLY_NO_END_DATE = [
    datetime.datetime(2019, 9, 24, 0, 0),
    datetime.datetime(2019, 9, 26, 0, 0),
    datetime.datetime(2019, 10, 1, 0, 0),
    datetime.datetime(2019, 10, 3, 0, 0),
    datetime.datetime(2019, 10, 8, 0, 0),
    datetime.datetime(2019, 10, 10, 0, 0),
    datetime.datetime(2019, 10, 15, 0, 0),
    datetime.datetime(2019, 10, 17, 0, 0),
    datetime.datetime(2019, 10, 22, 0, 0),
    datetime.datetime(2019, 10, 24, 0, 0),
    datetime.datetime(2019, 10, 29, 0, 0),
    datetime.datetime(2019, 10, 31, 0, 0),
    datetime.datetime(2019, 11, 5, 0, 0),
    datetime.datetime(2019, 11, 7, 0, 0),
    datetime.datetime(2019, 11, 12, 0, 0),
    datetime.datetime(2019, 11, 14, 0, 0),
    datetime.datetime(2019, 11, 19, 0, 0),
    datetime.datetime(2019, 11, 21, 0, 0),
    datetime.datetime(2019, 11, 26, 0, 0),
    datetime.datetime(2019, 11, 28, 0, 0),
    datetime.datetime(2019, 12, 3, 0, 0),
    datetime.datetime(2019, 12, 5, 0, 0),
    datetime.datetime(2019, 12, 10, 0, 0),
    datetime.datetime(2019, 12, 12, 0, 0),
    datetime.datetime(2019, 12, 17, 0, 0),
    datetime.datetime(2019, 12, 19, 0, 0),
    datetime.datetime(2019, 12, 24, 0, 0),
    datetime.datetime(2019, 12, 26, 0, 0),
    datetime.datetime(2019, 12, 31, 0, 0)
]
