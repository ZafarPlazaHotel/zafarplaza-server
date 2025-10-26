from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("ADMIN_CHAT_ID")

@app.route("/")
def home():
    return "ok"

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    room = data.get("room")
    product = data.get("product")
    quantity = data.get("quantity")
    comment = data.get("comment")

    text = f"""
🛎 Yangi buyurtma:
🏠 Xona: {room}
☕️ Mahsulot: {product}
📦 Miqdor: {quantity}
💬 Izoh: {comment}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, json=payload)

    return {"status": "success", "message": "Buyurtma yuborildi!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
