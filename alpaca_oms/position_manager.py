# position_manager.py

from alpaca_client import get_trading_client

class PositionManager:
    def __init__(self):
        self.client = get_trading_client()

    def get_position(self, symbol: str):
        try:
            return self.client.get_open_position(symbol)
        except Exception:
            return None

    def list_all_positions(self):
        return self.client.get_all_positions()

    def close_position(self, symbol: str):
        return self.client.close_position(symbol)