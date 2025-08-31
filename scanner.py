from data_fetcher import fetch_tickers, fetch_indicators
from telegram_bot import send_alert
from supabase_client import insert_row

def tier1_scan():
    tickers = fetch_tickers()
    for ticker in tickers:
        data = fetch_indicators(ticker)
        if not isinstance(data, dict): continue
        if not is_valid(data): continue
        send_alert(ticker, data, tier=1)
        insert_row("alerts_log", {"ticker": ticker, "data": data})
