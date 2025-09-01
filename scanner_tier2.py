from data_fetcher import fetch_indicators
from sentiment_fetcher import fetch_sentiment
from telegram_bot import send_alert
from supabase_client import insert_row

def run_ai_model(data):
    return 8.2, 0.85, "Bullish sentiment + whale activity"

def run_tier2_scan(coin_id):
    data = fetch_indicators(coin_id)
    if not isinstance(data, dict): return

    sentiment = fetch_sentiment(coin_id)
    data.update(sentiment)

    score, confidence, narrative = run_ai_model(data)
    data["narrative"] = narrative

    send_alert(coin_id.upper(), data, tier=2, score=score)
    insert_row("tier2_scores", {
        "ticker": coin_id.upper(),
        "score": score,
        "confidence": confidence,
        "narrative": narrative,
        "data": data
    })

if __name__ == "__main__":
    run_tier2_scan("bitcoin")
