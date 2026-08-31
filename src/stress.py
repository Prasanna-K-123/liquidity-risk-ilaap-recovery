from __future__ import annotations

import pandas as pd

from src.config import STRESS_SCENARIOS
from src.liquidity import cashflow_ladder, lcr_style, survival_horizon_days


def run_stress_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, s in STRESS_SCENARIOS.items():
        lcr = lcr_style(df, s["deposit_multiplier"], s["draw_multiplier"], s["haircut_add"], s["wholesale_rollover"])
        ladder = cashflow_ladder(df, s["deposit_multiplier"], s["draw_multiplier"], s["wholesale_rollover"], s["haircut_add"])
        rows.append({"scenario": name, "hqla": lcr["hqla"], "net_30d_outflows": lcr["net_30d_outflows"],
                     "lcr": lcr["lcr"], "survival_horizon_days": survival_horizon_days(ladder),
                     "minimum_post_buffer_liquidity": float(ladder["post_buffer_liquidity"].min())})
    return pd.DataFrame(rows)
