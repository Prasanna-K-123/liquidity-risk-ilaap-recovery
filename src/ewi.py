from __future__ import annotations

import pandas as pd


def build_early_warning_indicators(stress_summary: pd.DataFrame, base_lcr: float, nsfr: float,
                                   wholesale_share: float, hqla_ratio: float) -> pd.DataFrame:
    severe = stress_summary.loc[stress_summary["scenario"] == "combined_severe"].iloc[0]
    indicators = [
        ("base LCR-style", base_lcr, 1.10, "low"),
        ("NSFR-style", nsfr, 1.05, "low"),
        ("severe survival days", float(severe["survival_horizon_days"]), 30.0, "low"),
        ("wholesale funding share", wholesale_share, 0.20, "high"),
        ("HQLA / assets", hqla_ratio, 0.12, "low"),
    ]
    rows = []
    for name, value, trigger, direction in indicators:
        triggered = value <= trigger if direction == "low" else value >= trigger
        rows.append({"indicator": name, "value": value, "trigger": trigger,
                     "trigger_direction": direction, "status": "TRIGGER" if triggered else "NORMAL"})
    return pd.DataFrame(rows)
