
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# O'zingizning ma'lumotlaringizni yozing
BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', methods=['POST'])
def handle_faceid():
    try:
        xml_data = request.data.decode('utf-8')
        root = ET.fromstring(xml_data)

        # Xodim ID raqamini qidirish
        employee_id = "Noma'lum"
        for elem in root.iter():
            if 'employeeNo' in elem.tag:
                employee_id = elem.text

        msg = f"🔔 Terminal xabari: Xodim (ID: {employee_id}) o'tdi."
        
        # Telegramga yuborish
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg})
        
        return "OK", 200
    except Exception as e:
        print(f"Xato: {e}")
        return "Error", 400

# Vercel uchun
def handler(event, context):
    return app(event, context)