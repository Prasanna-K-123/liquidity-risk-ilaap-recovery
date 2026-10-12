# ILAAP-style liquidity risk assessment

## Executive conclusion

This repository demonstrates a reproducible **liquidity risk, stress testing, ILAAP-style assessment and recovery-planning framework** on a deterministic synthetic bank balance sheet. The data and behavioral assumptions are illustrative; the project is not a regulatory return and does not claim institution-specific calibration.

## Base balance sheet and liquidity position

- Accounts/facilities: **8,000**
- Total assets: **16,240,910,370**
- Total liabilities: **24,000,125,652**
- HQLA-style post-haircut buffer: **3,679,260,592**
- LCR-style ratio: **1.12x**
- NSFR-style ratio: **1.76x**
- Base survival horizon: **730 days**

## Stress testing

| scenario        |        hqla |   net_30d_outflows |      lcr |   survival_horizon_days |   minimum_post_buffer_liquidity |
|:----------------|------------:|-------------------:|---------:|------------------------:|--------------------------------:|
| base            | 3.67926e+09 |        3.27202e+09 | 1.12446  |                     730 |                     1.81971e+09 |
| idiosyncratic   | 3.36943e+09 |        5.91595e+09 | 0.56955  |                      30 |                    -7.04431e+08 |
| marketwide      | 3.21451e+09 |        4.49725e+09 | 0.714772 |                     730 |                     5.93965e+07 |
| combined_severe | 2.71103e+09 |        8.74539e+09 | 0.309996 |                       1 |                    -5.13752e+09 |

## Risk appetite / limit monitoring

| metric                      |      value |   limit | operator   | status   |
|:----------------------------|-----------:|--------:|:-----------|:---------|
| LCR-style ratio             |   1.12446  |    1    | >=         | PASS     |
| NSFR-style ratio            |   1.76167  |    1    | >=         | PASS     |
| survival horizon days       | 730        |   30    | >=         | PASS     |
| 30d cumulative gap / assets |  -0.114498 |   -0.15 | >=         | PASS     |
| liquidity buffer / assets   |   0.226543 |    0.12 | >=         | PASS     |

## Early-warning indicators

| indicator               |     value |   trigger | trigger_direction   | status   |
|:------------------------|----------:|----------:|:--------------------|:---------|
| base LCR-style          | 1.12446   |      1.1  | low                 | NORMAL   |
| NSFR-style              | 1.76167   |      1.05 | low                 | NORMAL   |
| severe survival days    | 1         |     30    | low                 | TRIGGER  |
| wholesale funding share | 0.0899638 |      0.2  | high                | NORMAL   |
| HQLA / assets           | 0.226543  |      0.12 | low                 | NORMAL   |

## ILAAP-style assessment

- Severe peak liquidity deficit: **5,137,518,601**
- Available recovery capacity: **3,800,000,000**
- Recovery covers peak deficit: **no**
- Reverse-stress deposit runoff multiplier producing a 30-day breach: **1.20x**

## Recovery option waterfall

| action                   |   capacity |   deployed |   post_action_liquidity | target_restored   |
|:-------------------------|-----------:|-----------:|------------------------:|:------------------|
| central_bank_facility    |    1.2e+09 |    1.2e+09 |            -3.93752e+09 | False             |
| secured_funding          |    1e+09   |    1e+09   |            -2.93752e+09 | False             |
| asset_sale               |    8.5e+08 |    8.5e+08 |            -2.08752e+09 | False             |
| deposit_pricing_campaign |    4.5e+08 |    4.5e+08 |            -1.63752e+09 | False             |
| new_unsecured_funding    |    3e+08   |    3e+08   |            -1.33752e+09 | False             |

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
