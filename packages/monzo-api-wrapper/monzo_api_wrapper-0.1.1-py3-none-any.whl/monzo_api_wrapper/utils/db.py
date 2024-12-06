import os
from typing import Optional

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from monzo_api_wrapper.utils import sql_templates
from monzo_api_wrapper.utils.custom_logger import CustomLogger

logger = CustomLogger.get_logger()


class InsertArgumentError(ValueError):
    """Custom exception raised when both DataFrame and SQL string arguments are missing
    for an insert operation.

    This exception is used to ensure that at least one valid data source (a
    DataFrame or an SQL string) is provided when attempting to insert data into
    the database.

    """

    def __init__(self) -> None:
        """Initialize the InsertArgumentError exception with a specific error message.

        This constructor sets the error message that indicates that either a
        DataFrame or an SQL string must be provided for an insert operation.

        The error message is passed to the base ValueError class.

        """
        super().__init__(
            "Either a DataFrame or SQL string must be provided for the insert operation."
        )


class Db:
    """Class to manage connection to a database and perform SQL operations."""

    def __init__(self) -> None:
        """Initialize the Db class and set up a database engine.

        Initializes the SQLAlchemy engine and logs the connection status.

        """
        self.engine = self.create_db_engine()
        logger.debug(f"Connected to database: {os.getenv('DB_NAME')}")

    def create_db_engine(self) -> Engine:
        """Create an SQLAlchemy engine for the database connection.

        Returns:
            Engine: An SQLAlchemy Engine instance configured with database connection details.

        """
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        host = os.getenv("DB_HOST")
        database_type = os.getenv("DB_TYPE")
        database_name = os.getenv("DB_NAME")
        port = os.getenv("DB_PORT")
        sql_string = f"{database_type}://{username}:{password}@{host}:{port}/{database_name}"
        return create_engine(sql_string)

    def query(self, sql: str, return_data: bool = True) -> Optional[pd.DataFrame]:
        """Execute an SQL query against the database.

        Args:
            sql (str): The SQL query to be executed.
            return_data (bool, optional): If True, returns query data as a DataFrame. Defaults to True.

        Returns:
            Optional[pd.DataFrame]: DataFrame with query results if return_data=True, else None.

        """
        if return_data:
            return pd.read_sql_query(sql, self.engine)
        with self.engine.begin() as conn:
            conn.execute(sqlalchemy.text(sql))
        return None

    def insert(
        self, table: str, df: Optional[pd.DataFrame] = None, sql: Optional[str] = None
    ) -> None:
        """Insert data into a table in the database.

        Args:
            table (str): The name of the target database table.
            df (Optional[pd.DataFrame]): DataFrame containing data to insert. Defaults to None.
            sql (Optional[str]): Custom SQL insert statement. Defaults to None.

        Raises:
            InsertArgumentError: If both `df` and `sql` are None.

        """
        if df is None and not sql:
            raise InsertArgumentError()

        if sql:
            insert_sql = f"INSERT INTO {table} (\n{sql}\n);"
            self.query(insert_sql, return_data=False)
            logger.debug(f"Data inserted into {table}")
        else:
            if df is not None:
                rows = len(df)
                chunksize = 20000 if rows > 20000 else None
                schema, table_name = table.split(".")
                with self.engine.begin() as conn:
                    df.to_sql(
                        schema=schema,
                        name=table_name,
                        index=False,
                        con=conn,
                        if_exists="append",
                        method="multi",
                        chunksize=chunksize,
                    )
                logger.debug(f"{rows} rows inserted into {schema}.{table_name}")

    def delete(self, table: str, data: str) -> None:
        """Delete data from a table in the database.

        Args:
            table (str): The name of the database table from which data will be deleted.
            data (str): Condition to specify which rows to delete, formatted as a SQL condition.

        """
        sql_delete = sql_templates.delete.format(table=table, data=data)
        logger.info(f"Running delete statement: {sql_delete}")
        self.query(sql=sql_delete, return_data=False)
