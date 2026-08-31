from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_figures(base_ladder: pd.DataFrame, stress_summary: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(base_ladder["days"], base_ladder["post_buffer_liquidity"] / 1e9, marker="o")
    ax.axhline(0.0, linewidth=1)
    ax.set_xlabel("Days")
    ax.set_ylabel("Post-buffer liquidity (USD bn)")
    ax.set_title("Base liquidity survival profile")
    fig.tight_layout()
    fig.savefig(outdir / "base_survival_profile.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(stress_summary["scenario"], stress_summary["lcr"])
    ax.axhline(1.0, linewidth=1)
    ax.set_ylabel("LCR-style ratio")
    ax.set_title("Liquidity ratio under stress")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(outdir / "stress_lcr.png", dpi=160)
    plt.close(fig)


def write_report(metrics: dict, stress: pd.DataFrame, limits: pd.DataFrame, ewi: pd.DataFrame,
                 recovery: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    p, b, i, r = metrics["portfolio"], metrics["base"], metrics["ilaap"], metrics["reverse_stress"]
    text = f"""# ILAAP-style liquidity risk assessment

## Executive conclusion

This repository demonstrates a reproducible **liquidity risk, stress testing, ILAAP-style assessment and recovery-planning framework** on a deterministic synthetic bank balance sheet. The data and behavioral assumptions are illustrative; the project is not a regulatory return and does not claim institution-specific calibration.

## Base balance sheet and liquidity position

- Accounts/facilities: **{p['accounts']:,}**
- Total assets: **{p['total_assets']:,.0f}**
- Total liabilities: **{p['total_liabilities']:,.0f}**
- HQLA-style post-haircut buffer: **{b['hqla']:,.0f}**
- LCR-style ratio: **{b['lcr']:.2f}x**
- NSFR-style ratio: **{b['nsfr']:.2f}x**
- Base survival horizon: **{b['survival_horizon_days']} days**

## Stress testing

{stress.to_markdown(index=False)}

## Risk appetite / limit monitoring

{limits.to_markdown(index=False)}

## Early-warning indicators

{ewi.to_markdown(index=False)}

## ILAAP-style assessment

- Severe peak liquidity deficit: **{i['severe_peak_liquidity_deficit']:,.0f}**
- Available recovery capacity: **{i['recovery_capacity']:,.0f}**
- Recovery covers peak deficit: **{i['recovery_covers_peak_deficit']}**
- Reverse-stress deposit runoff multiplier producing a 30-day breach: **{r['breach_deposit_multiplier']:.2f}x**

## Recovery option waterfall

{recovery.to_markdown(index=False)}

## Model-risk judgement

The framework deliberately distinguishes methodology from evidence. Account balances, maturity structure, behavioral runoff rates, asset haircuts, rollover assumptions, recovery capacities and EWI thresholds are synthetic or illustrative. LCR/NSFR calculations are simplified analytical analogues intended to demonstrate the mechanics and governance workflow; a production implementation requires the applicable jurisdictional rulebook, legal-entity perimeter, product-level classifications, encumbrance data, contractual/behavioral cash-flow models, validated runoff/drawdown assumptions, collateral eligibility and management-action feasibility.

## Production remediation

1. replace the synthetic balance sheet with governed treasury/ALM data and legal-entity mapping;
2. reconcile contractual cash flows to finance and regulatory reporting systems;
3. validate behavioral deposit decay, facility drawdown, rollover and intraday liquidity assumptions;
4. implement jurisdiction-specific HQLA eligibility, caps, haircuts, ASF and RSF classifications;
5. calibrate stress severity to historical and forward-looking scenarios and document management overlays;
6. validate recovery action capacity, execution time, collateral availability and operational dependencies;
7. establish independent validation, risk appetite governance, escalation, contingency funding and change control.
"""
    path.write_text(text, encoding="utf-8")


def save_metrics(metrics: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
