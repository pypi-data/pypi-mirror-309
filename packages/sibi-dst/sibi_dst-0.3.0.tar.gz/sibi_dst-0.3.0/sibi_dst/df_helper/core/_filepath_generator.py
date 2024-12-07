import datetime
import fsspec

class FilePathGenerator:
    def __init__(self, base_path=''):
        self.base_path = base_path.rstrip('/')
        self.fs = fsspec.filesystem("file") if "://" not in base_path else fsspec.filesystem(base_path.split("://")[0])

    def generate_file_paths(self, start_date, end_date):
        """
        Generate monthly directory patterns instead of individual files for Dask to read more efficiently.

        :param start_date: Start date for generating patterns.
        :param end_date: End date for generating patterns.
        :return: List of file path patterns.
        """
        start_date = self._convert_to_datetime(start_date)
        end_date = self._convert_to_datetime(end_date)

        patterns = []
        curr_date = start_date

        while curr_date <= end_date:
            year = curr_date.year
            month = str(curr_date.month).zfill(2)
            month_pattern = f"{self.base_path}/{year}/{month}/*/*.parquet"

            # Check if any files match the monthly pattern and only add if files exist
            if self.fs.glob(month_pattern):
                patterns.append(month_pattern)

            curr_date = self._increment_month(curr_date)

        return patterns

    @staticmethod
    def _convert_to_datetime(date):
        if isinstance(date, str):
            return datetime.datetime.strptime(date, '%Y-%m-%d')
        return date

    @staticmethod
    def _increment_month(curr_date):
        # Move to the first day of the next month
        if curr_date.month == 12:
            return datetime.datetime(curr_date.year + 1, 1, 1)
        else:
            return datetime.datetime(curr_date.year, curr_date.month + 1, 1)