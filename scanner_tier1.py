from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase_client import insert_row

def is_valid(data):
    return (
        0.005 <= data["price"] <= 50 and
        data["volume"] > 15_000_000 and
        2 <= data["rvol"] and
        50 <= data["rsi"] <= 70 and
        data["ema_stack"] == "bullish" and
        abs(data["vwap_diff"]) <= 0.02 and
        not data["is_pump"]
    )

def run_tier1_scan():
    tickers = fetch_tickers()
    for coin_id in tickers:
        data = fetch_indicators(coin_id)
        if not isinstance(data, dict): continue
        if not is_valid(data): continue
        send_alert(coin_id.upper(), data, tier=1)
        insert_row("alerts_log", {"ticker": coin_id.upper(), "data": data})

if __name__ == "__main__":
    run_tier1_scan()
