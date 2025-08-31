import requests

def fetch_tickers():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "volume_desc", "per_page": 100}
    r = requests.get(url, params=params).json()
    return [c["symbol"].upper() for c in r if 0.005 <= c["current_price"] <= 50 and c["market_cap"] >= 20_000_000]

def fetch_indicators(ticker):
    # Replace with real API calls
    return {
        "price": 0.12,
        "volume": 20000000,
        "rsi": 60,
        "rvol": 2.5,
        "ema_stack": "bullish",
        "vwap_diff": 0.01,
        "is_pump": False
    }
