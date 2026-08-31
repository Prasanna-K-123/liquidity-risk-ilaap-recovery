from __future__ import annotations

import pandas as pd

from src.recovery import recovery_capacity


def ilaap_assessment(base_lcr: float, nsfr: float, stress_summary: pd.DataFrame,
                     severe_ladder: pd.DataFrame) -> dict[str, float | str]:
    severe = stress_summary.loc[stress_summary["scenario"] == "combined_severe"].iloc[0]
    worst_liquidity = float(severe_ladder["post_buffer_liquidity"].min())
    deficit = max(-worst_liquidity, 0.0)
    capacity = recovery_capacity()
    return {
        "base_lcr": float(base_lcr), "base_nsfr": float(nsfr), "severe_lcr": float(severe["lcr"]),
        "severe_survival_days": int(severe["survival_horizon_days"]),
        "severe_peak_liquidity_deficit": deficit, "recovery_capacity": capacity,
        "post_full_recovery_liquidity": worst_liquidity + capacity,
        "recovery_covers_peak_deficit": "yes" if capacity >= deficit else "no",
    }


def reverse_stress(df, ladder_factory, max_multiplier: float = 4.0, step: float = 0.05) -> dict[str, float]:
    multiplier = 1.0
    while multiplier <= max_multiplier + 1e-9:
        ladder = ladder_factory(df, deposit_multiplier=multiplier, draw_multiplier=1.5,
                                wholesale_rollover=0.25, haircut_add=0.15)
        within_30 = ladder[ladder["days"] <= 30]
        min_liq = float(within_30["post_buffer_liquidity"].min())
        if min_liq < 0:
            return {"breach_deposit_multiplier": multiplier, "minimum_30d_liquidity": min_liq}
        multiplier = round(multiplier + step, 10)
    return {"breach_deposit_multiplier": float("nan"), "minimum_30d_liquidity": float("nan")}
