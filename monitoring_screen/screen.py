# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus
import plotly.graph_objects as go
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from alpaca_secrets import APCA_API_KEY_ID, APCA_API_SECRET_KEY
# alpaca_client = TradingClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY, paper=True)

# Define o tempo de atualização
REFRESH_INTERVAL_MINUTES = 10

# Usa o session state para manter o controle
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# Calcula tempo desde última atualização
now = datetime.now()
elapsed = now - st.session_state.last_refresh

if elapsed > timedelta(seconds=REFRESH_INTERVAL_MINUTES):
    st.session_state.last_refresh = now
    st.experimental_rerun()

trading_client = TradingClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY, paper=True)

# Função para puxar posição atual
def get_positions():
    return trading_client.get_all_positions()

# Função para calcular exposição ao risco com variação de 1%

def calculate_risk(positions):
    risk_data = []
    for pos in positions:
        symbol = pos.symbol
        qty = float(pos.qty)
        price = float(pos.current_price)
        value = qty * price
        risk = value * -0.01
        risk_data.append({
            'Symbol': symbol,
            'Qty': qty,
            'Price': price,
            'Value': value,
            'Estimated Risk (-1%)': risk
        })
    df = pd.DataFrame(risk_data)
    df = df.sort_values(by='Estimated Risk (-1%)', ascending=True)
    return df

# Função para buscar ordens executadas
def get_filled_orders():
    request = GetOrdersRequest(status="all")
    orders = trading_client.get_orders(filter=request)

    if not orders:
        return None  # ou retornar uma string tipo 'No orders' se quiser

    data = [{
        'Time': o.filled_at,
        'Symbol': o.symbol,
        'Qty': o.filled_qty,
        'Side': o.side,
        'Type': o.order_type,
        'Filled Avg Price': o.filled_avg_price,
    } for o in orders]

    return pd.DataFrame(data).sort_values(by='Time', ascending=False)

# Streamlit layout
st.set_page_config(layout="wide")
st.title("📊 Trading Dashboard - Alpaca")

st.subheader("🔴 Live Position")
positions = get_positions()
pos_df = pd.DataFrame([p.__dict__ for p in positions]
    ).rename(columns={"market_value":"financial_pos",})
st.dataframe(pos_df[["symbol", "qty", "avg_entry_price", "financial_pos", "unrealized_pl"]])

st.subheader("🛡️ Risk Map (-1% move)")
risk_df = calculate_risk(positions)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=risk_df['Symbol'],
    y=risk_df['Estimated Risk (-1%)'],
    text=[f"${r:,.2f}" for r in risk_df['Estimated Risk (-1%)']],
    textposition='outside',
    marker_color='rgb(255,127,14)'
))

fig.update_layout(
    template='plotly_dark',
    title='Exposure to -1% Price Move',
    xaxis_title='Symbol',
    yaxis_title='Estimated Risk (USD)',
    margin=dict(t=50, b=50),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Executed Orders")
orders_df = get_filled_orders()
st.dataframe(orders_df)