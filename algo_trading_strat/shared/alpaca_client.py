from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca_secrets import APCA_API_KEY_ID, APCA_API_SECRET_KEY

def get_trading_client(paper=True) -> TradingClient:
    return TradingClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY, paper=paper)

def get_data_client() -> StockHistoricalDataClient:
    return StockHistoricalDataClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

def get_crypto_data_client() -> CryptoHistoricalDataClient:
    return CryptoHistoricalDataClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)