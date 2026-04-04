import streamlit as st
import requests

st.title("🚀 Élő Bitcoin Árfolyam")

def get_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url)
    return f"{float(res.json()['price']):,.2f}"

    except:
        return "Hiba az adatoknál"

if st.button('Frissítés'):
    price = get_price()
    st.metric("BTC Ár (USDT)", f"$ {price}")
