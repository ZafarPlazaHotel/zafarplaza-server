from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# 🔥 CORS butunlay yoqilgan (Tilda uchun)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔑 Telegram ma'lumotlari
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID_HERE")

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Server ishlayapti"}), 200

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    room = data.get("room", "Noma'lum xona")
    product = data.get("product", "Noma'lum mahsulot")
    quantity = data.get("quantity", "1")
    comment = data.get("comment", "")

    text = f"🛎 Yangi buyurtma:\n🏠 Xona: {room}\n☕️ Mahsulot: {product}\n📦 Miqdor: {quantity}\n💬 Izoh: {comment}"

    # Telegramga yuborish
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Telegramga yuborilmadi"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
