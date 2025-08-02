# python3.10 alpaca_live_trader/run_live_trading.py

import sys
from pathlib import Path

# Garante que TRADING_STRATEGY/ está no sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from datetime import datetime
import hashlib

import time
from crypto_data_feed import fetch_recent_data
# from signal_engine import generate_signal
from signal_ethereum import generate_signal
from order_executor import send_order, close_position
from stage_manager import load_state, save_state
from send_email import EmailSender
from config_etf import SYMBOL, QTY

email_sender = EmailSender()

def main_loop():
    print("Iniciando loop de trading live...")
    try:
        while True:
            try:
                df = fetch_recent_data()
                state = load_state()
                signal = generate_signal(df, position=state)

                print(f"[SINAL] {signal}")

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
                print(f"Erro: {e}")

            time.sleep(60)

    except KeyboardInterrupt:
        print("\n[INFO] Execução interrompida pelo usuário. Encerrando com segurança...")



def send_trade_email(action: str, reason: str, price: float):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hash_str = hashlib.md5((str(action) + str(price) + now).encode()).hexdigest()[:8]

    subject = f"[AlpacaBot] {action.upper()} @ {price:.2f} | {hash_str}"
    body = (
        f"Ação: {action.upper()}\n"
        f"Preço: {price:.2f}\n"
        f"Motivo: {reason}\n"
        f"Horário: {now}\n"
        f"Hash ID: {hash_str}"
    )

    email_sender.send_email(
        receiver_email="guilistocco@gmail.com",
        subject=subject,
        body=body
    )
    print(f"Email enviado: {subject}")



if __name__ == "__main__":
    main_loop()