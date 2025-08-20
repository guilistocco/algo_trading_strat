import pandas as pd
import pandas_ta as ta
from config_iau import *


def generate_signal_zscore_stoploss(df: pd.DataFrame, position: dict) -> dict:
    if df.empty or "close" not in df.columns:
        return {"action": "hold", "reason": "empty_or_missing_data"}

    if len(df) < WINDOW + 2:
        return {"action": "hold", "reason": "insufficient_data"}

    df = df.copy()
    df['ma'] = df['close'].rolling(WINDOW).mean()
    df['std'] = df['close'].rolling(WINDOW).std()
    df['z'] = (df['close'] - df['ma']) / df['std']

    z = df['z'].iloc[-1]
    price = df['close'].iloc[-1]

    # ENTRY
    if not position.get("side"):
        if z < -THRESHOLD:
            return {
                "action": "buy",
                "reason": "z_below_negative_threshold",
                "entry_price": price
            }
        elif z > THRESHOLD:
            return {
                "action": "sell",
                "reason": "z_above_positive_threshold",
                "entry_price": price
            }

    # EXIT (mean reversion or stop loss)
    elif position.get("side") and position.get("entry_price"):
        entry = position["entry_price"]
        side = position["side"]
        stop_hit = False

        if side == "long":
            stop_price = entry * (1 - STOP_LOSS_PCT)
            if price <= stop_price:
                stop_hit = True
            elif z > 0:
                return {"action": "close", "reason": "z_crossed_above_zero"}

        elif side == "short":
            stop_price = entry * (1 + STOP_LOSS_PCT)
            if price >= stop_price:
                stop_hit = True
            elif z < 0:
                return {"action": "close", "reason": "z_crossed_below_zero"}

        if stop_hit:
            return {"action": "close", "reason": "stop_loss_triggered"}

    return {"action": "hold", "reason": "no_conditions_met"}