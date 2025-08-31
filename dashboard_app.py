import streamlit as st
from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase import create_client
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(page_title="📊 Crypto Momentum Scanner", layout="wide")
st.title("📊 Crypto Momentum Scanner")

scan_type = st.radio("Scan Type", ["Tier 1", "Tier 2"])
tickers = fetch_tickers()

for ticker in tickers:
    data = fetch_indicators(ticker)
    if not data: continue
    st.write(f"**{ticker}** | Price: ${data['price']} | RSI: {data['rsi']} | RVOL: {data['rvol']}")
    if scan_type == "Tier 2":
        if st.button(f"Run Deep Scan for {ticker}"):
            score = run_ai_model(data)
            data["narrative"] = "Bullish sentiment + whale activity"
            send_alert(ticker, data, tier=2, score=score)
            supabase.table("tier2_scores").insert({
                "ticker": ticker,
                "score": score,
                "confidence": 0.85,
                "narrative": data["narrative"],
                "data": data
            }).execute()

def run_ai_model(data):
    # Replace with real ML model
    return 8.2
