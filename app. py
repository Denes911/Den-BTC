import streamlit as st
import requests
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import plotly.graph_objects as go

# Oldal beállítása
st.set_page_config(page_title="BTC Haladó Dashboard", page_icon="📊", layout="wide")

# =========================
# HELPERS & API
# =========================
def safe_request(url, headers=None):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def get_fear_greed():
    data = safe_request("https://api.alternative.me/fng/?limit=1")
    if data:
        fg = int(data["data"][0]["value"])
        fg_class = data["data"][0]["value_classification"]
        return fg, fg_class
    return 50, "N/A"

def get_market_data():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=200"
    data = safe_request(url)
    if not data:
        return None
    df = pd.DataFrame(data)
    df = df[[0, 4]].copy()
    df.columns = ["time", "close"]
    df["close"] = df["close"].astype(float)
    df["time"] = pd.to_datetime(df[0], unit='ms')
    return df

def get_funding():
    data = safe_request("https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT")
    return float(data["lastFundingRate"]) if data else 0

# =========================
# DASHBOARD
# =========================
st.title("📊 BTC Haladó Dashboard & Analízis")

if st.button('Adatok Frissítése és Elemzés'):
    with st.spinner('Elemzés folyamatban...'):
        df = get_market_data()
        fg, fg_class = get_fear_greed()
        funding = get_funding()

        if df is not None:
            # Indikátorok számítása
            rsi_op = RSIIndicator(df["close"], window=14)
            rsi = round(rsi_op.rsi().iloc[-1], 2)
            
            ema50_ser = EMAIndicator(df["close"], window=50).ema_indicator()
            ema200_ser = EMAIndicator(df["close"], window=200).ema_indicator()
            
            price = df["close"].iloc[-1]
            ema50 = ema50_ser.iloc[-1]
            ema200 = ema200_ser.iloc[-1]

            # Pontozás (Score)
            score = 0
            reasons = []
            if fg < 25: score += 2; reasons.append("😨 Extrém Félelem (Vételi jel)")
            elif fg > 70: score -= 2; reasons.append("😎 Mohóság (Eladási jel)")
            if rsi < 30: score += 2; reasons.append("📉 RSI túladott")
            elif rsi > 70: score -= 2; reasons.append("🔥 RSI túlvett")
            if price > ema200: score += 2; reasons.append("📈 Ár az EMA200 felett (Bullish)")
            else: score -= 2; reasons.append("📉 Ár az EMA200 alatt (Bearish)")

            # Megjelenítés
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Ár (BTC/USDT)", f"${price:,.2f}")
            col2.metric("Fear & Greed", f"{fg} ({fg_class})")
            col3.metric("RSI (14h)", rsi)
            col4.metric("Funding Rate", f"{funding:.5f}")

            # Eredmény
            st.subheader("🧠 Mesterséges Intelligencia Elemzése:")
            if score > 2: st.success(f"🟢 VÉLEMÉNY: ERŐS BULLISH (Score: {score})")
            elif score < -2: st.error(f"🔴 VÉLEMÉNY: ERŐS BEARISH (Score: {score})")
            else: st.warning(f"⚪ VÉLEMÉNY: NEUTRÁLIS (Score: {score})")

            for r in reasons:
                st.write(f"- {r}")

            # Grafikon
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["time"], y=df["close"], name="BTC Ár"))
            fig.add_trace(go.Scatter(x=df["time"], y=ema50_ser, name="EMA50", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=df["time"], y=ema200_ser, name="EMA200", line=dict(width=2)))
            fig.update_layout(title="BTC Árfolyam + Indikátorok", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Hiba az adatok lekérésekor!")

