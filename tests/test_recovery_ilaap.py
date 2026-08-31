from src.config import STRESS_SCENARIOS
from src.ilaap import ilaap_assessment, reverse_stress
from src.liquidity import cashflow_ladder, lcr_style, nsfr_style
from src.portfolio import generate_balance_sheet
from src.recovery import recovery_waterfall
from src.stress import run_stress_scenarios


def test_recovery_waterfall_is_monotone():
    r = recovery_waterfall(-2_000_000_000.0)
    assert r["post_action_liquidity"].is_monotonic_increasing
    assert (r["deployed"] >= 0).all()


def test_ilaap_and_reverse_stress_execute():
    df = generate_balance_sheet(n_accounts=3000)
    base = lcr_style(df)
    stable = nsfr_style(df)
    stress = run_stress_scenarios(df)
    c = STRESS_SCENARIOS["combined_severe"]
    severe = cashflow_ladder(df, c["deposit_multiplier"], c["draw_multiplier"], c["wholesale_rollover"], c["haircut_add"])
    assessment = ilaap_assessment(base["lcr"], stable["nsfr"], stress, severe)
    assert assessment["recovery_capacity"] > 0
    rev = reverse_stress(df, cashflow_ladder, max_multiplier=4.0, step=0.25)
    assert "breach_deposit_multiplier" in rev
