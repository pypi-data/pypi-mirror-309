import dask.dataframe as dd
from sqlmodel import Session, select
from typing import Any, Dict, Optional
import logging
import pandas as pd

from ._io_sqlalchemy_dask import ReadFrameSqlAlchemy
from ._sqlalchemy_db_connection import SqlAlchemyConnectionConfig
from sibi_dst.df_helper.core import ParamsConfig, QueryConfig
from ._sqlachemy_filter_handler import SqlAlchemyFilterHandler

class SqlAlchemyLoadFromDb:
    df: dd.DataFrame

    def __init__(
        self,
        plugin_sqlalchemy: SqlAlchemyConnectionConfig,  # Expected to be an instance of SqlAlchemyConnection
        plugin_query: QueryConfig = None,
        plugin_params: ParamsConfig = None,
        logger: Optional[logging.Logger] = None,
        **kwargs,
    ):
        """
        Initialize the loader with database connection, query, and parameters.
        """
        self.db_connection = plugin_sqlalchemy
        self.table_name = self.db_connection.table
        self.model = self.db_connection.model
        self.engine = self.db_connection.engine
        self.logger = logger or self._default_logger()
        self.query_config =  plugin_query
        self.params_config = plugin_params
        self.debug = kwargs.pop("debug", False)
        self.verbose_debug = kwargs.pop("verbose_debug", False)

    def _default_logger(self) -> logging.Logger:
        """Create a default logger."""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("SQLAlchemyLoadFromDb")

    def build_and_load(self) -> dd.DataFrame:
        """
        Load data into a Dask DataFrame based on the query and parameters.
        """
        self.df = self._build_and_load()
        return self.df

    def _build_and_load(self) -> dd.DataFrame:
        """
        Query the database and load results into a Dask DataFrame.
        """
        with Session(self.engine) as session:
            try:
                query = select(self.model)
                filters = self.params_config.filters
                if filters:
                    n_records = 0
                    query = SqlAlchemyFilterHandler.apply_filters_sqlalchemy(query, self.model,self.params_config.filters)
                else:
                    n_records = self.query_config.n_records or 100

                if n_records:
                    query = query.limit(n_records)

                # Debug: Log the SQL query
                if self.debug:
                    self.logger.info(f"Executing query: {str(query)}")

                # Execute the query
                try:
                    results = session.exec(query).fetchall()
                    if results:
                        records = [
                            {key: getattr(result, key) for key in result.__table__.columns.keys()}
                                for result in results
                        ]
                    df = dd.from_pandas(pd.DataFrame(records), npartitions=1)
                except Exception as e:
                    print(e)
                    self.logger.warning("Query returned no results.")
                    df = dd.from_pandas(pd.DataFrame(), npartitions=1)

            except Exception as e:
                print(e)
                self.logger.error(f"Error loading data: {e}")
                df = dd.from_pandas(pd.DataFrame(), npartitions=1)

            return df

