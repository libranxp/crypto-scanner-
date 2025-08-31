import streamlit as st
from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase_client import insert_row

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
            score = run_ai_model(data)
            data["narrative"] = "Bullish sentiment + whale activity"
            send_alert(coin_id.upper(), data, tier=2, score=score)
            insert_row("tier2_scores", {
                "ticker": coin_id.upper(),
                "score": score,
                "confidence": 0.85,
                "narrative": data["narrative"],
                "data": data
            })

def run_ai_model(data):
    return 8.2  # Replace with real model later
