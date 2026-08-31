from __future__ import annotations

RANDOM_STATE = 20260831
N_ACCOUNTS = 8000

TIME_BUCKETS = ("overnight", "2d-7d", "8d-30d", "31d-90d", "91d-1y", ">1y")
BUCKET_DAYS = {"overnight": 1, "2d-7d": 7, "8d-30d": 30, "31d-90d": 90, "91d-1y": 365, ">1y": 730}

BASE_RUNOFF = {
    "retail_stable": 0.05,
    "retail_less_stable": 0.10,
    "corporate_operational": 0.25,
    "corporate_non_operational": 0.40,
    "wholesale_unsecured": 0.60,
}

STRESS_SCENARIOS = {
    "base": {"deposit_multiplier": 1.00, "draw_multiplier": 1.00, "haircut_add": 0.00, "wholesale_rollover": 0.85},
    "idiosyncratic": {"deposit_multiplier": 1.55, "draw_multiplier": 1.35, "haircut_add": 0.08, "wholesale_rollover": 0.45},
    "marketwide": {"deposit_multiplier": 1.25, "draw_multiplier": 1.25, "haircut_add": 0.12, "wholesale_rollover": 0.55},
    "combined_severe": {"deposit_multiplier": 2.30, "draw_multiplier": 2.00, "haircut_add": 0.25, "wholesale_rollover": 0.10},
}

RECOVERY_ACTIONS = {
    "central_bank_facility": 1_200_000_000.0,
    "secured_funding": 1_000_000_000.0,
    "asset_sale": 850_000_000.0,
    "deposit_pricing_campaign": 450_000_000.0,
    "new_unsecured_funding": 300_000_000.0,
}

LIMITS = {
    "minimum_lcr": 1.00,
    "minimum_nsfr": 1.00,
    "minimum_survival_days": 30,
    "maximum_30d_cumulative_gap_ratio": -0.15,
    "minimum_liquidity_buffer_ratio": 0.12,
}
