import json
from typing import Dict

import pandas as pd
from django.db.models import Q
import dask.dataframe as dd
from datetime import datetime

from sibi_dst.df_helper.plugins.django import ReadFrameDask

conversion_map: Dict[str, callable] = {
    "CharField": lambda x: x.astype(str),
    "TextField": lambda x: x.astype(str),
    "IntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "AutoField": lambda x: pd.to_numeric(x, errors="coerce"),
    "BigIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "SmallIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "PositiveIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "PositiveSmallIntegerField": lambda x: pd.to_numeric(x, errors="coerce"),
    "FloatField": lambda x: pd.to_numeric(x, errors="coerce"),
    "DecimalField": lambda x: pd.to_numeric(x, errors="coerce"),
    "BooleanField": lambda x: x.astype(bool),
    "NullBooleanField": lambda x: x.astype(bool),
    "DateTimeField": lambda x: pd.to_datetime(x, errors="coerce"),
    "DateField": lambda x: pd.to_datetime(x, errors="coerce").dt.date,
    "TimeField": lambda x: pd.to_datetime(x, errors="coerce").dt.time,
    "DurationField": lambda x: pd.to_timedelta(x, errors="coerce"),
    # for JSONField, assuming JSON objects are represented as string in df
    "JSONField": lambda x: x.apply(json.loads),
    "ArrayField": lambda x: x.apply(eval),
    "UUIDField": lambda x: x.astype(str),
}


class DjangoLoadFromDb:
    df: pd.DataFrame
    def __init__(self, db_connection, db_query, db_params, logger, **kwargs):
        self.connection_config = db_connection
        self.debug = kwargs.pop('debug', False)
        self.verbose_debug = kwargs.pop('verbose_debug', False)
        self.logger = logger
        if self.connection_config.model is None:
            if self.debug:
                self.logger.critical('Model must be specified')
                if self.verbose_debug:
                    print('Model must be specified')
            raise ValueError('Model must be specified')

        self.query_config = db_query
        self.params_config = db_params
        self.params_config.parse_params(kwargs)


    def build_and_load(self):
        self.df=self._build_and_load()
        if self.df is not None:
            self._process_loaded_data()
        return self.df

    def _build_and_load(self)->pd.DataFrame:
        query = self.connection_config.model.objects.using(self.connection_config.connection_name)
        try:
            if not self.params_config.filters:
                # IMPORTANT: if no filters are provided show only the first n_records
                # this is to prevent loading the entire table by mistake
                queryset = query.all()[:self.query_config.n_records]
            else:
                q_objects = self.__build_query_objects(self.params_config.filters, self.query_config.use_exclude)
                queryset = query.filter(q_objects)
            if queryset is not None:
                self.df=ReadFrameDask(queryset, **self.params_config.df_params).read_frame()
        except Exception as e:
            print(e)
            self.df=dd.from_pandas(pd.DataFrame(), npartitions=1)
        return self.df

    @staticmethod
    def __build_query_objects(filters: dict, use_exclude: bool):
        q_objects = Q()
        for key, value in filters.items():
            if not use_exclude:
                q_objects.add(Q(**{key: value}), Q.AND)
            else:
                q_objects.add(~Q(**{key: value}), Q.AND)
        return q_objects

    def _process_loaded_data(self):
        field_map = self.params_config.field_map
        if field_map is not None:
            rename_mapping = {k: v for k, v in field_map.items() if k in self.df.columns}
            if rename_mapping:
                # Apply renaming
                self.df = self.df.rename(columns=rename_mapping)