# Liquidity Risk, ILAAP & Recovery Planning

A reproducible **liquidity-risk and treasury analytics platform** covering cash-flow ladders, LCR/NSFR-style metrics, liquidity-buffer haircuts, survival horizons, idiosyncratic/marketwide/combined stress testing, reverse stress, early-warning indicators, risk limits and an ILAAP-style recovery assessment.

The project uses a deterministic **synthetic bank balance sheet** so the implementation is auditable without pretending that confidential institution data are public. Behavioral/runoff assumptions and recovery capacities are explicitly illustrative.

## What this repository demonstrates

| Layer | Implementation |
|---|---|
| Balance-sheet controls | 8,000-account synthetic assets, deposits, wholesale funding and committed facilities |
| Cash-flow ladder | overnight through >1y contractual/behavioral maturity buckets |
| Liquidity buffer | product-level asset haircuts and post-haircut liquidity value |
| LCR-style | 30-day stressed outflows, inflow cap and liquid-asset coverage ratio |
| NSFR-style | explicit illustrative ASF/RSF weighting and structural funding ratio |
| Stress testing | base, idiosyncratic, marketwide and combined-severe runoff/draw/haircut/rollover shocks |
| Survival horizon | first horizon at which cumulative liquidity resources are depleted |
| Reverse stress | searches for the deposit-run severity that causes a 30-day liquidity breach |
| Risk appetite | LCR/NSFR, survival, 30-day gap and liquidity-buffer limits |
| EWI framework | ratio, survival, wholesale-funding and buffer triggers |
| Recovery planning | capacity-constrained central-bank, secured-funding, asset-sale and funding actions |
| ILAAP framing | base adequacy + severe deficit + recovery capacity + governance limitations |
| Reproducibility | unit tests, GitHub Actions, generated metrics, figures and risk-committee-style report |

## Why this is high-signal for FSRM

Liquidity risk work is not just a ratio calculation. A credible implementation must connect balance-sheet structure, behavioral cash flows, funding concentration, liquid-asset monetisation, severe-but-plausible stress, survival, risk appetite, escalation and feasible recovery actions. This repository demonstrates that end-to-end control chain while keeping every assumption visible.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_pipeline.py
```

The pipeline generates `outputs/metrics.json`, cash-flow ladders, stress/limit/EWI tables, a recovery waterfall, figures and `reports/generated/ilaap_assessment.md`.

## Evidence standard

No bank data or regulatory compliance claim is made. Synthetic inputs are used to demonstrate the methodology. Resume bullets should quote only generated outputs and must preserve the words **synthetic**, **illustrative**, **LCR/NSFR-style** and **ILAAP-style** where relevant.
