# order_handler.py

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca_client import get_trading_client

class OrderHandler:
    def __init__(self):
        self.client = get_trading_client()

    def send_market_order(self, symbol: str, qty: int, side: str):
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        order = self.client.submit_order(order_data)
        return order

    def get_order_by_id(self, order_id: str):
        return self.client.get_order_by_id(order_id)

    def list_open_orders(self):
        return self.client.get_orders(status="open")