

from flask import Flask, request
import requests
import re

app = Flask(__name__)

# O'zingizning ma'lumotlaringizni kiriting
BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # Brauzerda tekshirish uchun
    if request.method == 'GET':
        return "Server ishga tushdi! Terminal kutyapman...", 200

    # Terminaldan ma'lumot kelganda
    try:
        # Kelgan ma'lumotni xatosiz o'qish
        xml_data = request.get_data(as_text=True) or ""
        
        # Regex bilan ID ni qidirish
        match = re.search(r'<employeeNo>(.*?)</employeeNo>', xml_data)
        
        if match:
            employee_id = match.group(1)
            msg = f"🔔 Terminal xabari:\nXodim ID: {employee_id}\nMuvaffaqiyatli o'tdi ✅"
        else:
            # Agar ID bo'lmasa, shunchaki log yozamiz
            msg = "🔔 Terminal: Harakat aniqlandi, lekin ID olinmadi."

        # Telegramga yuborish (timeout bilan, server qotib qolmasligi uchun)
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
            json={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
        
        return "OK", 200

    except Exception as e:
        # Xatolikni qaytarmaslik (server crash bo'lmasligi uchun)
        return "Internal error handled", 200

# Vercel uchun handler shart emas, Flask 'app' o'zi yetarli