from shared.logger_handler import setup_logger
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append("/app")

import time
# from crypto_data_feed import fetch_recent_data
from shared.data_feed import fetch_recent_data
from signal_iau import generate_signal
from shared.order_executor import send_order, close_position
from shared.email_handler import EmailSender
from shared.stage_manager import load_state, save_state
from config_iau import SYMBOL, QTY

logger = setup_logger()

def main_loop():
    logger.info("Starting live trading loop...")
    email_obj = EmailSender()

    try:
        while True:
            try:
                df = fetch_recent_data(symbol=SYMBOL)
                state = load_state()
                signal = generate_signal(df, position=state)

                logger.info(f"[SIGNAL] {signal}")

                if signal["action"] == "buy":
                    send_order("buy", SYMBOL, QTY)
                    logger.info(f"[ORDER] Buy order sent for {SYMBOL} at {df['close'].iloc[-1]}")
                    state = {"side": "long", "entry_price": df['close'].iloc[-1]}
                    
                elif signal["action"] == "sell":
                    send_order("sell", SYMBOL, QTY)
                    logger.info(f"[ORDER] Sell order sent for {SYMBOL} at {df['close'].iloc[-1]}")
                    state = {"side": "short", "entry_price": df['close'].iloc[-1]}
                elif signal["action"] == "close":
                    logger.info(f"[ORDER] Closing position for {SYMBOL}")
                    close_position(SYMBOL)
                    state = {}

                if signal["action"] in ["buy", "sell", "close"]:
                    logger.info(f"[EMAIL] Sending trade email for {signal['action']}...")
                    email_obj.send_trade_email(signal["action"], signal["reason"], df['close'].iloc[-1])

                save_state(state)
            except Exception as e:
                logger.exception(f"Erro: {e}")

            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("\n[INFO] Execution interrupted by user. Shutting down safely...")

if __name__ == "__main__":
    main_loop()