from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import BASE_RUNOFF, BUCKET_DAYS, LIMITS, TIME_BUCKETS


def hqla_value(df: pd.DataFrame, haircut_add: float = 0.0) -> float:
    assets = df[df["is_asset"]].copy()
    effective_haircut = np.clip(assets["base_haircut"] + haircut_add, 0.0, 1.0)
    return float((assets["amount"] * (1.0 - effective_haircut)).sum())


def lcr_style(df: pd.DataFrame, deposit_multiplier: float = 1.0, draw_multiplier: float = 1.0,
              haircut_add: float = 0.0, wholesale_rollover: float = 0.85) -> dict[str, float]:
    liabilities = df[df["is_liability"]].copy()
    runoff = liabilities["product"].map(BASE_RUNOFF).fillna(0.0).astype(float)
    runoff = np.clip(runoff * deposit_multiplier, 0.0, 1.0)
    wholesale = liabilities["product"] == "wholesale_unsecured"
    runoff.loc[wholesale] = np.maximum(runoff.loc[wholesale], 1.0 - wholesale_rollover)
    cash_outflows = float((liabilities["amount"] * runoff).sum())

    facilities = df[df["is_off_balance"]]
    facility_draws = float((facilities["amount"] * np.clip(0.10 * draw_multiplier, 0.0, 1.0)).sum())
    near_term_assets = df[(df["is_asset"]) & (df["bucket"].isin(["overnight", "2d-7d", "8d-30d"]))]
    inflows = float((near_term_assets["amount"] * (1.0 - near_term_assets["base_haircut"])).sum())
    recognised_inflows = min(inflows, 0.75 * (cash_outflows + facility_draws))
    net_outflows = max(cash_outflows + facility_draws - recognised_inflows, 1.0)
    hqla = hqla_value(df, haircut_add=haircut_add)
    return {"hqla": hqla, "gross_30d_outflows": cash_outflows + facility_draws,
            "recognised_30d_inflows": recognised_inflows, "net_30d_outflows": net_outflows,
            "lcr": hqla / net_outflows}


def nsfr_style(df: pd.DataFrame) -> dict[str, float]:
    available = float((df["amount"] * df["asf_weight"]).sum())
    required = max(float((df["amount"] * df["rsf_weight"]).sum()), 1.0)
    return {"available_stable_funding": available, "required_stable_funding": required, "nsfr": available / required}


def cashflow_ladder(df: pd.DataFrame, deposit_multiplier: float = 1.0, draw_multiplier: float = 1.0,
                    wholesale_rollover: float = 0.85, haircut_add: float = 0.0) -> pd.DataFrame:
    rows = []
    cumulative = 0.0
    buffer = hqla_value(df, haircut_add=haircut_add)
    for bucket in TIME_BUCKETS:
        subset = df[df["bucket"] == bucket]
        inflow_assets = subset[(subset["is_asset"]) & (subset["product"] != "treasury_hqla")]
        inflows = float((inflow_assets["amount"] * (1.0 - np.clip(inflow_assets["base_haircut"] + haircut_add, 0.0, 1.0))).sum())

        liabilities = subset[subset["is_liability"]]
        runoff = liabilities["product"].map(BASE_RUNOFF).fillna(0.0).astype(float)
        runoff = np.clip(runoff * deposit_multiplier, 0.0, 1.0)
        wholesale = liabilities["product"] == "wholesale_unsecured"
        runoff.loc[wholesale] = np.maximum(runoff.loc[wholesale], 1.0 - wholesale_rollover)
        outflows = float((liabilities["amount"] * runoff).sum())

        facilities = subset[subset["is_off_balance"]]
        facility_draw = float((facilities["amount"] * np.clip(0.10 * draw_multiplier, 0.0, 1.0)).sum())
        net = inflows - outflows - facility_draw
        cumulative += net
        rows.append({"bucket": bucket, "days": BUCKET_DAYS[bucket], "inflows": inflows,
                     "outflows": outflows + facility_draw, "net_cashflow": net,
                     "cumulative_gap": cumulative, "post_buffer_liquidity": buffer + cumulative})
    return pd.DataFrame(rows)


def survival_horizon_days(ladder: pd.DataFrame) -> int:
    depleted = ladder[ladder["post_buffer_liquidity"] < 0]
    if depleted.empty:
        return int(ladder["days"].max())
    return int(depleted.iloc[0]["days"])


def risk_limits(df: pd.DataFrame, base_lcr: float, nsfr: float, ladder: pd.DataFrame) -> pd.DataFrame:
    total_assets = float(df.loc[df["is_asset"], "amount"].sum())
    buffer_ratio = hqla_value(df) / total_assets
    within_30 = ladder[ladder["days"] <= 30]
    gap_30 = float(within_30.iloc[-1]["cumulative_gap"]) if not within_30.empty else 0.0
    gap_ratio = gap_30 / total_assets
    survival = survival_horizon_days(ladder)
    checks = [
        ("LCR-style ratio", base_lcr, LIMITS["minimum_lcr"]),
        ("NSFR-style ratio", nsfr, LIMITS["minimum_nsfr"]),
        ("survival horizon days", float(survival), float(LIMITS["minimum_survival_days"])),
        ("30d cumulative gap / assets", gap_ratio, LIMITS["maximum_30d_cumulative_gap_ratio"]),
        ("liquidity buffer / assets", buffer_ratio, LIMITS["minimum_liquidity_buffer_ratio"]),
    ]
    return pd.DataFrame([{"metric": n, "value": v, "limit": l, "operator": ">=", "status": "PASS" if v >= l else "BREACH"} for n, v, l in checks])
