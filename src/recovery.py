from __future__ import annotations

import pandas as pd

from src.config import RECOVERY_ACTIONS


def recovery_waterfall(starting_liquidity: float, target_liquidity: float = 0.0) -> pd.DataFrame:
    rows = []
    liquidity = float(starting_liquidity)
    for action, capacity in RECOVERY_ACTIONS.items():
        needed = max(target_liquidity - liquidity, 0.0)
        deployed = min(capacity, needed) if needed > 0 else 0.0
        liquidity += deployed
        rows.append({"action": action, "capacity": capacity, "deployed": deployed,
                     "post_action_liquidity": liquidity, "target_restored": liquidity >= target_liquidity})
    return pd.DataFrame(rows)


def recovery_capacity() -> float:
    return float(sum(RECOVERY_ACTIONS.values()))
