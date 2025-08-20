from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from shared.alpaca_client import get_trading_client
from shared.logger_handler import setup_logger

trading_client = get_trading_client()
logger = setup_logger()

def send_order(action: str, symbol:str, quantity:int):
    if action not in ["buy", "sell"]:
        return

    order_data = MarketOrderRequest(
        symbol=symbol,
        qty=quantity,
        side=OrderSide.BUY if action == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.GTC
    )
    order = trading_client.submit_order(order_data)
    logger.info(f"Order Sent: {order.id} ({action.upper()})")
    return order

def close_position(SYMBOL:str):
    try:
        trading_client.close_position(SYMBOL.replace("/",""))
        logger.info("Position closed.")
    except Exception as e:
        logger.info(f"No position to close: {e}")