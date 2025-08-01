from datetime import datetime
import hashlib
from shared.logger_handler import setup_logger
from send_email import EmailSender
email_sender = EmailSender()

logger = setup_logger()


def send_trade_email(action: str, reason: str, price: float, symbol: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hash_str = hashlib.md5((str(action) + str(price) + now).encode()).hexdigest()[:8]

    subject = f"[AlpacaBot] {action.upper()} @ {price:.2f} | {hash_str}"
    body = (
        f"Ação: {action.upper()}\n"
        f"Papel: {symbol.upper()}\n"
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
    logger.info(f"Email enviado: {subject}")