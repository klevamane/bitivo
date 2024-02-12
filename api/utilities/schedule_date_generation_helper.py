"""Module to handle generation of schedule dates for work orders created."""
import json
import datetime
from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, FR, MO, SA, SU, TH, TU, WE, rrule, MONTHLY, \
    YEARLY, WEEKLY
from dateutil import parser


class ScheduleGeneratorHelper:
    """ This is a helper to generate dates """

    def __init__(self, work_order_object):
        """ Constructor to init common data
        Args:
            work_order_object(obj): Object of inserted work order
        """
        self.start_date = work_order_object.start_date
        self.work_order_object = work_order_object
        self.end_date = ScheduleGeneratorHelper.get_end_date(self)

    def get_end_date(self):
        """ This method will try to get end date by checking though,
            workorder date, then, count, then date on json, else end of year
            Returns:
                self.end_date(datetime) : e.g. datetime(2019,2,23,4,5))
        """
        if self.work_order_object.end_date:
            return self.work_order_object.end_date
        return self.get_end_of_year()

    def mapper_for_specific_days(self):
        """ This method maps specific weekdays to dateutl objects for dates
            Returns:
                (list) of selected dates objects
                    e.g [TU, WE, SAT]
        """
        custom_occurrence = self.work_order_object.custom_occurrence
        mapper_to_date_object = {
            "Monday": MO,
            "Tuesday": TU,
            "Wednesday": WE,
            "Thursday": TH,
            "Friday": FR,
            "Saturday": SA,
            "Sunday": SU
        }
        return [
            mapper_to_date_object.get(date_obj)
            for date_obj in custom_occurrence["repeat_days"]
        ]

    @staticmethod
    def generates_dates(start_date, end_date, increment, period):
        """Will generate dates intervals and returns datetimes list
            Args:
                start_date(datetime): datetime(2019,2,23,4,5))
                end_date(datetime): datetime(2019,2,23,4,5))
                increment(int): The number of times the period should be
                incremented in
                period(string): One of the periods that the incrementation
                should be done in.(hours, days, weeks, months, years)
            Returns:
                dates(list of datetime)
            https://stackoverflow.com/questions/10688006/generate-a-
            list-of-datetimes-between-an-interval
        """
        dates = []
        nxt = start_date
        delta = relativedelta(**{period: increment})
        while nxt <= end_date:
            dates.append(nxt)
            nxt += delta
        return dates

    @staticmethod
    def get_end_of_year():
        """Method to generate end of year.
         Args:
            date (datetime): Date to get the end of year from
         Returns:
             (datetime): End of year of the given datetime or date.
         """
        return datetime.now().replace(month=12, day=31)


class GenerateCustomDates(ScheduleGeneratorHelper):
    """This class generates dates for custom fields"""

    def __init__(self, work_order_object):
        """ Init method getting
            Args:
              work_order_object(obj):Object of inserted work order
        """
        ScheduleGeneratorHelper.__init__(self, work_order_object)
        self.start_date = work_order_object.start_date
        self.custom_occurrence = {} if not self.work_order_object.custom_occurrence else \
            self.work_order_object.custom_occurrence
        self.end_date = self.get_end_date()
        self.interval = 1 if not self.custom_occurrence.get("repeat_units") \
            else self.custom_occurrence.get("repeat_units")

    def get_end_date(self):
        """This method will get the date on custom occurence json if its there
        Returns:
            end_date(datetime) End date on custom occurrence json or
            None if the date is not there
        """
        if self.custom_occurrence and self.custom_occurrence.get("ends") \
            and self.custom_occurrence.get("ends").get("on"):
            return self.custom_occurrence.get("ends").get("on")

    def generate_daily_dates(self):
        """ Generates hourly dates
            Returns:
                dates(list of datetimes): Interval datetimes
        """
        return self.calculate_dates(DAILY)

    def generate_specific_days_dates(self):
        """ Generates dates for specific days selected
            Returns:
                dates(list of datetimes): Interval datetimes
        """
        selected_dates = tuple(self.mapper_for_specific_days())
        return self.calculate_dates(DAILY, byweekday=selected_dates)

    def generate_monthly_dates(self):
        """ Generates dates for monthey occurence on certain day
            Returns:
                dates(list of datetimes): Interval datetimes
        """
        return self.calculate_dates(MONTHLY)

    def generate_yearly_dates(self):
        """ Generates dates for occurence is certain date of year
            Returns:
                dates(list of datetimes): Interval datetimes
        """
        return self.calculate_dates(YEARLY)

    def calculate_dates(self, *args, **kwargs):
        """This function is used to apply a common interval at the same time
         is used to apply type of ending
         Args
             :return(list of datetime
            )
         """
        json_date = self.get_end_date()
        end_date = None if not json_date else parser.parse(json_date)
        if end_date:
            kwargs["until"] = end_date
        elif self.custom_occurrence.get("ends") \
            and self.custom_occurrence.get("ends").get("after"):
            kwargs["count"] = self.custom_occurrence.get("ends").get("after")
        else:
            kwargs["until"] = self.get_end_of_year()

        return [
            date for date in rrule(
                *args,
                interval=self.interval,
                dtstart=self.start_date,
                **kwargs)
        ]


class GenerateDates(GenerateCustomDates):
    """
    This class will generate dates for frequency know and map the others for
    custom to inherited class
    """

    def __init__(self, work_order_object):
        GenerateCustomDates.__init__(self, work_order_object)
        self.work_order_object = work_order_object
        self.end_date = ScheduleGeneratorHelper.get_end_date(self)

    def no_repeat_dates(self):
        """ generate one time date
            Returns:
                dates(list of datetime): Interval datetime
        """
        return [self.start_date]

    def daily_dates(self):
        """ Generates daily dates
            Returns:
                dates(list of datetime): Interval datetime
        """
        return self.generates_dates(self.start_date, self.end_date, 1, "days")

    def weekly_dates(self):
        """ Generates weekly dates
            Returns:
                dates(list of datetime): Interval datetime
        """
        return list(
            rrule(WEEKLY, dtstart=self.start_date, until=self.end_date))

    def weekday_dates(self):
        """ Generates dates for weekdays
            Returns:
                dates(list of datetime): Interval datetime
        """
        return rrule(
            DAILY,
            dtstart=self.start_date,
            until=self.end_date,
            byweekday=(MO, TU, WE, TH, FR))

    def custom_dates(self):
        """ This methods maps the different types of custom occurrence
        and pass them to other methods
            Returns:
                dates(list of datetime): Interval datetime
        """
        custom_occurrence = self.work_order_object.custom_occurrence
        if custom_occurrence:
            custom_mapper = {
                "daily": self.generate_daily_dates,
                "weekly": self.generate_specific_days_dates,
                "monthly": self.generate_monthly_dates,
                "yearly": self.generate_yearly_dates
            }
            customs_dates = custom_mapper.get(
                custom_occurrence["repeat_frequency"])
            customs_dates = [] if not customs_dates else customs_dates()
            return customs_dates
