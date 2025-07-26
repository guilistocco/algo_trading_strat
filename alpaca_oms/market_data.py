# market_data.py

from alpaca.data.requests import StockBarsRequest
from alpaca_secrets import TIMEFRAME
from alpaca_client import get_data_client
from datetime import datetime, timedelta
import pandas as pd


class MarketData:
    def __init__(self):
        self.client = get_data_client()

    def get_bars(self, symbol: str, limit: int = 100):
        end = datetime.utcnow()
        start = end - timedelta(minutes=limit)

        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TIMEFRAME,
            start=start,
            end=end,
            feed="iex"
        )
        bars = self.client.get_stock_bars(request)
        df = bars.df
        if isinstance(df.columns, pd.MultiIndex):
            return df[symbol]
        else:
            return df