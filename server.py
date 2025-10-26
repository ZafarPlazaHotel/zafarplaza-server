from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Server ishlayapti"})

@app.route("/order", methods=["POST"])
def order():
    try:
        data = request.get_json(force=True)
        room = data.get("room", "Noma'lum xona")
        product = data.get("product", "Noma'lum mahsulot")
        quantity = data.get("quantity", 1)
        comment = data.get("comment", "")

        message = (
            f"🛎 Yangi buyurtma:\n"
            f"🏠 Xona: {room}\n"
            f"☕️ Mahsulot: {product}\n"
            f"📦 Miqdor: {quantity}\n"
            f"💬 Izoh: {comment}"
        )

        res = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_CHAT_ID, "text": message}
        )

        if res.status_code == 200:
            return jsonify({"status": "success", "message": "Buyurtma yuborildi!"})
        else:
            return jsonify({"status": "error", "message": "Telegramga yuborilmadi."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
