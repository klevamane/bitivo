"""Test module to test the due date generator class"""

from api.models import Schedule
from api.utilities.validators.schedule_creator import create_schedules, regenerate_schedules
from tests.mocks.schedules_mock import WEEKLY_MOCKS, DAILY_MOCKS, NO_REPEAT, \
    WEEKDAY_MOCKS, CUSTOM_DAILY_MOCKS, \
    CUSTOM_WEEKLY_MOCKS, CUSTOM_MONTHLY_MOCKS, CUSTOM_YEARLY_MOCKS, CUSTOM_WEEKLY_NEVER, WEEKLY_NO_END_DATE
from tests.mocks.work_order import (
    FREQUENCY_NO_REPEAT, FREQUENCY_DAILY, FREQUENCY_WEEKLY, FREQUENCY_WEEKDAY,
    FREQUENCY_CUSTOM_DAILY, FREQUENCY_CUSTOM_WEEKLY, FREQUENCY_CUSTOM_MONTHLY,
    FREQUENCY_CUSTOM_YEARLY, FREQUENCY_NO_CUSTOM_OCCURRENCE,
    FREQUENCY_WITH_COUNT)


class TestDueDateGenerator:
    """Tests for the due date generator class"""

    def test_generate_no_repeat_dates_succeeds(self,
                                               new_work_order_for_schedules):
        """ Test the generate date method for no_repeat as frequency
                Args:
                    new_work_order_for_schedules(object) work order
                    object with no_repeat
        """
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_no_repeat_schedule = [date.due_date for date in schedules]
        assert total_no_repeat_schedule == NO_REPEAT

    def test_generate_dates_daily_succeeds(self, new_work_order_for_schedules):
        """ Test the generate date method for daily as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00',
        new_work_order_for_schedules.end_date = '2019-03-20 00:00:00',
        new_work_order_for_schedules.frequency = 'daily'
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_daily_schedule = [date.due_date for date in schedules]
        assert total_daily_schedule == DAILY_MOCKS

    def test_the_generate_dates_method_with_weeks_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method with weeks as frequency
         Args:
             new_work_order_for_schedules(object) unsaved work order object
         """
        new_work_order_for_schedules.start_date = '2018-12-12 00:00:00',
        new_work_order_for_schedules.end_date = '2019-02-1 00:00:00',
        new_work_order_for_schedules.frequency = 'weekly'
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_weekly_schedule = [date.due_date for date in schedules]
        assert total_weekly_schedule == WEEKLY_MOCKS

    def test_generate_due_dates_for_weekday_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for weekday as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-25 00:00:00',
        new_work_order_for_schedules.end_date = '2019-03-20 00:00:00',
        new_work_order_for_schedules.frequency = 'weekday'
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_weekdays_schedule = [date.due_date for date in schedules]
        assert total_weekdays_schedule == WEEKDAY_MOCKS

    def test_generate_due_dates_custom_daily_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom daily as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2019-03-25"
            },
            "repeat_frequency": "daily"
        }
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_custom_daily_schedule = [date.due_date for date in schedules]
        assert total_custom_daily_schedule == CUSTOM_DAILY_MOCKS

    def test_generate_due_dates_custom_weekly_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom weekly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
         """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2019-03-25"
            },
            "repeat_frequency": "weekly"
        }
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_custom_weekly_schedule = [date.due_date for date in schedules]
        assert total_custom_weekly_schedule == CUSTOM_WEEKLY_MOCKS

    def test_generate_due_dates_custom_monthly_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom monthly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2020-01-25"
            },
            "repeat_frequency": "monthly"
        }
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_monthly_schedule = [date.due_date for date in schedules]
        assert total_monthly_schedule == CUSTOM_MONTHLY_MOCKS

    def test_generate_due_dates_custom_yearly_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom yearly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2025-03-25"
            },
            "repeat_frequency": "yearly"
        }
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule == CUSTOM_YEARLY_MOCKS

    def test_generate_due_dates_for_custom_without_custom_occurrence_fails(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom yearly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.frequency = 'custom'
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule == []

    def test_generate_due_dates_with_count_provided_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom yearly as frequency
            Args:
                new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
            },
            "repeat_frequency": 'yearly'
        }
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert len(total_yearly_schedule) == 5

    def test_generate_due_dates_without_date_and_count_succeeds(
            self, new_work_order_for_schedules):
        """ Test if its possible to generate end of year when date and count
        is not provided
            Args:
                new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-11-30 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
            },
            "repeat_frequency": "weekly"
        }
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_custom_year_schedule = [date.due_date for date in schedules]
        assert total_custom_year_schedule == CUSTOM_WEEKLY_NEVER

    def test_generate_weekly_without_end_date_succeeds(
            self, new_work_order_for_schedules):
        """ Test generate schedules without end date
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
            """
        new_work_order_for_schedules.start_date = '2019-09-20 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
            },
            "repeat_frequency": "weekly"
        }
        new_work_order_for_schedules.end_date = None
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule == WEEKLY_NO_END_DATE

    def test_generate_no_repeat_dates_succeeds(self,
                                               new_work_order_for_schedules):
        """ Test the generate date method for no_repeat as frequency
                Args:
                    new_work_order_for_schedules(object) work order
                    object with no_repeat
        """
        create_schedules(saved_work_order=new_work_order_for_schedules.save())
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_no_repeat_schedule = [date.due_date for date in schedules]
        assert total_no_repeat_schedule == NO_REPEAT

    def test_regenerate_no_repeat_dates_succeeds(self,
                                                 new_work_order_for_schedules):
        """ Test the generate date method for no_repeat as frequency
                Args:
                    new_work_order_for_schedules(object) work order
                    object with no_repeat
        """
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_NO_REPEAT)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_no_repeat_schedule = [date.due_date for date in schedules]
        assert total_no_repeat_schedule == NO_REPEAT

    def test_regenerate_dates_daily_succeeds(self,
                                             new_work_order_for_schedules):
        """ Test the generate date method for daily as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00',
        new_work_order_for_schedules.end_date = '2019-03-20 00:00:00',
        new_work_order_for_schedules.frequency = 'daily'
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_DAILY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_daily_schedule = [date.due_date for date in schedules]
        assert total_daily_schedule == DAILY_MOCKS

    def test_the_regenerate_dates_method_with_weeks_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method with weeks as frequency
         Args:
             new_work_order_for_schedules(object) unsaved work order object
         """
        new_work_order_for_schedules.start_date = '2018-12-12 00:00:00',
        new_work_order_for_schedules.end_date = '2019-02-1 00:00:00',
        new_work_order_for_schedules.frequency = 'weekly'
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_WEEKLY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_weekly_schedule = [date.due_date for date in schedules]
        assert total_weekly_schedule == WEEKLY_MOCKS

    def test_regenerate_due_dates_for_weekday_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for weekday as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-25 00:00:00',
        new_work_order_for_schedules.end_date = '2019-03-20 00:00:00',
        new_work_order_for_schedules.frequency = 'weekday'
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_WEEKDAY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_weekdays_schedule = [date.due_date for date in schedules]
        assert total_weekdays_schedule == WEEKDAY_MOCKS

    def test_regenerate_due_dates_custom_daily_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom daily as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2019-03-25"
            },
            "repeat_frequency": "daily"
        }
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_WEEKDAY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_custom_daily_schedule = [date.due_date for date in schedules]
        assert total_custom_daily_schedule == CUSTOM_DAILY_MOCKS

    def test_regenerate_due_dates_custom_weekly_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom weekly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
         """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2019-03-25"
            },
            "repeat_frequency": "weekly"
        }
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_CUSTOM_WEEKLY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_custom_weekly_schedule = [date.due_date for date in schedules]
        assert total_custom_weekly_schedule == CUSTOM_WEEKLY_MOCKS

    def test_regenerate_due_dates_custom_monthly_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom monthly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2020-01-25"
            },
            "repeat_frequency": "monthly"
        }
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_CUSTOM_MONTHLY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_monthly_schedule = [date.due_date for date in schedules]
        assert total_monthly_schedule == CUSTOM_MONTHLY_MOCKS

    def test_regenerate_due_dates_custom_yearly_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom yearly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
                "on": "2025-03-25"
            },
            "repeat_frequency": "yearly"
        }
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_CUSTOM_WEEKLY)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule == CUSTOM_YEARLY_MOCKS

    def test_regenerate_due_dates_for_custom_without_custom_occurrence_fails(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom yearly as frequency
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.frequency = 'custom'
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_NO_CUSTOM_OCCURRENCE)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule == []

    def test_regenerate_due_dates_with_count_provided_succeeds(
            self, new_work_order_for_schedules):
        """ Test the generate date method for custom yearly as frequency
            Args:
                new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
                "after": 5,
            },
            "repeat_frequency": 'yearly'
        }
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_WITH_COUNT)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert len(total_yearly_schedule) == 5

    def test_regenerate_due_dates_without_date_and_count_succeeds(
            self, new_work_order_for_schedules):
        """ Test if its possible to generate end of year when date and count
        is not provided
            Args:
                new_work_order_for_schedules(object) unsaved work order object
        """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.end_date = '2019-03-25 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
            },
            "repeat_frequency": "yearly"
        }
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_NO_CUSTOM_OCCURRENCE)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule

    def test_regenerate_weekly_without_end_date_succeeds(
            self, new_work_order_for_schedules):
        """ Test generate schedules without end date
                Args:
                    new_work_order_for_schedules(object) unsaved work order object
            """
        new_work_order_for_schedules.start_date = '2019-02-20 00:00:00'
        new_work_order_for_schedules.frequency = 'custom'
        new_work_order_for_schedules.custom_occurrence = {
            "repeat_days": ["Tuesday", "Thursday"],
            "ends": {
                "never": True,
            },
            "repeat_frequency": "yearly"
        }
        new_work_order_for_schedules.end_date = None
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_NO_CUSTOM_OCCURRENCE)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_yearly_schedule = [date.due_date for date in schedules]
        assert total_yearly_schedule

    def test_regenerate_no_repeat_dates_succeeds(self,
                                                 new_work_order_for_schedules):
        """ Test the generate date method for no_repeat as frequency
                Args:
                    new_work_order_for_schedules(object) work order
                    object with no_repeat
        """
        regenerate_schedules(
            work_order=new_work_order_for_schedules.save(),
            changed_fields=FREQUENCY_NO_CUSTOM_OCCURRENCE)
        schedules = Schedule.query.filter_by(
            work_order_id=new_work_order_for_schedules.id)
        total_no_repeat_schedule = [date.due_date for date in schedules]
        assert total_no_repeat_schedule == NO_REPEAT
