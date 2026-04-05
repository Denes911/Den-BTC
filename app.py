    import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import plotly.graph_objects as go
import requests

# Oldal beállítása
st.set_page_config(page_title="BTC Dashboard", page_icon="📊", layout="wide")

def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=1", timeout=10)
        data = r.json()
        return int(data["data"][0]["value"]), data["data"][0]["value_classification"]
    except:
        return 50, "N/A"

st.title("📊 BTC Haladó Dashboard & Analízis")
st.info("Az adatok forrása: Yahoo Finance & Alternative.me")

if st.button('Adatok Frissítése és Elemzés'):
    with st.spinner('Adatok lekérése...'):
        # BTC adatok lekérése a Yahoo Finance-től (period="7d" az utolsó 7 nap, interval="1h" az órás bontás)
        df = yf.download("BTC-USD", period="7d", interval="1h")
        
        if not df.empty:
            # Adatok tisztítása
            df = df.reset_index()
            # Oszlopnevek egységesítése
            df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
            df = df.rename(columns={'datetime': 'time', 'date': 'time', 'index': 'time'})

            # Indikátorok számítása
            rsi_op = RSIIndicator(df["close"], window=14)
            rsi = round(rsi_op.rsi().iloc[-1], 2)
            
            ema50_ser = EMAIndicator(df["close"], window=50).ema_indicator()
            ema200_ser = EMAIndicator(df["close"], window=200).ema_indicator()
            
            price = df["close"].iloc[-1]
            ema50 = ema50_ser.iloc[-1]
            ema200 = ema200_ser.iloc[-1]
            
            fg, fg_class = get_fear_greed()

            # Pontozás (Score)
            score = 0
            reasons = []
            if fg < 25: score += 2; reasons.append("😨 Extrém Félelem (Vételi zóna)")
            elif fg > 70: score -= 2; reasons.append("😎 Mohóság (Eladási zóna)")
            if rsi < 35: score += 2; reasons.append("📉 RSI túladott")
            elif rsi > 65: score -= 2; reasons.append("🔥 RSI túlvett")
            if price > ema200: score += 1; reasons.append("📈 Trend: Bullish (EMA200 felett)")
            else: score -= 1; reasons.append("📉 Trend: Bearish (EMA200 alatt)")

            # Megjelenítés
            col1, col2, col3 = st.columns(3)
            col1.metric("Ár (USD)", f"${price:,.2f}")
            col2.metric("Fear & Greed", f"{fg} ({fg_class})")
            col3.metric("RSI (14h)", rsi)

            st.subheader("🧠 Elemzés eredménye:")
            if score > 1: st.success(f"🟢 VÉLEMÉNY: BULLISH (Pontszám: {score})")
            elif score < -1: st.error(f"🔴 VÉLEMÉNY: BEARISH (Pontszám: {score})")
            else: st.warning(f"⚪ VÉLEMÉNY: NEUTRÁLIS (Pontszám: {score})")
            
            for r in reasons:
                st.write(f"- {r}")

            # Grafikon rajzolása
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["time"], y=df["close"], name="BTC Ár"))
            fig.add_trace(go.Scatter(x=df["time"], y=ema50_ser, name="EMA50", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=df["time"], y=ema200_ser, name="EMA200", line=dict(width=2)))
            fig.update_layout(title="BTC Árfolyam és Indikátorok", template="plotly_dark", height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Nem sikerült adatokat kinyerni a Yahoo Finance-től!")
        
