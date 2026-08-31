# Methodology

This project is a liquidity-risk architecture demonstration, not a regulatory return.

The engine creates a deterministic synthetic balance sheet with assets, deposits, wholesale funding and committed facilities. It then builds contractual/behavioral cash-flow ladders, applies transparent product-level runoff and drawdown assumptions, haircuts liquid assets, computes simplified LCR- and NSFR-style ratios, estimates survival horizons, tests risk-appetite limits, runs idiosyncratic/marketwide/combined stress scenarios, performs reverse stress testing and evaluates a recovery-action waterfall.

The LCR-style calculation uses post-haircut liquid assets divided by 30-day net stressed outflows, with a simplified 75% inflow cap. The NSFR-style calculation uses explicit illustrative ASF/RSF weights. These are analytical analogues only; they are not jurisdiction-specific Basel regulatory calculations.
