import os
import requests

def send_alert(ticker, data, tier=1, score=None):
    msg = f"🚨 ${ticker} | Price: ${data['price']} | Volume: ${data['volume']} | RSI: {data['rsi']} | RVOL: {data['rvol']}"
    if tier == 2:
        msg += f"\n📊 AI Score: {score}/10\n🧠 Reason: {data['narrative']}"
    requests.post(f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage", data={
        "chat_id": os.getenv("TELEGRAM
