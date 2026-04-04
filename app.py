import streamlit as st
import requests

st.set_page_config(page_title="BTC Monitor", page_icon="🚀")
st.title("🚀 Élő Bitcoin Árfolyam")

def get_price():
    try:
        # Pontos Binance API URL
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Ellenőrzi, hogy sikeres-e a kérés
        
        data = response.json()
        price = float(data['price'])
        
        return f"{price:,.2f}"
    except Exception as e:
        return f"Hiba: {str(e)}"

if st.button('Árfolyam Frissítése'):
    with st.spinner('Adatok lekérése...'):
        price_result = get_price()
        if "Hiba" in price_result:
            st.error(price_result)
        else:
            st.metric(label="Bitcoin (BTC/USDT)", value=f"$ {price_result}")
            st.success("Sikeres frissítés!")

