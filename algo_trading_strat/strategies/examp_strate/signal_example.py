import pandas as pd
from config_example import SHORT_WINDOW, LONG_WINDOW, BUFFER_PCT


def generate_signal(df: pd.DataFrame, position: dict) -> dict:
    required_cols = {'close'}

    if df.empty or not required_cols.issubset(df.columns):
        return {"action": "hold", "reason": "empty_or_incomplete_df"}

    df = df.copy()

    # Moving average calculation
    df['ma_short'] = df['close'].rolling(SHORT_WINDOW).mean()
    df['ma_long'] = df['close'].rolling(LONG_WINDOW).mean()

    df.dropna(inplace=True)

    # Indicator completeness check
    if df[['ma_short', 'ma_long']].isna().any().any() or len(df) < max(SHORT_WINDOW, LONG_WINDOW) + 2:
        return {"action": "hold", "reason": "incomplete_indicators"}

    # Latest values
    price = df['close'].iloc[-1]
    ma_short = df['ma_short'].iloc[-1]
    ma_long = df['ma_long'].iloc[-1]
    prev_ma_short = df['ma_short'].iloc[-2]
    prev_ma_long = df['ma_long'].iloc[-2]

    diff = ma_short - ma_long
    buffer = BUFFER_PCT * price
    
    cross_up = prev_ma_short <= prev_ma_long and ma_short > ma_long and diff > buffer
    cross_down = prev_ma_short >= prev_ma_long and ma_short < ma_long and abs(diff) > buffer

    reverse_cross_up = prev_ma_short <= prev_ma_long and ma_short > ma_long
    reverse_cross_down = prev_ma_short >= prev_ma_long and ma_short < ma_long

    # === ENTRY ===
    if not position.get("side"):
        if cross_up:
            return {"action": "buy", "reason": "cross_up + buffer"}
        elif cross_down:
            return {"action": "sell", "reason": "cross_down + buffer"}

    # === EXIT ===
    if position.get("side") == "long" and reverse_cross_down:
        return {"action": "close", "reason": "reverse_cross_down"}
    elif position.get("side") == "short" and reverse_cross_up:
        return {"action": "close", "reason": "reverse_cross_up"}

    return {"action": "hold", "reason": "no_condition"}
