
from flask import Flask, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# O'zingizning ma'lumotlaringiz
BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        # TEST: Brauzerda ochganda ham xabar yuborish
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": "Test: Brauzerdan so'rov keldi!"})
        return "Server ishlayapti. Test xabari Telegramga yuborildi!", 200

    try:
        xml_data = request.data.decode('utf-8')
        root = ET.fromstring(xml_data)

        employee_id = "Noma'lum"
        for elem in root.iter():
            if 'employeeNo' in elem.tag:
                employee_id = elem.text

        msg = f"🔔 Terminaldan xabar: ID {employee_id} o'tdi."
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg})
        
        return "OK", 200
    except Exception as e:
        return f"Xato: {str(e)}", 500

# MUHIM: Vercel Flaskni 'app' nomi bilan qidiradi