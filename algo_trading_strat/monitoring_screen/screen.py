# dashboard.py
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.models import Position
from alpaca.data.timeframe import TimeFrame
import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from alpaca_secrets import APCA_API_KEY_ID, APCA_API_SECRET_KEY

# Define o tempo de atualização
REFRESH_INTERVAL_MINUTES = 3


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

def get_account_pnl():
    account = trading_client.get_account()
    return float(account.equity) #- float(account.last_equity)

# Função para puxar posição atual
def get_positions():
    return trading_client.get_all_positions()

def get_exposure(positions):
    data = []
    for pos in positions:
        symbol = pos.symbol
        qty = float(pos.qty)
        price = float(pos.current_price)
        value = qty * price
        data.append({'Symbol': symbol, 'Exposure': value})
    df = pd.DataFrame(data).sort_values(by='Exposure', ascending=False)
    return df

def plot_return_histogram(symbol: str, qty: float):
    now = datetime.now(pytz.UTC)
    start = now - timedelta(minutes=500)

    is_crypto = symbol.endswith("USD")  # crude check

    if is_crypto:
        client = CryptoHistoricalDataClient()
        request = CryptoBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=now,
            adjustment="all",
            feed="iex"
        )
        bars = client.get_crypto_bars(request).df
    else:
        client = StockHistoricalDataClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=now,
            adjustment="all",
            feed="iex"
        )
        bars = client.get_stock_bars(request).df

    bars.reset_index(inplace=True)

    if bars.empty or symbol not in bars['symbol'].values:
        return None

    bars = bars[bars['symbol'] == symbol]
    bars['return'] = np.log(bars['close'] / bars['close'].shift(1)) * 100  # Convert to percentage
    bars.dropna(inplace=True)

    returns = bars['return']
    mean = returns.mean()
    std = returns.std()
    var_1 = np.percentile(returns, 1)
    var_5 = np.percentile(returns, 5)

    last_price = bars['close'].iloc[-1]
    var1_cash = var_1 / 100 * qty * last_price
    var5_cash = var_5 / 100 * qty * last_price

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(returns, bins=50, color='steelblue', edgecolor='black', alpha=0.7)

    ax.axvline(mean, color='green', linestyle='--', label=f'Mean: {mean:.2f}%')
    ax.axvline(mean + std, color='orange', linestyle='--', label='+1σ')
    ax.axvline(mean - std, color='orange', linestyle='--', label='-1σ')
    ax.axvline(var_1, color='red', linestyle='--', label=f'VaR 1%: {var_1:.2f}% (${var1_cash:.2f})')
    ax.axvline(var_5, color='purple', linestyle='--', label=f'VaR 5%: {var_5:.2f}% (${var5_cash:.2f})')

    ax.set_title(f'{symbol} - 1min Return Histogram (500 bins)')
    ax.set_xlabel('Log Returns (%)')
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=8)
    st.pyplot(fig)

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

def get_filled_orders():
    request = GetOrdersRequest(status="all")
    orders = trading_client.get_orders(filter=request)

    if not orders:
        return None

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

st.markdown("## 💵 Live PnL (Realized)")
realized_pnl = get_account_pnl()
st.metric("Realized PnL (USD)", f"${realized_pnl:,.2f}")


st.subheader("🔴 Live Position")
positions = get_positions()
pos_df = pd.DataFrame([p.__dict__ for p in positions]
    ).rename(columns={"market_value":"financial_pos",})
st.dataframe(pos_df[["symbol", "qty", "avg_entry_price", "financial_pos", "unrealized_pl"]])

st.subheader("📊 Exposure by Asset")
exposure_df = get_exposure(positions)

ex_fig = go.Figure()
ex_fig.add_trace(go.Bar(
    x=exposure_df['Symbol'],
    y=exposure_df['Exposure'],
    text=[f"${v:,.2f}" for v in exposure_df['Exposure']],
    textposition='outside',
    marker_color='rgb(100,149,237)'
))
ex_fig.update_layout(
    template='plotly_dark',
    title='Exposure by Asset',
    xaxis_title='Symbol',
    yaxis_title='Exposure (USD)',
    margin=dict(t=50, b=50),
    height=500
)
st.plotly_chart(ex_fig, use_container_width=True)

st.subheader("🛡️ Estimated Risk (-1% / +1%)")
risk_data = []
for pos in positions:
    symbol = pos.symbol
    qty = float(pos.qty)
    price = float(pos.current_price)
    value = qty * price
    risk_pos = value * 0.01
    risk_neg = -value * 0.01
    risk_data.append({
        'Symbol': symbol,
        '+1% Move': risk_pos,
        '-1% Move': risk_neg
    })
risk_df = pd.DataFrame(risk_data).sort_values(by='+1% Move', ascending=True)

risk_fig = go.Figure(data=[
    go.Bar(name='-1% Move', x=risk_df['Symbol'], y=risk_df['-1% Move'], marker_color='crimson'),
    go.Bar(name='+1% Move', x=risk_df['Symbol'], y=risk_df['+1% Move'], marker_color='limegreen')
])
risk_fig.update_layout(
    barmode='group',
    template='plotly_dark',
    title='Estimated Risk for ±1% Move',
    xaxis_title='Symbol',
    yaxis_title='Risk (USD)',
    height=500
)
st.plotly_chart(risk_fig, use_container_width=True)

st.subheader("📉 1min Return Histogram with VaR")

for pos in positions:
    symbol = pos.symbol
    qty = float(pos.qty)

    st.markdown(f"#### {symbol}")
    result = plot_return_histogram(symbol, qty)
    if result is None:
        st.warning(f"No recent data for {symbol}.")

st.subheader("📋 Executed Orders")
orders_df = get_filled_orders()
st.dataframe(orders_df)