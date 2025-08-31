import os, time
from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase_client import supabase  # ✅ Integrated

def tier1_scan():
    tickers = fetch_tickers()
    for ticker in tickers:
        data = fetch_indicators(ticker)
        if not data or not is_valid(data): continue
        send_alert(ticker, data, tier=1)
        supabase.table("alerts_log").insert({"ticker": ticker, "data": data}).execute()
        time.sleep(1)

def is_valid(d):
    return (
        0.005 <= d["price"] <= 50 and
        d["volume"] > 15_000_000 and
        2 <= d["rvol"] and
        50 <= d["rsi"] <= 70 and
        d["ema_stack"] == "bullish" and
        abs(d["vwap_diff"]) <= 0.02 and
        not d["is_pump"]
    )

if __name__ == "__main__":
    tier1_scan()
