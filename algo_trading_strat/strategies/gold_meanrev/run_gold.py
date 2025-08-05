from shared.logger_handler import setup_logger
import time
# from crypto_data_feed import fetch_recent_data
from data_feed import fetch_recent_data
from signal_gold import generate_signal
from shared.order_executor import send_order, close_position
from position_manager import load_state, save_state
from config_gold import SYMBOL, QTY

logger = setup_logger()

def main_loop():
    logger.info("Iniciando loop de trading live...")
    try:
        while True:
            try:
                df = fetch_recent_data()
                state = load_state()
                signal = generate_signal(df, position=state)

                logger.info(f"[SINAL] {signal}")

                if signal["action"] == "buy":
                    send_order("buy", SYMBOL, QTY)
                    state = {"side": "long", "entry_price": df['close'].iloc[-1]}
                    
                elif signal["action"] == "sell":
                    send_order("sell", SYMBOL, QTY)
                    state = {"side": "short", "entry_price": df['close'].iloc[-1]}
                elif signal["action"] == "close":
                    close_position()
                    state = {}

                if signal["action"] in ["buy", "sell", "close"]:
                    send_trade_email(signal["action"], signal["reason"], df['close'].iloc[-1])

                save_state(state)
            except Exception as e:
                logger.exception(f"Erro: {e}")

            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("\n[INFO] Execução interrompida pelo usuário. Encerrando com segurança...")

if __name__ == "__main__":
    main_loop()