from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase_client import insert_row

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

def tier1_scan():
    tickers = fetch_tickers()
    for coin_id in tickers:
        data = fetch_indicators(coin_id)
        if not isinstance(data, dict): continue
        if not is_valid(data): continue
        send_alert(coin_id.upper(), data, tier=1)
        insert_row("alerts_log", {"ticker": coin_id.upper(), "data": data})

if __name__ == "__main__":
    tier1_scan()
