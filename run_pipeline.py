from __future__ import annotations

from pathlib import Path

from src.config import STRESS_SCENARIOS
from src.ewi import build_early_warning_indicators
from src.ilaap import ilaap_assessment, reverse_stress
from src.liquidity import cashflow_ladder, hqla_value, lcr_style, nsfr_style, risk_limits, survival_horizon_days
from src.portfolio import generate_balance_sheet, validate_balance_sheet
from src.recovery import recovery_waterfall
from src.reporting import save_figures, save_metrics, write_report
from src.stress import run_stress_scenarios

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
REPORT = ROOT / "reports" / "generated"


def main() -> None:
    df = generate_balance_sheet()
    validate_balance_sheet(df)

    base_lcr = lcr_style(df)
    nsfr = nsfr_style(df)
    base_ladder = cashflow_ladder(df)
    base_survival = survival_horizon_days(base_ladder)
    stresses = run_stress_scenarios(df)

    severe_cfg = STRESS_SCENARIOS["combined_severe"]
    severe_ladder = cashflow_ladder(df, severe_cfg["deposit_multiplier"], severe_cfg["draw_multiplier"],
                                    severe_cfg["wholesale_rollover"], severe_cfg["haircut_add"])
    limits = risk_limits(df, base_lcr["lcr"], nsfr["nsfr"], base_ladder)

    total_assets = float(df.loc[df["is_asset"], "amount"].sum())
    total_liabilities = float(df.loc[df["is_liability"], "amount"].sum())
    wholesale = float(df.loc[df["product"] == "wholesale_unsecured", "amount"].sum())
    wholesale_share = wholesale / total_liabilities
    hqla_ratio = hqla_value(df) / total_assets
    ewi = build_early_warning_indicators(stresses, base_lcr["lcr"], nsfr["nsfr"], wholesale_share, hqla_ratio)

    ilaap = ilaap_assessment(base_lcr["lcr"], nsfr["nsfr"], stresses, severe_ladder)
    rev = reverse_stress(df, cashflow_ladder)
    recovery = recovery_waterfall(-ilaap["severe_peak_liquidity_deficit"])

    metrics = {
        "portfolio": {"accounts": int(len(df)), "total_assets": total_assets, "total_liabilities": total_liabilities,
                      "off_balance_commitments": float(df.loc[df["is_off_balance"], "amount"].sum()),
                      "wholesale_funding_share": wholesale_share},
        "base": {"hqla": float(base_lcr["hqla"]), "gross_30d_outflows": float(base_lcr["gross_30d_outflows"]),
                 "net_30d_outflows": float(base_lcr["net_30d_outflows"]), "lcr": float(base_lcr["lcr"]),
                 "nsfr": float(nsfr["nsfr"]), "survival_horizon_days": int(base_survival),
                 "hqla_to_assets": hqla_ratio},
        "ilaap": ilaap,
        "reverse_stress": rev,
        "limit_breaches": int((limits["status"] == "BREACH").sum()),
        "ewi_triggers": int((ewi["status"] == "TRIGGER").sum()),
        "methodology_flags": {"balance_sheet_data": "synthetic illustrative",
                              "behavioral_assumptions": "illustrative",
                              "lcr_nsfr_status": "simplified analytical analogues; not regulatory reporting",
                              "stress_scenarios": "illustrative", "recovery_capacities": "illustrative"},
    }

    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "synthetic_balance_sheet.csv", index=False)
    base_ladder.to_csv(OUT / "base_cashflow_ladder.csv", index=False)
    severe_ladder.to_csv(OUT / "severe_cashflow_ladder.csv", index=False)
    stresses.to_csv(OUT / "stress_summary.csv", index=False)
    limits.to_csv(OUT / "limit_monitoring.csv", index=False)
    ewi.to_csv(OUT / "early_warning_indicators.csv", index=False)
    recovery.to_csv(OUT / "recovery_waterfall.csv", index=False)
    save_metrics(metrics, OUT / "metrics.json")
    save_figures(base_ladder, stresses, REPORT)
    write_report(metrics, stresses, limits, ewi, recovery, REPORT / "ilaap_assessment.md")


if __name__ == "__main__":
    main()
