import datetime
from typing import Union, Dict, Tuple
import pandas as pd

class DateUtils:
    @classmethod
    def _ensure_date(cls, value: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Ensure the input is converted to a datetime.date object.
        """
        if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, pd.Timestamp):
            return value.to_pydatetime().date()
        elif isinstance(value, str):
            try:
                # Try parsing as datetime first, then fallback to date
                return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S').date()
            except ValueError:
                return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        else:
            raise ValueError(f"Unsupported date format: {value}")


    @classmethod
    def calc_week_range(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> Tuple[datetime.date, datetime.date]:
        """
        Calculate the start and end of the week for a given reference date.
        """
        reference_date = cls._ensure_date(reference_date)
        start = reference_date - datetime.timedelta(days=reference_date.weekday())
        end = start + datetime.timedelta(days=6)
        return start, end


    @staticmethod
    def get_year_timerange(year: int) -> Tuple[datetime.date, datetime.date]:
        """
        Get the start and end dates for a given year.
        """
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        return start, end


    @classmethod
    def get_first_day_of_the_quarter(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Get the first day of the quarter for a given date.
        """
        reference_date = cls._ensure_date(reference_date)
        quarter = (reference_date.month - 1) // 3 + 1
        return datetime.date(reference_date.year, 3 * quarter - 2, 1)


    @classmethod
    def get_last_day_of_the_quarter(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Get the last day of the quarter for a given date.
        """
        reference_date = cls._ensure_date(reference_date)
        quarter = (reference_date.month - 1) // 3 + 1
        first_day_of_next_quarter = datetime.date(reference_date.year, 3 * quarter + 1, 1)
        return first_day_of_next_quarter - datetime.timedelta(days=1)

    @classmethod
    def get_month_range(cls, n: int = 0) -> Tuple[datetime.date, datetime.date]:
        """
        Get the date range for the current month or the month `n` months in the past or future.

        :param n: The number of months to look forward (positive) or backward (negative). Defaults to 0 (current month).
        :return: A tuple containing the start and end dates of the range.
        """
        today = datetime.date.today()

        # Calculate the target month and year
        target_month = today.month + n
        target_year = today.year

        # Adjust the year and month if target_month goes out of range (1-12)
        while target_month > 12:
            target_month -= 12
            target_year += 1
        while target_month < 1:
            target_month += 12
            target_year -= 1

        # Start date is the first day of the target month
        start = datetime.date(target_year, target_month, 1)

        # End date is:
        # - Last day of the target month if n != 0
        # - Today's date if n == 0
        if n == 0:
            end = today
        else:
            next_month = target_month + 1
            next_year = target_year
            if next_month > 12:
                next_month = 1
                next_year += 1
            end = datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)

        return start, end

    @classmethod
    def parse_period(cls,**kwargs):
        """
        Parse the period keyword to determine the start and end date for date range operations.
        """
        period = kwargs.setdefault('period', 'today')

        def get_today():
            return datetime.date.today()

        def get_yesterday():
            return datetime.date.today() - datetime.timedelta(days=1)

        def get_current_week():
            start, end = cls.calc_week_range(get_today())
            return start, end

        def get_last_week():
            start, end = cls.calc_week_range(get_today() - datetime.timedelta(days=7))
            return start, end

        def get_current_month():
            today = get_today()
            start = today.replace(day=1)
            end = today
            return start, end

        def get_last_month():
            return cls.get_month_range(n=1)

        def get_current_year():
            year = get_today().year
            start, end = cls.get_year_timerange(year)
            return start, end

        def get_current_quarter():
            today = get_today()
            start = cls.get_first_day_of_the_quarter(today)
            end = cls.get_last_day_of_the_quarter(today)
            return start, end

        period_functions = {
            'today': lambda: (get_today(), get_today()),
            'yesterday': lambda: (get_yesterday(), get_yesterday()),
            'current_week': get_current_week,
            'last_week': get_last_week,
            'current_month': get_current_month,
            'last_month': get_last_month,
            'current_year': get_current_year,
            'current_quarter': get_current_quarter,
        }

        start_date, end_date = period_functions.get(period, period_functions['today'])()
        return start_date, end_date
