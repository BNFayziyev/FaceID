


from flask import Flask, request
import requests
import re

app = Flask(__name__)

# Ma'lumotlaringiz
BOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'GET':
        return "Server Ready!", 200

    try:
        # Terminaldan kelgan ma'lumot
        raw_data = request.get_data(as_text=True) or ""
        
        # ID ni bir nechta usulda qidiramiz
        # 1. <employeeNo> 2. <ID> 3. <cardNo>
        emp_match = re.search(r'<employeeNo>(.*?)</employeeNo>', raw_data)
        id_match = re.search(r'<ID>(.*?)</ID>', raw_data)
        card_match = re.search(r'<cardNo>(.*?)</cardNo>', raw_data)

        if emp_match:
            res_id = emp_match.group(1)
        elif id_match:
            res_id = id_match.group(1)
        elif card_match:
            res_id = card_match.group(1)
        else:
            res_id = None

        if res_id:
            msg = f"✅ Xodim o'tdi!\nID: {res_id}"
        else:
            # Agar ID topilmasa, terminal nima yuborganini ko'rish uchun:
            msg = f"❓ ID topilmadi. XML boshlanishi:\n{raw_data[:200]}"

        # Telegramga yuborish
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
        return "OK", 200

    except Exception as e:
        return "OK", 200

# DIQQAT: Vercel uchun 'handler' funksiyasini olib tashladik. 
# Flask'ning 'app' obyekti o'zi yetarli.