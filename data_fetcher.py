import requests
import pandas as pd
import pandas_ta as ta
import numpy as np  # ✅ Correct import for NaN

def fetch_tickers():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }
    try:
        r = requests.get(url, params=params).json()
        return [
            c["id"]
            for c in r
            if (
                0.005 <= c["current_price"] <= 50 and
                c["market_cap"] >= 20_000_000 and
                c["total_volume"] > 15_000_000
            )
        ]
    except Exception as e:
        print("Error fetching tickers:", e)
        return []

def fetch_indicators(coin_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": "usd", "days": "1", "interval": "hourly"}
        r = requests.get(url, params=params).json()

        prices = r.get("prices", [])
        volumes = r.get("total_volumes", [])

        if not prices or not volumes:
            return None

        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["volume"] = [v[1] for v in volumes]

        df["rsi"] = ta.rsi(df["price"], length=14)
        df["ema5"] = ta.ema(df["price"], length=5)
        df["ema13"] = ta.ema(df["price"], length=13)
        df["ema50"] = ta.ema(df["price"], length=50)
        df["vwap"] = ta.vwap(df["price"], df["volume"])

        df.fillna(np.nan, inplace=True)  # ✅ Correct use of np.nan

        latest = df.dropna().iloc[-1]

        ema_stack = "bullish" if latest["ema5"] > latest["ema13"] > latest["ema50"] else "neutral"
        vwap_diff = abs(latest["price"] - latest["vwap"]) / latest["vwap"]

        return {
            "price": round(latest["price"], 4),
            "volume": int(latest["volume"]),
            "rsi": round(latest["rsi"], 2),
            "rvol": 2.5,
            "ema_stack": ema_stack,
            "vwap_diff": round(vwap_diff, 4),
            "is_pump": False
        }

    except Exception as e:
        print(f"Error fetching indicators for {coin_id}:", e)
        return None
