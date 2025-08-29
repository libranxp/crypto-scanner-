import os
import time
import pandas as pd
from data_fetcher import fetch_market_data
from db_manager import store_scan_result
from telegram_alert import send_alert
from dotenv import load_dotenv

load_dotenv("config.env")

# Thresholds
MIN_VOLUME = 1000000  # $1M
MIN_RSI = 55
RVOL_THRESHOLD = 1.5
VWAP_PROXIMITY = 0.02  # ±2%

def is_valid_candidate(data):
    try:
        price = data['price']
        volume = data['volume']
        rsi = data['rsi']
        rvol = data['rvol']
        ema_alignment = data['ema5'] > data['ema13'] > data['ema50']
        vwap_proximity = abs(data['price'] - data['vwap']) / data['vwap'] <= VWAP_PROXIMITY

        return (
            volume >= MIN_VOLUME and
            rsi >= MIN_RSI and
            rvol >= RVOL_THRESHOLD and
            ema_alignment and
            vwap_proximity
        )
    except KeyError:
        return False

def run_tier1_scan():
    print("🔍 Running Tier 1 Scan...")
    tickers = fetch_market_data()
    results = []

    for ticker, data in tickers.items():
        if is_valid_candidate(data):
            result = {
                "ticker": ticker,
                "price": data['price'],
                "change": data['change'],
                "volume": data['volume'],
                "rsi": data['rsi'],
                "rvol": data['rvol'],
                "vwap": data['vwap'],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            results.append(result)
            store_scan_result(result)
            send_alert(result, tier=1)

    print(f"✅ Tier 1 Scan Complete. {len(results)} signals found.")

if __name__ == "__main__":
    run_tier1_scan()
