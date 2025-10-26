from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Server ishlayapti ✅"})

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    room = data.get("room", "Noma'lum xona")
    product = data.get("product", "Noma'lum mahsulot")
    quantity = data.get("quantity", 1)
    comment = data.get("comment", "")

    message = (
        f"🛎 Yangi buyurtma:\n"
        f"🏨 Xona: {room}\n"
        f"☕ Mahsulot: {product}\n"
        f"🔢 Miqdor: {quantity}\n"
        f"💬 Izoh: {comment}"
    )

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_CHAT_ID, "text": message}
        )
        if r.status_code == 200:
            return jsonify({"status": "success", "message": "Buyurtma yuborildi!"})
        else:
            return jsonify({"status": "error", "message": f"Telegram error: {r.text}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
