#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#
import json
from dataclasses import dataclass
from typing import Dict, Union, Optional

import pandas as pd

# This is the defaults configuration file for the df_helper module.

# conversion_map is a dictionary that maps the field types to their corresponding data type conversion functions.
# Each entry in the dictionary is a pair of a field type (as a string) and a callable function that performs the
# conversion. This mapping is used to convert the values in a pandas DataFrame to the appropriate data types based on
# the Django field type.

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


parquet_defaults: Dict[str, Union[bool, str, int, None]] = {
    "df_as_dask": False,
    "use_parquet": False,  # Whether to use parquet files for storing data
    "save_parquet": False,
    "load_parquet": False,
    "parquet_filename": None,
    "parquet_storage_path": None,  # Path to the folder where parquet files are stored
    "parquet_full_path": None,  # Full path to the parquet file
    "parquet_folder_list": None,  # List of folders where parquet files are stored
    "parquet_max_age_minutes": 0,  # Maximum age of the parquet file in minutes
    "parquet_size_bytes": 0,
    "parquet_is_recent": False,
    "parquet_start_date": "",
    "parquet_end_date": "",
}

connection_defaults: Dict[str, Union[str, int, None]] = {
    "live": False,
    "connection_name": None,
    "table": None,
    "model": None,
}

query_defaults: Dict[str, Union[str, int, None]] = {
    "use_exclude": False,
    "n_records": 0,
    "dt_field": None,
    "use_dask": False,
    "as_dask": False,
}

params_defaults: Dict[str, Union[str, int, None]] = {
    "field_map": {},
    "legacy_filters": False,
    "params": {},
}
