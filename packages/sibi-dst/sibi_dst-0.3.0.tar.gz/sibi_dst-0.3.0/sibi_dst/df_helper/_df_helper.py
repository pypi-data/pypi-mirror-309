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
from .plugins.parquet import ParquetConfig, ParquetFilterHandler
from django.db import models

from .plugins.sql_alchemy import *

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')

# Define a generic type variable for BaseModel subclasses
T = TypeVar("T", bound=BaseModel)

class DfHelper:
    df: Union[dd.DataFrame, pd.DataFrame] = None
    plugin_django_connection: Optional[DjangoConnectionConfig] = None
    plugin_query: Optional[QueryConfig] = None
    plugin_params: Optional[ParamsConfig] = None
    plugin_parquet: Optional[ParquetConfig] = None
    plugin_http: Optional[HttpConfig] = None
    plugin_sqlalchemy: Optional[SqlAlchemyConnectionConfig] = None
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
            self.plugin_django_connection = self.__get_config(DjangoConnectionConfig, kwargs)
        elif self.source == 'parquet':
            self.parquet_filename = kwargs.setdefault("parquet_filename", None)
            self.plugin_parquet = ParquetConfig(**kwargs)
        elif self.source == 'http':
            self.plugin_http = HttpConfig(**kwargs)
        elif self.source == 'sqlalchemy':
            self.plugin_sqlalchemy = self.__get_config(SqlAlchemyConnectionConfig,kwargs)

    @staticmethod
    def __get_config(model: [T], kwargs: Dict[str, Any]) -> Union[T]:
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
            self.plugin_params.parse_params(options)
            return self._load_from_db(**options)
        elif self.source == 'sqlalchemy':
            self.plugin_params.parse_params(options)
            return self._load_from_sqlalchemy(**options)
        elif self.source == 'parquet':
            return self._load_from_parquet(**options)
        elif self.source == 'http':
            if asyncio.get_event_loop().is_running():
                return self._load_from_http(**options)
            else:
                return asyncio.run(self._load_from_http(**options))


    def _load_from_sqlalchemy(self, **options):
        try:
            db_loader = SqlAlchemyLoadFromDb(
                self.plugin_sqlalchemy,
                self.plugin_query,
                self.plugin_params,
                self.logger,
                **options
            )
            self.df = db_loader.build_and_load()
            self._process_loaded_data()
            #self._post_process_df()
            self.logger.info("Data successfully loaded from sqlalchemy database.")
        except Exception as e:
            self.logger.error(f"Failed to load data from sqlqlchemy database: {e}")
            self.df = dd.from_pandas(pd.DataFrame(), npartitions=1)

        return self.df

    def _load_from_db(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        try:
            db_loader = DjangoLoadFromDb(
                self.plugin_django_connection,
                self.plugin_query,
                self.plugin_params,
                self.logger,
                **options
            )
            self.df = db_loader.build_and_load()
            self._process_loaded_data()
            #self._post_process_df()
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

    def _post_process_df(self):
        print(self.df.columns)
        # Convert datetime columns to timezone-naive
        fieldnames = self.plugin_params.df_params.get("fieldnames", None)
        index_col = self.plugin_params.df_params.get("index_col", None)
        datetime_index = self.plugin_params.df_params.get("datetime_index", False)
        column_names = self.plugin_params.df_params.get("column_names", None)
        print(fieldnames, index_col, datetime_index, column_names)
        #if fieldnames:
        #    self.df = self.df[fieldnames].copy()

        #for col in self.df.columns:
        #    if isinstance(self.df[col].dtype, pd.DatetimeTZDtype):
        #        self.df[col] = self.df[col].dt.tz_localize(None)

        # Handle index column
        #if index_col and index_col in self.df.columns:
        #    self.df = self.df.set_index(self.index_col)

        # Convert index to datetime if required
        #if datetime_index and index_col in self.df.columns:
        #    self.df = self.df.map_partitions(lambda df: df.set_index(pd.to_datetime(df.index)))

        # Handle column renaming
        #if column_names and column_names in self.df.columns:
        #    rename_mapping = dict(zip(fieldnames, column_names))
        #    self.df = self.df.rename(columns=rename_mapping)

    def _process_loaded_data(self):
        if len(self.df.index) > 0:
            field_map = self.plugin_params.field_map
            if field_map is not None:
                rename_mapping = {k: v for k, v in field_map.items() if k in self.df.columns}
                if rename_mapping:
                    # Apply renaming
                    self.df = self.df.rename(columns=rename_mapping)

    def save_to_parquet(self, parquet_filename: Optional[str] = None):
        ps = ParquetSaver(self.df, self.parquet_storage_path, self.logger)
        ps.save_to_parquet(parquet_filename)

    def _load_from_parquet(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        self.df = self.plugin_parquet.load_files()
        if options:
            self.df = ParquetFilterHandler().apply_filters_dask(self.df, options)
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
            model_fields = {field.name: field for field in self.plugin_django_connection.model._meta.get_fields()}
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
