from datetime import datetime, timedelta
import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# import sys
# sys.path.append('../alpaca_oms/')  # Adjust path to import from alpaca_oms
from alpaca_oms.alpaca_client import get_data_client
# import alpaca_oms.alpaca_client as alpaca_client
from config import SYMBOL, TIMEFRAME_MINUTES

client = get_data_client()

def fetch_recent_data(limit=100):
    end = datetime.utcnow()
    start = end - timedelta(minutes=limit + 5)

    request = StockBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end,
        adjustment="all",
        feed="iex"
    )
    bars = client.get_stock_bars(request).df
    df = bars[SYMBOL] if isinstance(bars.columns, pd.MultiIndex) else bars
    return df