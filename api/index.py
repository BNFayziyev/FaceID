
from flask import Flask, request
import requests
import re

app = Flask(__name__)

BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        return "Server ishlayapti!", 200

    try:
        # Terminaldan kelgan barcha ma'lumotni olish
        raw_data = request.get_data(as_text=True) or ""
        
        # 1-urinish: employeeNo ni qidirish
        match = re.search(r'<employeeNo>(.*?)</employeeNo>', raw_data)
        
        # 2-urinish: Agar employeeNo bo'lmasa, shunchaki ID ni qidirish
        if not match:
            match = re.search(r'<ID>(.*?)</ID>', raw_data)

        if match:
            emp_id = match.group(1)
            msg = f"✅ Xodim o'tdi! \nID: {emp_id}"
        else:
            # AGAR ID TOPILMASA: Terminal yuborgan matnning bir qismini Telegramga yuboramiz
            # Bu bizga xatoni topishga yordam beradi
            debug_info = raw_data[:300] # Birinchi 300 ta harf
            msg = f"❓ ID topilmadi. Terminal yuborgan ma'lumot:\n\n{debug_info}"

        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
        
        return "OK", 200

    except Exception as e:
        return "OK", 200 # Terminalga har doim OK qaytaramiz

def handler(event, context):
    return app(event, context)