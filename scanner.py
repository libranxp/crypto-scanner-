import os
from dotenv import load_dotenv
from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def tier1_scan():
    tickers = fetch_tickers()
    for coin in tickers:
        data = fetch_indicators(coin)
        if not data or not is_valid(data): continue
        send_alert(coin, data, tier=1)
        supabase.table("alerts_log").insert({"ticker": coin, "data": data}).execute()

def is_valid(d):
    return (
        0.005 <= d["price"] <= 50 and
        d["volume"] > 15_000_000 and
        2 <= d["rvol"] and
        50 <= d["rsi"] <= 70 and
        d["ema_stack"] == "bullish" and
        abs(d["vwap_diff"]) <= 0.02 and
        not d["is_pump"] and
        not d["is_duplicate"]
    )

if __name__ == "__main__":
    tier1_scan()
