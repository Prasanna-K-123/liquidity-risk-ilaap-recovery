from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import N_ACCOUNTS, RANDOM_STATE, TIME_BUCKETS


def generate_balance_sheet(n_accounts: int = N_ACCOUNTS, seed: int = RANDOM_STATE) -> pd.DataFrame:
    """Create a deterministic synthetic bank balance-sheet/funding population."""
    rng = np.random.default_rng(seed)
    products = np.array([
        "retail_stable", "retail_less_stable", "corporate_operational",
        "corporate_non_operational", "wholesale_unsecured", "loans",
        "treasury_hqla", "corporate_bonds", "equities", "committed_facilities",
    ])
    probs = np.array([0.22, 0.14, 0.08, 0.08, 0.05, 0.19, 0.09, 0.06, 0.03, 0.06])
    product = rng.choice(products, size=n_accounts, p=probs)

    is_liability = np.isin(product, [
        "retail_stable", "retail_less_stable", "corporate_operational",
        "corporate_non_operational", "wholesale_unsecured",
    ])
    is_asset = np.isin(product, ["loans", "treasury_hqla", "corporate_bonds", "equities"])
    is_off_balance = product == "committed_facilities"

    amount = rng.lognormal(mean=np.log(2_500_000), sigma=1.05, size=n_accounts) * 1.25
    bucket_probs = {
        "liability": np.array([0.34, 0.18, 0.20, 0.12, 0.10, 0.06]),
        "asset": np.array([0.06, 0.07, 0.13, 0.18, 0.27, 0.29]),
        "off_balance": np.array([0.06, 0.09, 0.20, 0.25, 0.25, 0.15]),
    }
    bucket = []
    for a, l in zip(is_asset, is_liability):
        key = "asset" if a else "liability" if l else "off_balance"
        bucket.append(rng.choice(TIME_BUCKETS, p=bucket_probs[key]))

    df = pd.DataFrame({
        "account_id": [f"A{i:05d}" for i in range(n_accounts)],
        "product": product,
        "amount": amount,
        "bucket": bucket,
        "is_asset": is_asset,
        "is_liability": is_liability,
        "is_off_balance": is_off_balance,
    })

    df["base_haircut"] = np.select(
        [product == "treasury_hqla", product == "corporate_bonds", product == "equities", product == "loans"],
        [0.05, 0.20, 0.45, 0.65], default=1.0,
    ).astype(float)
    df["asf_weight"] = np.select(
        [product == "retail_stable", product == "retail_less_stable", product == "corporate_operational",
         product == "corporate_non_operational", product == "wholesale_unsecured"],
        [0.95, 0.90, 0.50, 0.50, 0.00], default=0.0,
    ).astype(float)
    df["rsf_weight"] = np.select(
        [product == "treasury_hqla", product == "corporate_bonds", product == "equities", product == "loans"],
        [0.05, 0.50, 0.85, 0.85], default=0.0,
    ).astype(float)
    return df


def validate_balance_sheet(df: pd.DataFrame) -> None:
    required = {"account_id", "product", "amount", "bucket", "is_asset", "is_liability", "is_off_balance", "base_haircut", "asf_weight", "rsf_weight"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing balance-sheet fields: {sorted(missing)}")
    if len(df) < 1000:
        raise ValueError("Demonstration population is unexpectedly small")
    if (df["amount"] <= 0).any():
        raise ValueError("All account amounts must be positive")
    role_count = df[["is_asset", "is_liability", "is_off_balance"]].sum(axis=1)
    if not (role_count == 1).all():
        raise ValueError("Every account must map to exactly one balance-sheet role")
