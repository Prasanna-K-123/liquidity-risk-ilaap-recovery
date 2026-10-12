# Liquidity Risk, ILAAP & Recovery Planning

A reproducible **liquidity-risk and treasury analytics platform** covering cash-flow ladders, LCR/NSFR-style metrics, liquidity-buffer haircuts, survival horizons, idiosyncratic/marketwide/combined stress testing, reverse stress, early-warning indicators, risk limits and an ILAAP-style recovery assessment.

The project uses a deterministic **synthetic bank balance sheet** so the implementation is auditable without pretending that confidential institution data are public. Behavioral/runoff assumptions and recovery capacities are explicitly illustrative.

## Verified reproducible evidence

The current green GitHub Actions pipeline generates the following results from the deterministic synthetic balance sheet:

- **8,000 synthetic account records**, modeled assets **USD 16.24bn**, modeled liabilities **USD 24.00bn**, and off-balance commitments **USD 2.58bn**; this is **not an equity-reconciled bank balance sheet**;
- corrected disjoint opening HQLA **USD 3.679bn** (treasury_hqla only); base **LCR-style ratio 1.124x**, **NSFR-style ratio 1.762x** and modeled base survival horizon **730 days**;
- combined-severe illustrative stress reduces LCR-style ratio to **0.310x**, shortens the modeled survival horizon to **1 day**, and produces a **USD 5.138bn** peak liquidity deficit;
- modeled recovery capacity remains **USD 3.80bn** and is **INSUFFICIENT** against the severe peak deficit, leaving about **USD 1.338bn uncovered** after every modeled recovery action;
- reverse stress reaches the modeled 30-day liquidity-breach boundary at approximately a **1.20x deposit-run multiplier** under the project's stated assumptions;
- the final run produces **1 early-warning trigger** and **0 illustrative limit breaches** under the defined risk-appetite thresholds.

These are **synthetic/illustrative model outputs**, not observed bank positions or regulatory ratios.

**Accounting correction (12 October 2026):** The previous version incorrectly counted non-treasury loans in the opening liquid-asset buffer and allowed treasury assets to appear again as 30-day maturity inflows. The corrected code counts only `treasury_hqla` in starting HQLA and excludes those same securities from 30-day inflows. The previous public figures (**9.460bn** HQLA, **3.97x** base LCR, **0.69x** severe LCR, **2.45bn** severe deficit, **2.70x** reverse-stress multiplier and a falsely sufficient recovery waterfall) are superseded, remain recoverable from earlier source commits, and must **not** be copied into a current résumé or risk report. [Corrected disjoint-accounting PR and controls](https://github.com/Prasanna-K-123/liquidity-risk-ilaap-recovery/pull/1) · [Matching synthetic-pipeline run](https://github.com/Prasanna-K-123/liquidity-risk-ilaap-recovery/actions/runs/38287063600). The corrected results reproduce the same fixed synthetic accounts and stated assumptions; no bank liquidity regulation, equity-funded balance-sheet identity or real-world recovery is validated. The LCR, NSFR and ILAAP labels in this project are analytical analogues, not regulatory submissions or compliance claims. See `outputs/metrics.json` and `reports/generated/ilaap_assessment.md`.

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

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest
python run_pipeline.py
```

The pipeline generates `outputs/metrics.json`, cash-flow ladders, stress/limit/EWI tables, a recovery waterfall, figures and `reports/generated/ilaap_assessment.md`.

## Evidence standard

No bank data or regulatory compliance claim is made. Synthetic inputs are used to demonstrate the methodology. Resume bullets should quote only generated outputs and must preserve the words **synthetic**, **illustrative**, **LCR/NSFR-style** and **ILAAP-style** where relevant.
