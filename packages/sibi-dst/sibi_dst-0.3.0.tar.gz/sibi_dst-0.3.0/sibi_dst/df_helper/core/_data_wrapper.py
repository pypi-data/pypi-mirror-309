import datetime
from typing import Type, Any, Dict, Optional
import fsspec
from sibi_dst.utils import Logger
from tqdm import tqdm
from sibi_dst.df_helper.core import ParquetSaver

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')

class DataWrapper:
    DEFAULT_MAX_AGE_MINUTES = 1440
    DEFAULT_HISTORY_DAYS_THRESHOLD = 30

    def __init__(self,
                 dataclass: Type,
                 date_field: str,
                 data_path: str,
                 parquet_filename: str,
                 start_date: Any,
                 end_date: Any,
                 filesystem_type: str = "file",
                 filesystem_options: Optional[Dict] = None,
                 verbose: bool = False,
                 class_params: Optional[Dict] = None,
                 load_params: Optional[Dict] = None,
                 reverse_order: bool = False,
                 overwrite: bool = False,
                 max_age_minutes: int = DEFAULT_MAX_AGE_MINUTES,
                 history_days_threshold: int = DEFAULT_HISTORY_DAYS_THRESHOLD,
                 show_progress: bool = False):
        self.dataclass = dataclass
        self.date_field = date_field
        self.data_path = self.ensure_forward_slash(data_path)
        self.parquet_filename = parquet_filename
        self.filesystem_type = filesystem_type
        self.filesystem_options = filesystem_options or {}
        self.fs = fsspec.filesystem(filesystem_type, **self.filesystem_options)
        self.verbose = verbose
        self.class_params = class_params or {}
        self.load_params = load_params or {}
        self.reverse_order = reverse_order
        self.overwrite = overwrite
        self.max_age_minutes = max_age_minutes
        self.history_days_threshold = history_days_threshold
        self.show_progress = show_progress

        self.start_date = self.convert_to_date(start_date)
        self.end_date = self.convert_to_date(end_date)

    @staticmethod
    def convert_to_date(date: Any) -> datetime.date:
        try:
            return datetime.datetime.strptime(date, '%Y-%m-%d').date() if isinstance(date, str) else date
        except ValueError as e:
            logger.error(f"Error converting {date} to datetime: {e}")
            raise

    @staticmethod
    def ensure_forward_slash(path: str) -> str:
        return path if path.endswith('/') else path + '/'

    def generate_date_range(self):
        step = -1 if self.reverse_order else 1
        start, end = (self.end_date, self.start_date) if self.reverse_order else (self.start_date, self.end_date)
        current_date = start
        while current_date != end + datetime.timedelta(days=step):
            yield current_date
            current_date += datetime.timedelta(days=step)

    def process(self):
        date_range = list(self.generate_date_range())
        if self.show_progress:
            date_range = tqdm(date_range, desc="Processing dates", unit="date")

        for current_date in date_range:
            self.process_date(current_date)

    def is_file_older_than(self, file_path: str, current_date: datetime.date) -> bool:
        if not self.fs.exists(file_path):
            return True

        if self.overwrite:
            self.fs.rm(file_path)
            return True

        file_modification_time = self.fs.info(file_path)['mtime']
        file_modification_date = datetime.datetime.utcfromtimestamp(file_modification_time).date()
        file_age_days = (datetime.date.today() - file_modification_date).days

        if file_age_days <= self.history_days_threshold:
            file_age_seconds = (datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(file_modification_time)).total_seconds()
            if self.verbose:
                logger.info(f"File {file_path} is {round((file_age_seconds / 60), 0)} minutes old")
            return file_age_seconds / 60 > self.max_age_minutes or self.max_age_minutes == 0

        return False

    def process_date(self, date: datetime.date):
        folder = f'{self.data_path}{date.year}/{date.month:02d}/{date.day:02d}/'
        full_parquet_filename = f"{folder}{self.parquet_filename}"

        start_time = datetime.datetime.now()

        if self.verbose:
            logger.info(f"Processing {full_parquet_filename}...")

        if not self.is_file_older_than(full_parquet_filename, date):
            if self.verbose:
                logger.info("File exists and conditions for regeneration are not met. Skipping.")
            return

        data_object = self.dataclass(**self.class_params)
        date_filter_params = {
            f'{self.date_field}__year': date.year,
            f'{self.date_field}__month': date.month,
            f'{self.date_field}__day': date.day
        }
        df = data_object.load(**self.load_params, **date_filter_params)

        if len(df.index) == 0:
            if self.verbose:
                logger.info("No data found for the specified date.")
            return

        # Ensure directory structure exists
        parquet_saver = ParquetSaver(df, folder, logger)
        parquet_saver.save_to_parquet(self.parquet_filename, clear_existing=True)

        #self.fs.makedirs(folder, exist_ok=True)
        #with self.fs.open(full_parquet_filename, "wb") as f:
        #    df.to_parquet(f)

        end_time = datetime.datetime.now()
        duration_seconds = (end_time - start_time).total_seconds()

        if self.verbose:
            logger.info(f"Data saved to {full_parquet_filename}. Processing time: {duration_seconds:.2f} seconds")

    def remove_empty_directories(self, path: str):
        if not self.fs.isdir(path) or self.fs.abspath(path) == self.fs.abspath(self.data_path):
            return

        if not self.fs.ls(path):  # Check if directory is empty
            try:
                self.fs.rmdir(path)
                if self.verbose:
                    logger.info(f"Removed empty directory: {path}")
                self.remove_empty_directories(self.fs.path.dirname(path))
            except Exception as e:
                if self.verbose:
                    logger.error(f"Error removing directory {path}: {e}")
        else:
            if self.verbose:
                logger.info(f"Directory not empty, stopping: {path}")
# Usage:
# wrapper = DataWrapper(
#     dataclass=YourDataClass,
#     date_field="created_at",
#     data_path="/path/to/data",
#     parquet_filename="data.parquet",
#     start_date="2022-01-01",
#     end_date="2022-12-31",
#     filesystem_type="file",
#     verbose=True
# )
# wrapper.process()
# wrapper = DataWrapper(
#    dataclass=YourDataClass,
#    date_field="created_at",
#    data_path="s3://your-bucket-name/path/to/data",
#    parquet_filename="data.parquet",
#    start_date="2022-01-01",
#    end_date="2022-12-31",
#    filesystem_type="s3",
#    filesystem_options={
#        "key": "your_aws_access_key",
#        "secret": "your_aws_secret_key",
#        "client_kwargs": {"endpoint_url": "https://s3.amazonaws.com"}
#    },
#    verbose=True
#)
#wrapper.process()
