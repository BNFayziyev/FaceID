
from flask import Flask, request
import requests
import json
import re

app = Flask(__name__)

BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        return "Server Sozlandi! Terminalni kutyapman...", 200

    try:
        # Terminal JSON ma'lumotni 'event_log' nomi bilan multipart formatda yuboryapti
        # Biz uni matn ichidan sug'urib olamiz
        raw_data = request.get_data(as_text=True) or ""
        
        # JSON qismini qidirish ( { dan boshlanib } gacha )
        json_match = re.search(r'({.*})', raw_data, re.DOTALL)
        
        if json_match:
            data_str = json_match.group(1)
            data = json.loads(data_str)
            
            # JSON ichidan ID ni olish (Hikvision uchun odatda 'employeeNoString')
            emp_id = data.get('employeeNoString') or data.get('employeeNo') or data.get('id')
            
            if emp_id:
                msg = f"✅ Xodim o'tdi!\nID: {emp_id}"
            else:
                msg = "❓ Harakat bor, lekin ID topilmadi (JSON ichida)."
        else:
            msg = "❓ Terminal tushunarsiz format yubordi."

        # Telegramga yuborish
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
        return "OK", 200

    except Exception as e:
        # Xatolikni log qilish (faqat bot egasiga)
        return "OK", 200