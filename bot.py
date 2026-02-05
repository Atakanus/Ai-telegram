import os
import time
import json
import requests
from openai import OpenAI  # OpenAI kütüphanesini yüklemiş olman gerekir

# --- AYARLAR ---
# Pydroid terminaline 'pip install openai' yazmayı unutma!
client = OpenAI(api_key="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")

TELEGRAM_TOKEN = "8483969480:AAGlFsDGFu1aMOSpwDyTgzuySmsfGEQYK7U"
TG_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

print("🧠 V601 SİSTEM BAŞLATILDI (Modern SDK)")

# --- HAFIZA ---
try:
    with open("memory.json", "r", encoding="utf-8") as f:
        memory = json.load(f)
except:
    memory = {}

def save():
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

# --- AI YANIT MOTORU ---
def get_ai_reply(user_id, text):
    uid = str(user_id)
    if uid not in memory:
        memory[uid] = {"history": []}
    
    memory[uid]["history"].append({"role": "user", "content": text})
    memory[uid]["history"] = memory[uid]["history"][-6:] # Son 6 mesajı hatırla

    try:
        # GPT-5.2 yok, en iyisi 'gpt-4o-mini' veya 'gpt-4o' kullanmaktır
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen karizmatik bir siber asistansın."}
            ] + memory[uid]["history"]
        )
        
        reply = response.choices[0].message.content
        memory[uid]["history"].append({"role": "assistant", "content": reply})
        save()
        return reply
    except Exception as e:
        print("AI Hata:", e)
        return "Zihnim şu an bulanık, biraz bekle efendim."

# --- ANA DÖNGÜ ---
offset = 0
while True:
    try:
        r = requests.get(TG_URL + f"getUpdates?offset={offset}&timeout=20").json()
        if "result" in r:
            for update in r["result"]:
                offset = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    user_id = update["message"]["from"]["id"]
                    msg_text = update["message"]["text"]

                    # Cevap oluştur ve gönder
                    answer = get_ai_reply(user_id, msg_text)
                    requests.get(TG_URL + f"sendMessage?chat_id={chat_id}&text={answer}")
                    
    except Exception as e:
        print("Döngü hatası:", e)
        time.sleep(2)
