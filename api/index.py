
# MUHIM: Vercel Flaskni 'app' nomi bilan qidiradi
from flask import Flask, request
import requests
import re

app = Flask(__name__)

# O'zingizning ma'lumotlaringiz
BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        return "Server ishga tushdi! Terminal kutyapman...", 200

    try:
        # Kelgan ma'lumotni matn ko'rinishida olish
        xml_data = request.data.decode('utf-8', errors='ignore')
        
        # XML ichidan employeeNo ni topish (Eng xavfsiz yo'l - Regex orqali)
        match = re.search(r'<employeeNo>(.*?)</employeeNo>', xml_data)
        
        if match:
            employee_id = match.group(1)
            msg = f"🔔 Terminal xabari:\nXodim ID: {employee_id}\nMuvaffaqiyatli o'tdi ✅"
        else:
            # Agar ID topilmasa, voqeani bildirish
            msg = "🔔 Terminal: Harakat aniqlandi, lekin ID olinmadi."

        # Telegramga yuborish
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg})
        
        return "OK", 200

    except Exception as e:
        # Xatolikni logga yozish
        print(f"Xatolik yuz berdi: {str(e)}")
        return "Error", 500

# Vercel uchun
def handler(event, context):
    return app(event, context)