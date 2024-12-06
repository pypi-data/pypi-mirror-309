import pandas as pd
from monzo.authentication import Authentication
from monzo.endpoints.pot import Pot

from monzo_api_wrapper.utils.custom_logger import loggable


@loggable
def get_balances(monzo_auth: Authentication, source_account: str) -> pd.DataFrame:
    """Fetch and process balances from Monzo pots.

    Args:
        monzo_auth (object): Monzo authentication object.
        source_account (str): Monzo source account ID.

    Returns:
        pd.DataFrame: DataFrame containing the balances and details of pots.

    """
    fetched_pots = Pot.fetch(auth=monzo_auth, account_id=source_account)
    pots_data = [
        (pot.pot_id, pot.name, pot.style, pot.balance / 100, pot.currency, pot.deleted)
        for pot in fetched_pots
    ]

    columns = ["id", "name", "style", "balance", "currency", "deleted"]
    return pd.DataFrame(pots_data, columns=columns)
