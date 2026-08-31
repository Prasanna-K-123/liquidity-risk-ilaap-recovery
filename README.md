# Liquidity Risk, ILAAP & Recovery Planning

A reproducible **liquidity-risk and treasury analytics platform** covering cash-flow ladders, LCR/NSFR-style metrics, liquidity-buffer haircuts, survival horizons, idiosyncratic/marketwide/combined stress testing, reverse stress, early-warning indicators, risk limits and an ILAAP-style recovery assessment.

The project uses a deterministic **synthetic bank balance sheet** so the implementation is auditable without pretending that confidential institution data are public. Behavioral/runoff assumptions and recovery capacities are explicitly illustrative.

## Verified reproducible evidence

The current green GitHub Actions pipeline generates the following results from the deterministic synthetic balance sheet:

- **8,000 accounts**, total modeled assets **USD 16.24bn** and off-balance commitments **USD 2.58bn**;
- base **LCR-style ratio 3.97x**, **NSFR-style ratio 1.76x** and modeled survival horizon **730 days**;
- combined-severe stress reduces the LCR-style ratio to **0.69x**, shortens modeled survival to **30 days**, and produces a **USD 2.45bn** peak liquidity deficit;
- modeled recovery capacity is **USD 3.80bn**, covering the severe peak deficit and leaving approximately **USD 1.35bn** after full modeled recovery actions;
- reverse stress reaches the 30-day liquidity-breach boundary at a **2.70x deposit-run multiplier** under the project's stated assumptions;
- the final run produces **1 early-warning trigger** and **0 illustrative limit breaches** under the defined risk-appetite thresholds.

These are **synthetic/illustrative model outputs**, not observed bank positions or regulatory ratios. The LCR, NSFR and ILAAP labels in this project are analytical analogues, not regulatory submissions or compliance claims. See `outputs/metrics.json` and `reports/generated/ilaap_assessment.md`.

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
