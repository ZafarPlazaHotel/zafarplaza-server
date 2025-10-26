from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Tilda bilan ishlashi uchun CORS butunlay yoqamiz
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "7936668543:AAEjYNdUk2fKNTa29mpnWdT9YBPx_E54hSg")
CHAT_ID = os.getenv("CHAT_ID", "8411892709")

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Server ishlayapti"})

@app.route('/order', methods=['POST'])
def order():
    try:
        data = request.get_json(force=True)
    except:
        return jsonify({"status": "error", "message": "JSON o‘qilmadi"}), 400

    if not data:
        return jsonify({"status": "error", "message": "Bo‘sh ma'lumot"}), 400

    room = data.get("room", "Noma’lum xona")
    product = data.get("product", "Noma’lum mahsulot")
    quantity = data.get("quantity", "1")
    comment = data.get("comment", "")

    text = f"🛎 Yangi buyurtma:\n🏠 Xona: {room}\n☕️ Mahsulot: {product}\n📦 Miqdor: {quantity}\n💬 Izoh: {comment}"

    # Telegramga yuborish
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Telegramga yuborildi"}), 200
    else:
        return jsonify({"status": "error", "message": "Telegram xatosi"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
