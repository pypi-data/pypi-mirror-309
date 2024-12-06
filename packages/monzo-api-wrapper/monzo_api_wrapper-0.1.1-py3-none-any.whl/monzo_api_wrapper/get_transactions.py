from datetime import datetime, timedelta

import pandas as pd
from monzo.endpoints.transaction import Authentication, Transaction

from monzo_api_wrapper.utils.custom_logger import CustomLogger, loggable

logger = CustomLogger.get_logger()


@loggable
def get_transactions_df(
    monzo_auth: Authentication, account_id: str, account_name: str, days_lookback: int = 30
) -> pd.DataFrame:
    """Fetch recent transactions from Monzo API.

    Args:
        monzo_auth (Authentication): Monzo authentication object.
        account_id (str): Monzo account ID.
        account_name (str): Monzo account name.
        days_lookback (int): Number of days to look back, defaults to 30.

    Returns:
        pd.DataFrame: DataFrame of fetched transactions.

    """
    try:
        since_date = datetime.today() - timedelta(days=days_lookback)
        fetched_transactions_list = Transaction.fetch(
            auth=monzo_auth,
            account_id=account_id,
            since=since_date,
            expand=["merchant"],
        )
        logger.debug(f"Fetched {len(fetched_transactions_list)} transactions from {account_name}")

        if not fetched_transactions_list:
            logger.debug(
                f"No transactions found for {account_name} over the last {days_lookback} days."
            )
            return pd.DataFrame()

        return pd.DataFrame([
            {
                "id": trn.transaction_id,
                "date": trn.created,
                "description": trn.description,
                "amount": trn.amount,
                "category": trn.category,
                "decline_reason": trn.decline_reason,
                "meta": trn.metadata,
                "merchant": trn.merchant,
                "currency": trn.currency,
                "local_currency": trn.local_currency,
                "local_amount": trn.local_amount,
                "source": account_name,
            }
            for trn in fetched_transactions_list
        ])

    except Exception:
        logger.exception(f"Error fetching transactions for {account_name}")
        raise
