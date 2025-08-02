import pandas as pd
import pandas_ta as ta
from config_etf import *
from pprint import pprint



def generate_signal(df: pd.DataFrame, position: dict) -> dict:
    required_cols = {'close', 'high', 'low'}

    if df.empty or not required_cols.issubset(df.columns):
        return {"action": "hold", "reason": "df_vazio_ou_incompleto"}

    df = df.copy()

    # Indicadores com pandas_ta
    df['ma_short'] = df['close'].rolling(SHORT_WINDOW).mean()
    df['ma_long'] = df['close'].rolling(LONG_WINDOW).mean()
    df['adx'] = ta.adx(high=df['high'], low=df['low'], close=df['close'], length=T_PERIOD)['ADX_14']
    df.dropna(how="any", inplace=True)

    if df[['ma_short', 'ma_long', 'adx']].isna().any().any() or len(df) < max(SHORT_WINDOW, LONG_WINDOW, T_PERIOD) + 2:
        return {"action": "hold", "reason": "indicadores_incompletos"}

    # Extração dos últimos valores
    price = df['close'].iloc[-1]
    ma_short = df['ma_short'].iloc[-1]
    ma_long = df['ma_long'].iloc[-1]
    prev_ma_short = df['ma_short'].iloc[-2]
    prev_ma_long = df['ma_long'].iloc[-2]
    adx = df['adx'].iloc[-1]
    diff = ma_short - ma_long
    buffer = BUFFER_PCT * price

    # === STOP LOSS ===
    if position.get("side") and position.get("entry_price"):
        entry = position["entry_price"]
        side = position["side"]
        pnl = (price - entry) / entry if side == "long" else (entry - price) / entry

        if pnl < -STOP_LOSS_PCT:
            return {"action": "close", "reason": "stop_loss"}

    # === Entradas com buffer + ADX ===
    cross_up = diff > buffer and prev_ma_short <= prev_ma_long
    cross_down = diff < -buffer and prev_ma_short >= prev_ma_long
    reverse_cross_up = cross_up
    reverse_cross_down = cross_down

    # ENTRADA
    if not position.get("side"):
        if cross_up and adx > ADX_THRESHOLD:
            return {"action": "buy", "reason": "cross_up + adx"}
        elif cross_down and adx > ADX_THRESHOLD:
            return {"action": "sell", "reason": "cross_down + adx"}

    # SAÍDA
    else:
        if position["side"] == "long" and reverse_cross_down:
            return {"action": "close", "reason": "reverse_cross_down"}
        elif position["side"] == "short" and reverse_cross_up:
            return {"action": "close", "reason": "reverse_cross_up"}

    return {"action": "hold", "reason": "nenhuma_condição"}