from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

@app.route('/', methods=['GET'])
def home():
    return "✅ Server is running!"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return "No data", 400

    chat_id = data.get("message", {}).get("chat", {}).get("id")
    text = data.get("message", {}).get("text", "")

    if text == "/start":
        send_message(chat_id, "Salom! Bot ishga tushdi ✅")
    elif text:
        send_message(chat_id, f"Siz yubordingiz: {text}")

    return "ok", 200


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
