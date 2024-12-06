import asyncio
import datetime
from typing import Any, Dict, Type, TypeVar
from typing import Union, Optional

import dask.dataframe as dd
import pandas as pd
from pydantic import BaseModel

from sibi_dst.df_helper.core import ParquetSaver
from sibi_dst.df_helper.core import QueryConfig, ParamsConfig
from sibi_dst.utils import Logger
from .plugins.django import *
from .plugins.http import HttpConfig
from .plugins.parquet import ParquetConfig
from django.db import models

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')

# Define a generic type variable for BaseModel subclasses
T = TypeVar("T", bound=BaseModel)

class DfHelper:
    df: Union[dd.DataFrame, pd.DataFrame] = None
    plugin_db_connection: Optional[DjangoConnectionConfig] = None
    plugin_query: Optional[QueryConfig] = None
    plugin_params: Optional[ParamsConfig] = None
    plugin_parquet: Optional[ParquetConfig] = None
    plugin_http: Optional[HttpConfig] = None
    parquet_filename: str = None
    logger: Logger
    default_config: Dict = None

    def __init__(self, source='django_db', **kwargs):
        # Ensure default_config is not shared across instances
        self.default_config = self.default_config or {}
        kwargs = {**self.default_config.copy(), **kwargs}
        self.source = source
        self.logger = logger
        self.debug = kwargs.setdefault("debug", False)
        self.verbose_debug = kwargs.setdefault("verbose_debug", False)
        self.parquet_storage_path = kwargs.setdefault("parquet_storage_path", None)
        self.dt_field=kwargs.setdefault("dt_field", None)
        kwargs.setdefault("live", True)
        self.post_init(**kwargs)

    def post_init(self, **kwargs):
        self.plugin_query = self.__get_config(QueryConfig, kwargs)
        self.plugin_params = self.__get_config(ParamsConfig, kwargs)
        if self.source == 'django_db':
            self.plugin_db_connection = self.__get_config(DjangoConnectionConfig, kwargs)
        elif self.source == 'parquet':
            self.parquet_filename = kwargs.setdefault("parquet_filename", None)
            self.plugin_parquet = ParquetConfig(**kwargs)
        elif self.source == 'http':
            self.plugin_http = HttpConfig(**kwargs)

    @staticmethod
    def __get_config(model: Type[T], kwargs: Dict[str, Any]) -> BaseModel:
        """
        Initializes a Pydantic model with the keys it recognizes from the kwargs,
        and removes those keys from the kwargs dictionary.
        :param model: The Pydantic model class to initialize.
        :param kwargs: The dictionary of keyword arguments.
        :return: The initialized Pydantic model instance.
        """
        # print(kwargs)
        # Extract keys that the model can accept
        recognized_keys = set(model.__annotations__.keys())
        # print(recognized_keys)
        model_kwargs = {k: kwargs.pop(k) for k in list(kwargs.keys()) if k in recognized_keys}
        return model(**model_kwargs)

    def load(self, **options):
        # this will be the universal method to load data from a df irrespective of the source
        return self._load(**options)

    def _load(self, **options):

        if self.source == 'django_db':
            return self._load_from_db(**options)
        elif self.source == 'parquet':
            return self._load_from_parquet(**options)
        elif self.source == 'http':
            if asyncio.get_event_loop().is_running():
                return self._load_from_http(**options)
            else:
                return asyncio.run(self._load_from_http(**options))


    def _load_from_db(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        try:
            db_loader = DjangoLoadFromDb(
                self.plugin_db_connection,
                self.plugin_query,
                self.plugin_params,
                self.logger,
                **options
            )
            self.df = db_loader.build_and_load()
            self.logger.info("Data successfully loaded from django database.")
        except Exception as e:
            self.logger.error(f"Failed to load data from django database: {e}")
            self.df=dd.from_pandas(pd.DataFrame(), npartitions=1)

        return self.df

    async def _load_from_http(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        """Delegate asynchronous HTTP data loading to HttpDataSource plugin."""
        if self.plugin_http:
            self.df = await self.plugin_http.fetch_data(**options)
        else:
            self.logger.error("HTTP plugin not configured properly.")
            self.df=dd.from_pandas(pd.DataFrame(), npartitions=1)
        return self.df

    def save_to_parquet(self, parquet_filename: Optional[str] = None):
        ps = ParquetSaver(self.df, self.parquet_storage_path, self.logger)
        ps.save_to_parquet(parquet_filename)

    def _load_from_parquet(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        self.df = self.plugin_parquet.load_files()
        if options:
            self.df = self.plugin_query.apply_filters_dask(self.df, options)
        return self.df

    def load_period(self, **kwargs):
        return self.__load_period(**kwargs)

    def __load_period(self, **kwargs):
        dt_field = kwargs.pop("dt_field", self.dt_field)
        if dt_field is None:
            raise ValueError('dt_field must be provided')
        start = kwargs.pop('start', None)
        end = kwargs.pop('end', None)

        if isinstance(start, str):
            start = self.parse_date(start)
        if isinstance(end, str):
            end = self.parse_date(end)

        if self.source == 'django_db':
            model_fields = {field.name: field for field in self.plugin_db_connection.model._meta.get_fields()}
            field_type = model_fields.get(dt_field, None)

            if field_type is None:
                raise ValueError(f"Field '{dt_field}' does not exist in the model.")

            # Determine the field type
            is_date_field = isinstance(field_type, models.DateField)
            is_datetime_field = isinstance(field_type, models.DateTimeField)

            if is_date_field:
                if start is not None:
                    kwargs[f"{dt_field}__gte"] = start
                if end is not None:
                    kwargs[f"{dt_field}__lte"] = end
            elif is_datetime_field:
                if isinstance(start, datetime.date) and not isinstance(start, datetime.datetime):
                    kwargs[f"{dt_field}__gte"] = start
                elif start is not None:
                    kwargs[f"{dt_field}__date__gte"] = start

                if isinstance(end, datetime.date) and not isinstance(end, datetime.datetime):
                    kwargs[f"{dt_field}__lte"] = end
                elif end is not None:
                    kwargs[f"{dt_field}__date__lte"] = end

            return self.load(**kwargs)

    @staticmethod
    def parse_date(date_str: str) -> Union[datetime.datetime, datetime.date]:
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    @staticmethod
    def parse_parquet_period(**kwargs):
        period = kwargs.pop('period', 'today')

        def get_today():
            return datetime.datetime.today().strftime('%Y-%m-%d')

        def get_yesterday():
            return (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        def get_current_week():
            start, end = calc_week_range(datetime.datetime.today())
            return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

        def get_last_week():
            start, end = calc_week_range(datetime.datetime.today() - datetime.timedelta(days=7))
            return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

        def get_current_month():
            return datetime.datetime.today().replace(day=1).strftime('%Y-%m-%d'), datetime.datetime.today().strftime(
                '%Y-%m-%d')

        def get_current_year():
            year = datetime.datetime.today().year
            start, end = get_year_timerange(year)
            return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

        def get_current_quarter():
            return get_first_day_of_the_quarter(datetime.datetime.today()).strftime(
                '%Y-%m-%d'), get_last_day_of_the_quarter(datetime.datetime.today()).strftime('%Y-%m-%d')

        period_functions = {
            'today': lambda: (get_today(), get_today()),
            'yesterday': lambda: (get_yesterday(), get_yesterday()),
            'current_week': get_current_week,
            'last_week': get_last_week,
            'current_month': get_current_month,
            'current_year': get_current_year,
            'current_quarter': get_current_quarter,
        }
        start_date, end_date = period_functions.get(period, period_functions['today'])()
        return {
            'parquet_start_date': start_date,
            'parquet_end_date': end_date
        }