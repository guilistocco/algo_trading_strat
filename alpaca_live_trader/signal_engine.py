import talib
import pandas as pd
from config import *

def generate_signal(df: pd.DataFrame, position: dict) -> dict:
    # Verifica se o DataFrame tem dados e colunas esperadas
    required_cols = {'close', 'high', 'low'}

    if df.empty:
        return {"action": "hold", "reason": "df_vazio"}

    if not required_cols.issubset(df.columns):
        return {"action": "hold", "reason": f"colunas ausentes: {required_cols - set(df.columns)}"}

    df = df.copy()

    # Calcula indicadores
    df['ma_short'] = df['close'].rolling(SHORT_WINDOW).mean()
    df['ma_long'] = df['close'].rolling(LONG_WINDOW).mean()
    df['adx'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=T_PERIOD)

    if len(df) < max(SHORT_WINDOW, LONG_WINDOW, T_PERIOD) + 2:
        return {"action": "hold", "reason": "dados_insuficientes"}

    adx = df['adx'].iloc[-1]
    price = df['close'].iloc[-1]

    # Stop loss
    if position.get("side") and position.get("entry_price"):
        entry = position["entry_price"]
        side = position["side"]
        pnl = (price - entry) / entry if side == "long" else (entry - price) / entry

        if pnl < -STOP_LOSS_PCT:
            return {"action": "close", "reason": "stop_loss"}

    if adx < ADX_THRESHOLD:
        return {"action": "hold", "reason": "adx_baixo"}

    cross_up = (
        df['ma_short'].iloc[-1] > df['ma_long'].iloc[-1]
        and df['ma_short'].iloc[-2] <= df['ma_long'].iloc[-2]
    )
    cross_down = (
        df['ma_short'].iloc[-1] < df['ma_long'].iloc[-1]
        and df['ma_short'].iloc[-2] >= df['ma_long'].iloc[-2]
    )

    if cross_up:
        return {"action": "buy", "reason": "cruzamento_para_cima"}
    elif cross_down:
        return {"action": "sell", "reason": "cruzamento_para_baixo"}

    return {"action": "hold", "reason": "nenhum_sinal"}