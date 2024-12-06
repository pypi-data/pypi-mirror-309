import pandas as pd

from monzo_api_wrapper.utils import sql_templates
from monzo_api_wrapper.utils.custom_logger import CustomLogger, loggable
from monzo_api_wrapper.utils.db import Db

logger = CustomLogger.get_logger()


class NoTransactionsFoundError(Exception):
    """Exception raised when no transactions are found in the database."""

    def __init__(self, message: str = "No transactions found in database.") -> None:
        """Initializes the NoTransactionsFoundError exception.

        Args:
            message (str): A custom error message to describe the exception.
                           Defaults to "No transactions found in database."

        """
        self.message = message
        super().__init__(self.message)


@loggable
def get_db_transactions(db: Db, table: str) -> pd.DataFrame | None:
    """Fetch transactions from the database.

    Args:
        db (Db): Database connection object.
        table (str): Name of the table to fetch transactions from.

    Returns:
        pd.DataFrame | None: DataFrame containing the transactions fetched from the database.

    """
    return db.query(
        sql=sql_templates.exists.format(table=table),
        return_data=True,
    )


@loggable
def get_new_transactions(db: Db, table: str, fetched_transactions: pd.DataFrame) -> pd.DataFrame:
    """Identify new transactions that are not present in the database.

    Args:
        db (Db): Database connection object.
        table (str): Name of the table to check transactions against.
        fetched_transactions (pd.DataFrame): DataFrame containing fetched transactions.

    Returns:
        pd.DataFrame: DataFrame containing new transactions to be uploaded.

    """
    db_transactions = get_db_transactions(db, table)
    db_ids_lst = db_transactions["id"].tolist() if db_transactions is not None else []

    new_transaction_ids = [
        item for item in fetched_transactions["id"].tolist() if item not in db_ids_lst
    ]

    return fetched_transactions[fetched_transactions["id"].isin(new_transaction_ids)].reset_index(
        drop=True
    )


@loggable
def get_changed_transaction_ids(
    db: Db, table: str, fetched_transactions: pd.DataFrame
) -> list[str]:
    """Identify transactions that have changed based on a set of columns.

    Args:
        db (Db): Database connection object.
        table (str): Name of the table to check transactions against.
        fetched_transactions (pd.DataFrame): DataFrame containing fetched transactions.

    Returns:
       Optional[List[str]]: List of transactions IDs that have changed, or None if no changes are found.

    Raises:
        NoTransactionsFoundError: If no transactions are found in the database.

    """
    compare_transaction_cols = ["id", "description", "amount", "category", "notes", "timestamp"]

    logger.debug("Getting existing transactions from database")
    db_transactions = get_db_transactions(db, table)
    if db_transactions.empty:
        raise NoTransactionsFoundError()

    logger.debug("Standardizing columns for comparison")
    db_transactions["date"] = pd.to_datetime(db_transactions["date"])
    fetched_transactions["date"] = pd.to_datetime(fetched_transactions["date"])
    db_transactions["amount"] = db_transactions["amount"].round(2)

    logger.debug("Creating comparable subsets of database and fetched transactions")
    fetched_transactions_subset = (
        fetched_transactions[fetched_transactions["id"].isin(db_transactions["id"])][
            compare_transaction_cols
        ]
        .sort_values("id")
        .reset_index(drop=True)
    )  # Exclude any new transactions not in database
    fetched_transactions_subset.fillna("", inplace=True)
    db_transactions_subset = (
        db_transactions[db_transactions["id"].isin(fetched_transactions["id"])][
            compare_transaction_cols
        ]
        .sort_values("id")
        .reset_index(drop=True)
    )
    db_transactions_subset.fillna("", inplace=True)

    logger.debug("Comparing transactions to identify differences")

    differences = (
        fetched_transactions_subset[compare_transaction_cols[1:]]  # Exclude 'id' column
        .ne(db_transactions_subset[compare_transaction_cols[1:]])
        .any(axis=1)
    )
    return fetched_transactions_subset.loc[differences, "id"].tolist()
