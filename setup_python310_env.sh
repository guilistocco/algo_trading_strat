#!/bin/bash

set -e  # para sair no primeiro erro

echo "🚧 Atualizando pacotes..."
sudo apt update -y

echo "🧹 Removendo Python 3.10 (se instalado via apt)..."
sudo apt remove -y python3.10 python3.10-venv python3.10-dev || true

echo "🐍 Instalando Python 3.10..."
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3.10-distutils

echo "📦 Instalando pip para Python 3.10..."
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.10

echo "🧪 Criando ambiente virtual em trading_env..."
cd /home/ubuntu/algo_trading_strat
python3.10 -m venv trading_env

echo "✅ Ativando ambiente e instalando requirements..."
source trading_env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements_trading_env.txt

echo "🎉 Ambiente Python 3.10 criado com sucesso em trading_env"

