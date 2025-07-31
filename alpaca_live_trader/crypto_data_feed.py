from datetime import datetime, timedelta
import pandas as pd
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

from alpaca_oms.alpaca_client import get_crypto_data_client
from config_etf import SYMBOL, TIMEFRAME_MINUTES

client = get_crypto_data_client()

def fetch_recent_data(limit=100):
    end = datetime.utcnow()
    start = end - timedelta(minutes=limit + 5)

    request = CryptoBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end,
        adjustment="all",
        feed="iex"
    )
    bars = client.get_crypto_bars(request).df
    df = bars[SYMBOL] if isinstance(bars.columns, pd.MultiIndex) else bars
    return df