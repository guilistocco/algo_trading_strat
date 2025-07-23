from send_email import EmailSender
from datetime import datetime
import pandas as pd
import hashlib
import random

# Cria um DataFrame fictício
df = pd.DataFrame({
    'nome': ['Alice', 'Bob', 'Carol'],
    'valor': [random.randint(1, 100) for _ in range(3)],
    'data': [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(3)]
})

# Gera um hash único para o envio
hash_input = df.to_string() + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
hash_str = hashlib.md5(hash_input.encode()).hexdigest()[:8]  # 8 caracteres

# Monta o corpo do e-mail com a tabela
body = (
    f"Este é um e-mail de teste simples.\n"
    f"Funciona!\n"
    f"Hora do envio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
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
