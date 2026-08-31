from src.portfolio import generate_balance_sheet
from src.stress import run_stress_scenarios


def test_severe_stress_is_worse_than_base():
    df = generate_balance_sheet(n_accounts=2500)
    s = run_stress_scenarios(df).set_index("scenario")
    assert s.loc["combined_severe", "lcr"] < s.loc["base", "lcr"]
    assert s.loc["combined_severe", "hqla"] < s.loc["base", "hqla"]
