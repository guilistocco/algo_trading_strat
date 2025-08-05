from datetime import datetime
import smtplib
import pendulum
from email.mime.text import MIMEText
from email_secrets import EMAIL_SENDER, APP_PASSWORD


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

    @staticmethod
    def create_message(receiver_email, subject, body):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "guilherme.mstocco@gmail.com"
        msg["To"] = receiver_email
        return msg

# 05 23 * * * trading_env/bin/python3.10 /Users/guilistocco/Documents/CQF/Trabalho_Final/send_email.py 
# 10 23 * * *  /Users/guilistocco/Documents/CQF/Trabalho_Final/trading_env/bin/python3.10 /Users/guilistocco/Documents/CQF/Trabalho_Final/send_email.py >> /Users/guilistocco/Documents/CQF/Trabalho_Final/logs/email_cron.log 2>&1
