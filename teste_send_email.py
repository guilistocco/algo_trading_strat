from send_email import EmailSender
import pandas as pd
import hashlib
import random
import pendulum  # <-- usando pendulum

# Define horário fixo em São Paulo (GMT-3, com ajuste automático de verão)
now = pendulum.now("America/Sao_Paulo")
now_str = now.format("YYYY-MM-DD HH:mm:ss")

# Cria um DataFrame fictício
df = pd.DataFrame({
    'nome': ['Alice', 'Bob', 'Carol'],
    'valor': [random.randint(1, 100) for _ in range(3)],
    'data': [now_str for _ in range(3)]
})

# Gera um hash único para o envio
hash_input = df.to_string() + now_str
hash_str = hashlib.md5(hash_input.encode()).hexdigest()[:8]

# Monta o corpo do e-mail com a tabela
body = (
    f"Este é um e-mail de teste simples.\n"
    f"Funciona!\n"
    f"Hora do envio: {now_str}\n"
    f"Hash: {hash_str}\n\n"
    f"Tabela de dados:\n"
    f"{df.to_string(index=False)}"
)

EmailSender_ = EmailSender()
EmailSender_.send_email(
    receiver_email="guilistocco@gmail.com",
    subject=f"Teste direto com smtplib - {hash_str}",
    body=body
)