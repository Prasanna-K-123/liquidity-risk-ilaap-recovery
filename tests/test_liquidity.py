from src.liquidity import cashflow_ladder, lcr_style, nsfr_style, survival_horizon_days
from src.portfolio import generate_balance_sheet, validate_balance_sheet


def test_portfolio_and_core_ratios_are_valid():
    df = generate_balance_sheet(n_accounts=2000)
    validate_balance_sheet(df)
    lcr = lcr_style(df)
    nsfr = nsfr_style(df)
    assert lcr["hqla"] > 0
    assert lcr["net_30d_outflows"] > 0
    assert lcr["lcr"] > 0
    assert nsfr["nsfr"] > 0
    ladder = cashflow_ladder(df)
    assert len(ladder) == 6
    assert survival_horizon_days(ladder) >= 1

def test_treasury_buffer_and_non_treasury_inflows_are_disjoint():
    """A treasury asset cannot be counted as both opening buffer and maturing inflow."""
    import pandas as pd
    from src.liquidity import hqla_value

    records = [
        {"product": "treasury_hqla", "amount": 100.0, "base_haircut": 0.05,
         "bucket": "overnight", "is_asset": True, "is_liability": False, "is_off_balance": False},
        {"product": "corporate_loan", "amount": 100.0, "base_haircut": 0.65,
         "bucket": "overnight", "is_asset": True, "is_liability": False, "is_off_balance": False},
        {"product": "wholesale_unsecured", "amount": 500.0, "base_haircut": 0.0,
         "bucket": "overnight", "is_asset": False, "is_liability": True, "is_off_balance": False},
    ]
    df = pd.DataFrame(records)
    assert abs(hqla_value(df) - 95.0) < 1e-12
    ratio = lcr_style(df)
    assert abs(ratio["hqla"] - 95.0) < 1e-12
    assert abs(ratio["gross_30d_outflows"] - 300.0) < 1e-12
    assert abs(ratio["recognised_30d_inflows"] - 35.0) < 1e-12
    assert abs(ratio["net_30d_outflows"] - 265.0) < 1e-12
    assert abs(ratio["lcr"] - 95.0 / 265.0) < 1e-12
    ladder = cashflow_ladder(df)
    assert abs(float(ladder.iloc[0]["inflows"]) - 35.0) < 1e-12
    assert abs(float(ladder.iloc[0]["post_buffer_liquidity"]) + 170.0) < 1e-12
    assert abs(hqla_value(df, haircut_add=0.25) - 70.0) < 1e-12


def test_treasury_maturity_does_not_create_inflow():
    import pandas as pd
    df = pd.DataFrame([
        {"product": "treasury_hqla", "amount": 100.0, "base_haircut": 0.05,
         "bucket": "overnight", "is_asset": True, "is_liability": False, "is_off_balance": False},
        {"product": "retail_stable", "amount": 200.0, "base_haircut": 0.0,
         "bucket": "overnight", "is_asset": False, "is_liability": True, "is_off_balance": False},
    ])
    ratio = lcr_style(df)
    assert ratio["hqla"] == 95.0
    assert ratio["recognised_30d_inflows"] == 0.0
    assert ratio["gross_30d_outflows"] == 10.0
    assert float(cashflow_ladder(df).iloc[0]["inflows"]) == 0.0
