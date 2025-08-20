from datetime import datetime
import hashlib
import smtplib
import pendulum
from email.mime.text import MIMEText
from shared.logger_handler import setup_logger
from shared.email_secrets import EMAIL_SENDER, APP_PASSWORD

logger = setup_logger()
# [2025-08-06 11:43:02,541] [ERROR] Error: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
class EmailSender:
    def __init__(self):
        self.sender_email = EMAIL_SENDER
        self.app_password = APP_PASSWORD

    def send_email(self, receiver_email, subject, body):
        if self.sender_email != "guilherme.mstocco@gmail.com":
            raise ValueError("A senha só funciona com o email guilherme.mstocco@gmail.com")
        msg = self.create_message(receiver_email, subject, body)
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, receiver_email, msg.as_string())
                now = pendulum.now("America/Sao_Paulo")
                now_str = now.format("YYYY-MM-DD HH:mm:ss")
            print("✅ Email enviado com sucesso. " + now_str)
        except Exception as e:
            print("❌ Falha ao enviar email:")
            print(e)

    def send_trade_email(self, action: str, reason: str, price: float):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hash_str = hashlib.md5((str(action) + str(price) + now).encode()).hexdigest()[:8]

        subject = f"[AlpacaBot] {action.upper()} @ {price:.2f} | {hash_str}"
        body = (
            f"Action: {action.upper()}\n"
            f"Price: {price:.2f}\n"
            f"Trading_Reason: {reason}\n"
            f"Timestamp: {now}\n"
            f"Hash ID: {hash_str}"
        )

        self.send_email(
            receiver_email="guilistocco@gmail.com",
            subject=subject,
            body=body
        )
        print(f"Email sent: {subject}")

    @staticmethod
    def create_message(receiver_email, subject, body):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "guilherme.mstocco@gmail.com"
        msg["To"] = receiver_email
        return msg


    
