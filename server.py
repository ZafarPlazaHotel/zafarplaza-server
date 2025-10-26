# server.py
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

app = Flask(__name__)
# CORS: Tilda yoki hamma joydan murojaat qilish uchun * ishlatish mumkin,
# agar xohlasangiz originni tilda sahifangiz bilan cheklang
CORS(app, resources={r"/order": {"origins": "*"}})

# BOT token va admin chat idni ENV orqali bering:
BOT_TOKEN = os.getenv("BOT_TOKEN")  # misol: export BOT_TOKEN="123:ABC..."
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # misol: export ADMIN_CHAT_ID="8411892709"

if not BOT_TOKEN or not ADMIN_CHAT_ID:
    logging.warning("BOT_TOKEN yoki ADMIN_CHAT_ID atrof-muhitda topilmadi. Telegram yuborish ishlamasligi mumkin.")

TELEGRAM_SEND_URL = "https://api.telegram.org/bot{token}/sendMessage"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status":"ok","message":"Zafar Plaza server ishlayapti ✅"}), 200

@app.route("/order", methods=["POST"])
def order():
    try:
        data = request.get_json(force=True)
    except Exception as e:
        logging.exception("JSON parse error")
        return jsonify({"success": False, "error": "Invalid JSON"}), 400

    # Mos kalitlar nomlari (Tilda sahifasidagi JS bilan mos bo'lsin)
    room = data.get("room") or data.get("room_number") or "Noma'lum"
    item = data.get("item") or data.get("product") or "Noma'lum mahsulot"
    quantity = data.get("quantity", 1)
    price = data.get("price", "")
    comment = data.get("comment", "")

    if not room or not item:
        return jsonify({"success": False, "error": "room and item required"}), 400

    # Telegram uchun xabar
    text = (
        f"🛎 <b>Yangi buyurtma</b>\n"
        f"🏨 Xona: <b>{room}</b>\n"
        f"🍽 Mahsulot: <b>{item}</b>\n"
        f"🔢 Miqdor: <b>{quantity}</b>\n"
        f"💰 Narx: <b>{price}</b>\n"
    )
    if comment:
        text += f"💬 Izoh: {comment}\n"

    # Telegramga yuborish
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        logging.error("Telegram token/ID yo'q — xabar yuborilmadi. payload=%s", data)
        return jsonify({"success": False, "error": "Telegram token not configured"}), 500

    try:
        resp = requests.post(
            TELEGRAM_SEND_URL.format(token=BOT_TOKEN),
            json={"chat_id": ADMIN_CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        logging.exception("Telegramga yuborishda xato")
        return jsonify({"success": False, "error": "Telegram request failed"}), 500

    if resp.status_code != 200:
        logging.error("Telegram API xato: status=%s body=%s", resp.status_code, resp.text)
        return jsonify({"success": False, "error": "Telegram API error", "details": resp.text}), 502

    logging.info("Buyurtma qabul qilindi: room=%s item=%s qty=%s", room, item, quantity)
    return jsonify({"success": True}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    logging.info("Server starting on port %s", port)
    app.run(host="0.0.0.0", port=port)
