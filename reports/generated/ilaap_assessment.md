# ILAAP-style liquidity risk assessment

## Executive conclusion

This repository demonstrates a reproducible **liquidity risk, stress testing, ILAAP-style assessment and recovery-planning framework** on a deterministic synthetic bank balance sheet. The data and behavioral assumptions are illustrative; the project is not a regulatory return and does not claim institution-specific calibration.

## Base balance sheet and liquidity position

- Accounts/facilities: **8,000**
- Total assets: **16,240,910,370**
- Total liabilities: **24,000,125,652**
- HQLA-style post-haircut buffer: **9,460,086,240**
- LCR-style ratio: **3.97x**
- NSFR-style ratio: **1.76x**
- Base survival horizon: **730 days**

## Stress testing

| scenario        |        hqla |   net_30d_outflows |      lcr |   survival_horizon_days |   minimum_post_buffer_liquidity |
|:----------------|------------:|-------------------:|---------:|------------------------:|--------------------------------:|
| base            | 9.46009e+09 |        2.38567e+09 | 3.96537  |                     730 |                     7.60053e+09 |
| idiosyncratic   | 8.16081e+09 |        5.02961e+09 | 1.62256  |                     730 |                     4.08695e+09 |
| marketwide      | 7.51118e+09 |        3.61091e+09 | 2.08013  |                     730 |                     4.35606e+09 |
| combined_severe | 5.39986e+09 |        7.85905e+09 | 0.687088 |                      30 |                    -2.44869e+09 |

## Risk appetite / limit monitoring

| metric                      |      value |   limit | operator   | status   |
|:----------------------------|-----------:|--------:|:-----------|:---------|
| LCR-style ratio             |   3.96537  |    1    | >=         | PASS     |
| NSFR-style ratio            |   1.76167  |    1    | >=         | PASS     |
| survival horizon days       | 730        |   30    | >=         | PASS     |
| 30d cumulative gap / assets |  -0.114498 |   -0.15 | >=         | PASS     |
| liquidity buffer / assets   |   0.582485 |    0.12 | >=         | PASS     |

## Early-warning indicators

| indicator               |      value |   trigger | trigger_direction   | status   |
|:------------------------|-----------:|----------:|:--------------------|:---------|
| base LCR-style          |  3.96537   |      1.1  | low                 | NORMAL   |
| NSFR-style              |  1.76167   |      1.05 | low                 | NORMAL   |
| severe survival days    | 30         |     30    | low                 | TRIGGER  |
| wholesale funding share |  0.0899638 |      0.2  | high                | NORMAL   |
| HQLA / assets           |  0.582485  |      0.12 | low                 | NORMAL   |

## ILAAP-style assessment

- Severe peak liquidity deficit: **2,448,694,074**
- Available recovery capacity: **3,800,000,000**
- Recovery covers peak deficit: **yes**
- Reverse-stress deposit runoff multiplier producing a 30-day breach: **2.70x**

## Recovery option waterfall

| action                   |   capacity |    deployed |   post_action_liquidity | target_restored   |
|:-------------------------|-----------:|------------:|------------------------:|:------------------|
| central_bank_facility    |    1.2e+09 | 1.2e+09     |            -1.24869e+09 | False             |
| secured_funding          |    1e+09   | 1e+09       |            -2.48694e+08 | False             |
| asset_sale               |    8.5e+08 | 2.48694e+08 |             0           | True              |
| deposit_pricing_campaign |    4.5e+08 | 0           |             0           | True              |
| new_unsecured_funding    |    3e+08   | 0           |             0           | True              |

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
