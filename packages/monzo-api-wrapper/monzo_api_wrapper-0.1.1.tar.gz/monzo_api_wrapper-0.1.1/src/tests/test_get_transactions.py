from unittest.mock import MagicMock

import pandas as pd
from monzo.endpoints.transaction import Authentication, Transaction

from monzo_api_wrapper.get_transactions import (
    get_transactions_df,
)


def test_get_transactions_df(monkeypatch):
    mock_transactions = [
        MagicMock(
            transaction_id="txn1",
            created="2023-11-01T12:00:00Z",
            description="Coffee Shop",
            amount=-300,
            category="eating_out",
            decline_reason=None,
            metadata={"note": "Latte"},
            merchant="Coffee House",
            currency="GBP",
            local_currency="GBP",
            local_amount=-300,
        ),
        MagicMock(
            transaction_id="txn2",
            created="2023-11-02T15:30:00Z",
            description="Book Store",
            amount=-1200,
            category="shopping",
            decline_reason=None,
            metadata={"note": "Notebook"},
            merchant="Books & Co.",
            currency="GBP",
            local_currency="GBP",
            local_amount=-1200,
        ),
    ]

    monkeypatch.setattr(
        Transaction, "fetch", lambda auth, account_id, since, expand: mock_transactions
    )

    mock_auth = MagicMock(spec=Authentication)

    result = get_transactions_df(mock_auth, "dummy_account_id", "Test Account")

    expected_df = pd.DataFrame({
        "id": ["txn1", "txn2"],
        "date": ["2023-11-01T12:00:00Z", "2023-11-02T15:30:00Z"],
        "description": ["Coffee Shop", "Book Store"],
        "amount": [-300.0, -1200.0],
        "category": ["eating_out", "shopping"],
        "decline_reason": [None, None],
        "meta": [{"note": "Latte"}, {"note": "Notebook"}],
        "merchant": ["Coffee House", "Books & Co."],
        "currency": ["GBP", "GBP"],
        "local_currency": ["GBP", "GBP"],
        "local_amount": [-300, -1200],
        "source": ["Test Account", "Test Account"],
    })

    result["date"] = pd.to_datetime(result["date"])
    expected_df["date"] = pd.to_datetime(expected_df["date"])
    result["amount"] = result["amount"].astype(float)
    expected_df["amount"] = expected_df["amount"].astype(float)

    pd.testing.assert_frame_equal(result, expected_df)
