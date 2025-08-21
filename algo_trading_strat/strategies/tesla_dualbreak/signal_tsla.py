import pandas as pd
import pandas_ta as ta
from config_tsla import *


def generate_signal(df: pd.DataFrame, position: dict) -> dict:
    required_cols = {'close'}
    if df.empty or not required_cols.issubset(df.columns):
        return {"action": "hold", "reason": "empty_or_incomplete_df"}

    if len(df) < BREAKOUT_WINDOW + 1:
        return {"action": "hold", "reason": "incomplete_indicators"}

    df = df.copy()
    df['high_breakout'] = df['close'].rolling(BREAKOUT_WINDOW).max()
    df['low_breakout'] = df['close'].rolling(BREAKOUT_WINDOW).min()
    df['high_exit'] = df['close'].rolling(EXIT_WINDOW).max()
    df['low_exit'] = df['close'].rolling(EXIT_WINDOW).min()

    close = df['close'].iloc[-1]
    high_breakout = df['high_breakout'].iloc[-1]
    low_breakout = df['low_breakout'].iloc[-1]
    high_exit = df['high_exit'].iloc[-1]
    low_exit = df['low_exit'].iloc[-1]

    # === EXIT CONDITIONS ===
    if position.get("side") == "long" and close <= low_exit:
        return {"action": "close", "reason": "long_exit_break"}
    elif position.get("side") == "short" and close >= high_exit:
        return {"action": "close", "reason": "short_exit_break"}

    # === ENTRY CONDITIONS ===
    if not position.get("side"):
        if close >= high_breakout:
            return {"action": "buy", "reason": "breakout_up"}
        elif close <= low_breakout:
            return {"action": "sell", "reason": "breakout_down"}

    return {"action": "hold", "reason": "no_conditions"}