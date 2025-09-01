import streamlit as st
from data_fetcher import fetch_tickers, fetch_indicators
from scanner_tier2 import run_tier2_scan

st.set_page_config(page_title="📊 Crypto Momentum Scanner", layout="wide")
st.title("📊 Crypto Momentum Scanner")

if st.button("🔁 Refresh Scan"):
    st.experimental_rerun()

scan_type = st.radio("Scan Type", ["Tier 1", "Tier 2"])
tickers = fetch_tickers()

for coin_id in tickers:
    data = fetch_indicators(coin_id)
    if not isinstance(data, dict): continue

    st.write(f"**{coin_id.upper()}** | Price: ${data['price']} | RSI: {data['rsi']} | RVOL: {data['rvol']}")
    
    if scan_type == "Tier 2":
        if st.button(f"Run Deep Scan for {coin_id.upper()}"):
            run_tier2_scan(coin_id)
