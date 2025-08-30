import os
import requests
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(ticker, data, tier=1, score=None):
    msg = f"🚨 ${ticker} | Price: ${data['price']} | Volume: ${data['volume']} | RSI: {data['rsi']} | RVOL: {data['rvol']}"
    if tier == 2:
        msg += f"\n📊 AI Score: {score}/10\n🧠 Reason: {data.get('narrative', 'N/A')}"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})
