from datetime import datetime, timedelta
import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from shared.alpaca_client import get_data_client

client = get_data_client()

def fetch_recent_data(symbol, limit=400):
    end = datetime.utcnow()
    start = end - timedelta(minutes=limit + 5)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end,
        adjustment="all",
        feed="iex"
    )
    bars = client.get_stock_bars(request).df
    df = bars[symbol] if isinstance(bars.columns, pd.MultiIndex) else bars
    return df