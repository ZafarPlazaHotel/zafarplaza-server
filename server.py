# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

app = Flask(__name__)
# Tilda yoki boshqa domenlardan so'rov kelishi uchun origins="*" qilamiz
CORS(app, origins="*")

# Telegram sozlamalari — RENDER/PA da Environment Variables sifatida qo'ying
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "").strip()

if not BOT_TOKEN or not ADMIN_CHAT_ID:
    logging.warning("BOT_TOKEN yoki ADMIN_CHAT_ID topilmadi. Telegram xabar berish ishlamasligi mumkin.")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Server ishlayapti"}), 200

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"info":"Server ishlayapti va tayyor","status":"ok"}), 200

@app.route("/order", methods=["POST"])
def order():
    # JSON olish
    try:
        data = request.get_json(force=True)
    except Exception as e:
        logging.exception("JSON o'qishda xato")
        return jsonify({"status":"error","message":"Invalid JSON"}), 400

    room = data.get("room") or data.get("room_no") or "Noma'lum"
    product = data.get("product") or data.get("item") or data.get("name") or "Noma'lum mahsulot"
    quantity = data.get("quantity") or data.get("qty") or 1
    comment = data.get("comment") or data.get("note") or ""

    text = (
        f"🛎 <b>Yangi buyurtma</b>\n"
        f"🏠 Hona: {room}\n"
        f"☕️ Mahsulot: {product}\n"
        f"🔢 Miqdor: {quantity}\n"
        f"💬 Izoh: {comment}"
    )

    # Telegramga yuborish
    if BOT_TOKEN and ADMIN_CHAT_ID:
        try:
            tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            resp = requests.post(tg_url, json={
                "chat_id": ADMIN_CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            }, timeout=10)
            if resp.status_code != 200:
                logging.error("Telegram API xato: %s", resp.text)
                # ammo buyurtmani qabul qildik hamma joyda ham ishlasin deyish uchun success qaytaramiz
        except Exception as e:
            logging.exception("Telegramga yuborishda xato")
    else:
        logging.warning("Telegram token yoki chat_id yo'q, faqat logda saqlanmoqda.")

    logging.info("Buyurtma qabul qilindi: %s | %s | %s", room, product, quantity)
    return jsonify({"status":"success","message":"Buyurtma qabul qilindi"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info("Server start on port %s", port)
    app.run(host="0.0.0.0", port=port)
