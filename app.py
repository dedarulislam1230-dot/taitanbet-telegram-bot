import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    if not BOT_TOKEN:
        return

    try:
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=10
        )
    except requests.RequestException:
        app.logger.exception("Telegram message failed")


@app.route("/", methods=["GET"])
def home():
    return "Taitan Bet AI Assistant is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip().lower()

    if not chat_id or not text:
        return {"ok": True}

    if text == "/start":
        reply = (
            "স্বাগতম Taitan Bet AI Assistant-এ! 💙\n\n"
            "আমি আপনাকে অ্যাকাউন্ট ও সাপোর্ট সংক্রান্ত "
            "সাধারণ তথ্য দিতে সাহায্য করব।\n\n"
            "/help লিখুন সাহায্যের জন্য।"
        )
        send_message(chat_id, reply)

    elif text == "/help":
        send_message(
            chat_id,
            "আপনার কী সাহায্য প্রয়োজন?\n\n"
            "• Deposit সহায়তা\n"
            "• Withdraw সহায়তা\n"
            "• Wallet সংক্রান্ত প্রশ্ন\n"
            "• Customer Support"
        )

    else:
        send_message(
            chat_id,
            "আপনার বার্তা পেয়েছি। 💙\n"
            "AI Support এখনো সংযুক্ত করা হয়নি।"
        )

    return {"ok": True}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
