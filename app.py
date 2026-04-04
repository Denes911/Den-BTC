import streamlit as st
import requests

# Oldal beállítása (cím és ikon a böngésző fülön)
st.set_page_config(page_title="BTC Monitor", page_icon="🪙")

st.title("🪙 Élő Bitcoin Árfolyam")
st.write("Ez az alkalmazás valós időben kéri le a BTC árfolyamát a Coinbase-től.")

def get_price():
    try:
        # Stabil Coinbase API végpont
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        response = requests.get(url, timeout=10)
        
        # Ellenőrizzük, hogy a szerver válaszolt-e rendesen
        response.raise_for_status()
        
        data = response.json()
        # Az ár kinyerése a Coinbase válaszából
        price = float(data['data']['amount'])
        
        return f"{price:,.2f}"
    except Exception as e:
        return f"Hiba történt: {str(e)}"

# Gomb a frissítéshez
if st.button('Árfolyam lekérdezése'):
    with st.spinner('Kapcsolódás a szerverhez...'):
        price_result = get_price()
        
        if "Hiba" in price_result:
            st.error(price_result)
        else:
            # Megjelenítés nagy, szép számmal
            st.metric(label="Bitcoin (USD)", value=f"$ {price_result}")
            st.success("Adatok sikeresen frissítve!")

st.info("Kattints a fenti gombra az aktuális ár megjelenítéséhez.")

