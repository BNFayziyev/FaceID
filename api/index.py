
from flask import Flask, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', methods=['GET', 'POST'])
def handle_faceid():
    # Agar brauzerda shunchaki ochilsa (GET)
    if request.method == 'GET':
        return "Server ishlayapti. Terminaldan POST so'rovini kutyapman...", 200

    # Terminaldan ma'lumot kelsa (POST)
    try:
        xml_data = request.data.decode('utf-8')
        # Kelgan ma'lumotni logda ko'rish (Vercel Logs bo'limida ko'rinadi)
        print("Kelgan ma'lumot:", xml_data)

        root = ET.fromstring(xml_data)
        employee_id = "Noma'lum"
        
        # Hikvision XML strukturasidan ID ni qidirish
        for elem in root.iter():
            if 'employeeNo' in elem.tag:
                employee_id = elem.text

        msg = f"🔔 Terminal xabari: Xodim (ID: {employee_id}) o'tdi."
        
        # Telegramga yuborish
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg})
        
        return "OK", 200
    except Exception as e:
        print(f"Xatolik: {e}")
        return f"Xatolik yuz berdi: {e}", 500

# Vercel uchun
def handler(event, context):
    return app(event, context)