import itertools

import dask.dataframe as dd
import django
import numpy as np
import pandas as pd
from django.core.cache import cache
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Field
from django.db import models
from django.utils.encoding import force_str as force_text

class ReadFrameDask:
    FieldDoesNotExist = (
        django.core.exceptions.FieldDoesNotExist
        if django.VERSION < (1, 8)
        else django.core.exceptions.FieldDoesNotExist
    )

    def __init__(
            self,
            qs,
            fieldnames=(),
            index_col=None,
            coerce_float=False,
            verbose=True,
            datetime_index=False,
            column_names=None,
            chunk_size=1000,
    ):
        self.qs = qs
        self.fieldnames = pd.unique(np.array(fieldnames)) if fieldnames else ()
        self.index_col = index_col
        self.coerce_float = coerce_float
        self.verbose = verbose
        self.datetime_index = datetime_index
        self.column_names = column_names
        self.chunk_size = chunk_size

    @staticmethod
    def replace_from_choices(choices):
        def inner(values):
            return [choices.get(v, v) for v in values]

        return inner

    @staticmethod
    def get_model_name(model):
        return model._meta.model_name

    @staticmethod
    def get_related_model(field):
        model = None
        if hasattr(field, "related_model") and field.related_model:
            model = field.related_model
        elif hasattr(field, "rel") and field.rel:
            model = field.rel.to
        return model

    @classmethod
    def get_base_cache_key(cls, model):
        return (
            f"dask_{model._meta.app_label}_{cls.get_model_name(model)}_%s_rendering"
        )

    @classmethod
    def replace_pk(cls, model):
        base_cache_key = cls.get_base_cache_key(model)

        def get_cache_key_from_pk(pk):
            return None if pk is None else base_cache_key % str(pk)

        def inner(pk_series):
            pk_series = pk_series.astype(object).where(pk_series.notnull(), None)
            cache_keys = pk_series.apply(get_cache_key_from_pk, convert_dtype=False)
            unique_cache_keys = list(filter(None, cache_keys.unique()))
            if not unique_cache_keys:
                return pk_series

            out_dict = cache.get_many(unique_cache_keys)
            if len(out_dict) < len(unique_cache_keys):
                out_dict = dict(
                    [
                        (base_cache_key % obj.pk, force_text(obj))
                        for obj in model.objects.filter(
                        pk__in=list(filter(None, pk_series.unique()))
                    )
                    ]
                )
                cache.set_many(out_dict)
            return list(map(out_dict.get, cache_keys))

        return inner

    @classmethod
    def build_update_functions(cls, fieldnames, fields):
        for fieldname, field in zip(fieldnames, fields):
            if not isinstance(field, Field):
                yield fieldname, None
            else:
                if field.choices:
                    choices = dict([(k, force_text(v)) for k, v in field.flatchoices])
                    yield fieldname, cls.replace_from_choices(choices)
                elif field.get_internal_type() == "ForeignKey":
                    yield fieldname, cls.replace_pk(cls.get_related_model(field))

    @classmethod
    def update_with_verbose(cls, df, fieldnames, fields):
        for fieldname, function in cls.build_update_functions(fieldnames, fields):
            if function is not None:
                df[fieldname] = df[fieldname].map_partitions(lambda x: function(x))

    @classmethod
    def to_fields(cls, qs, fieldnames):
        """Get fields from a queryset based on the given fieldnames."""
        for fieldname in fieldnames:
            model = qs.model
            for fieldname_part in fieldname.split("__"):
                try:
                    field = model._meta.get_field(fieldname_part)
                except cls.FieldDoesNotExist:
                    try:
                        rels = model._meta.get_all_related_objects_with_model()
                    except AttributeError:
                        field = fieldname
                    else:
                        for relobj, _ in rels:
                            if relobj.get_accessor_name() == fieldname_part:
                                field = relobj.field
                                model = field.model
                                break
                else:
                    model = cls.get_related_model(field)
            yield field

    @staticmethod
    def is_values_queryset(qs):
        try:
            return qs._iterable_class == django.db.models.query.ValuesIterable
        except:
            return False

    @staticmethod
    def object_to_dict(obj, fields=None):
        """Convert a Django model instance to a dictionary based on specified fields."""
        if obj is None:
            return {}  # Return an empty dictionary if obj is None
        if not fields:
            obj.__dict__.pop("_state", None)  # Remove _state safely
            return obj.__dict__
        return {field: obj.__dict__.get(field) for field in fields if field is not None}

    @staticmethod
    def infer_dtypes_from_django(qs):
        """Infers Dask data types based on Django queryset model fields, with support for nullable integers."""
        django_to_dask_dtype = {
            'AutoField': 'Int64',  # Use nullable integer
            'BigAutoField': 'Int64',
            'BigIntegerField': 'Int64',
            'BooleanField': 'bool',
            'CharField': 'object',
            'DateField': 'datetime64[ns]',
            'DateTimeField': 'datetime64[ns]',
            'DecimalField': 'float64',
            'FloatField': 'float64',
            'IntegerField': 'Int64',  # Use nullable integer
            'PositiveIntegerField': 'Int64',
            'SmallIntegerField': 'Int64',
            'TextField': 'object',
            'TimeField': 'object',
            'UUIDField': 'object',
            'ForeignKey': 'Int64',  # Use nullable integer for FK fields
        }

        dtypes = {}
        # Handle model fields
        for field in qs.model._meta.get_fields():
            # Skip reverse relationships and non-concrete fields
            if not getattr(field, 'concrete', False):
                continue

            # Check for AutoField or BigAutoField explicitly
            if isinstance(field, (models.AutoField, models.BigAutoField)):
                dtypes[field.name] = 'Int64'  # Nullable integer for autoincremented fields
            else:
                # Use field type to infer dtype
                field_type = field.get_internal_type()
                dtypes[field.name] = django_to_dask_dtype.get(field_type, 'object')

        # Handle annotated fields
        for annotation_name, annotation in qs.query.annotation_select.items():
            if hasattr(annotation, 'output_field'):
                field_type = annotation.output_field.get_internal_type()
                dtype = django_to_dask_dtype.get(field_type, 'object')
            else:
                dtype = 'object'  # Default to object for untyped annotations
            dtypes[annotation_name] = dtype

        return dtypes

    def read_frame(self, fillna_value=None):
        qs = self.qs
        fieldnames = tuple(self.fieldnames)
        index_col = self.index_col
        coerce_float = self.coerce_float
        verbose = self.verbose
        datetime_index = self.datetime_index
        column_names = self.column_names
        chunk_size = self.chunk_size

        if fieldnames:
            fields = self.to_fields(qs, fieldnames)

        elif self.is_values_queryset(qs):
            annotation_field_names = list(qs.query.annotation_select)
            extra_field_names = list(qs.query.extra_select)
            select_field_names = list(qs.query.values_select)

            fieldnames = select_field_names + annotation_field_names + extra_field_names
            fields = [
                         None if "__" in f else qs.model._meta.get_field(f)
                         for f in select_field_names
                     ] + [None] * (len(annotation_field_names) + len(extra_field_names))

            uniq_fields = set()
            fieldnames, fields = zip(
                *(
                    f
                    for f in zip(fieldnames, fields)
                    if f[0] not in uniq_fields and not uniq_fields.add(f[0])
                )
            )
        else:
            fields = qs.model._meta.fields
            fieldnames = [f.name for f in fields]
            fieldnames += list(qs.query.annotation_select.keys())

        # Infer dtypes from Django fields
        dtypes = self.infer_dtypes_from_django(qs)
        if fieldnames:
            dtypes = {field: dtype for field, dtype in dtypes.items() if field in fieldnames}

        # Create partitions for Dask by iterating through chunks
        partitions = []
        iterator = iter(qs.iterator(chunk_size=chunk_size))

        while True:
            chunk = list(itertools.islice(iterator, chunk_size))
            #chunk = list(next(iterator, None) for _ in range(chunk_size))
            # Check if the chunk is empty or contains only None values
            #chunk = [obj for obj in chunk if obj is not None]
            if not chunk:
                break

            # Convert chunk to DataFrame with inferred dtypes
            df = pd.DataFrame.from_records(
                [self.object_to_dict(obj, fieldnames) for obj in chunk],
                columns=fieldnames,
                coerce_float=coerce_float,
            )
            # Handle NaN values before casting, if specified
            if fillna_value is not None:
                df = df.fillna(fillna_value)

            # Convert timezone-aware columns to timezone-naive if needed
            for col in df.columns:
                if isinstance(df[col].dtype, pd.DatetimeTZDtype):
                    df[col] = df[col].dt.tz_localize(None)

            # Convert to the appropriate data types
            df = df.astype(dtypes)
            partitions.append(dd.from_pandas(df, npartitions=1))

        # Concatenate partitions into a single Dask DataFrame
        # Ensure all partitions have the same columns

        dask_df = dd.concat(partitions, axis=0, ignore_index=True)

        if verbose:
            self.update_with_verbose(dask_df, fieldnames, fields)

        if index_col is not None and index_col in dask_df.columns:
            dask_df = dask_df.set_index(index_col)

        if datetime_index and index_col in dask_df.columns:
            def safe_to_datetime(index):
                """Safely convert the index to datetime, preserving non-datetime values."""
                try:
                    return pd.to_datetime(index)
                except Exception:
                    return index  # If conversion fails, return the original index

            dask_df = dask_df.map_partitions(lambda x: x.set_index(safe_to_datetime(x.index)))
        # Handle column renaming
        if column_names is not None:
            # Ensure fieldnames and column_names align
            if len(fieldnames) != len(column_names):
                raise ValueError(
                    f"Length mismatch: fieldnames ({len(fieldnames)}) and column_names ({len(column_names)}) must have the same length."
                )

            # Create rename mapping
            rename_mapping = {str(k): v for k, v in zip(fieldnames, column_names)}

            # Apply renaming using map_partitions and Pandas' rename
            def rename_columns(df, mapping):
                return df.rename(columns=mapping)

            dask_df = dask_df.map_partitions(rename_columns, mapping=rename_mapping)
        return dask_df
