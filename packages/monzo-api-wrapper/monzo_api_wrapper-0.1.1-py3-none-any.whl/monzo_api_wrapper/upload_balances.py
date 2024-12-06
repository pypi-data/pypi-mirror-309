from typing import Any

import numpy as np
import pandas as pd

from monzo_api_wrapper.utils import sql_templates
from monzo_api_wrapper.utils.custom_logger import loggable
from monzo_api_wrapper.utils.db import Db


@loggable
def _get_uploaded_balances(database: Db, table_name: str) -> pd.DataFrame | None:
    """Retrieve uploaded balances from the database.

    Args:
        database (Db): Database connection object.
        table_name (str): Name of the table to query.

    Returns:
        pd.DataFrame | None: DataFrame containing the uploaded balances, or None if no data is found.

    """
    return database.query(
        sql=sql_templates.exists_pots.format(table=table_name),
        return_data=True,
    )


@loggable
def _prepare_balances(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare the balance DataFrame by sorting, resetting index, handling nulls, and
    rounding.

    Args:
        df (pd.DataFrame): DataFrame to be processed.

    Returns:
        pd.DataFrame: Processed DataFrame.

    """
    return (
        df.sort_values("id")
        .reset_index(drop=True)
        .replace({None: np.nan})
        .fillna(0)
        .astype({"balance": float})
        .round({"balance": 2})
    )


@loggable
def get_new_balances(database: Db, table_name: str, current_balances: pd.DataFrame) -> pd.DataFrame:
    """Identify new balances that are not yet uploaded to the database.

    Args:
        database (Db): Database connection object.
        table_name (str): Name of the table to check for existing balances.
        current_balances (pd.DataFrame): DataFrame containing the current balances.

    Returns:
        pd.DataFrame: DataFrame containing the new balances to be uploaded.

    """
    existing_balances = _get_uploaded_balances(database, table_name)
    if existing_balances is not None:
        existing_balance_ids = set(existing_balances["id"])
        new_balances = current_balances[~current_balances["id"].isin(existing_balance_ids)]
        return new_balances.reset_index(drop=True)
    return current_balances


@loggable
def get_changed_balances(
    database: Db, table_name: str, current_balances: pd.DataFrame
) -> pd.DataFrame | Any:
    """Identify balances that have changed compared to the ones in the database.

    Args:
        database (Db): Database connection object.
        table_name (str): Name of the table to check for existing balances.
        current_balances (pd.DataFrame): DataFrame containing the current balances.

    Returns:
        pd.DataFrame: DataFrame containing the balances that have changed.

    """
    existing_balances = _get_uploaded_balances(database, table_name)
    if existing_balances is None:
        return pd.DataFrame()

    existing_balance_ids = set(existing_balances["id"])
    matched_balances = _prepare_balances(
        current_balances[current_balances["id"].isin(existing_balance_ids)]
    )
    matched_existing_balances = _prepare_balances(
        existing_balances[existing_balances["id"].isin(matched_balances["id"])]
    )

    # Return rows where any column value has changed
    return matched_balances[matched_existing_balances.ne(matched_balances).any(axis=1)]


@loggable
def update_changed_balances(
    database: Db, table_name: str, current_balances: pd.DataFrame, updated_balances: pd.DataFrame
) -> None:
    """Update the balances in the database by deleting and reinserting the changed
    balances.

    Args:
        database (Db): Database connection object.
        table_name (str): Name of the table to update balances.
        current_balances (pd.DataFrame): DataFrame containing the current balances.
        updated_balances (pd.DataFrame): DataFrame containing the balances that have changed.

    """
    if updated_balances.empty:
        return

    ids_to_delete = ",".join(map(str, updated_balances["id"]))
    database.delete(table_name, ids_to_delete)

    reinserted_balances = current_balances[current_balances["id"].isin(updated_balances["id"])]
    database.insert(table_name, reinserted_balances)
