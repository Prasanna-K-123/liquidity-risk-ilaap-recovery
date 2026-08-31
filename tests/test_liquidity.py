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
