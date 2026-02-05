import requests
import time
import json
import random

# --- AYARLAR ---
TELEGRAM_TOKEN = "8483969480:AAGlFsDGFu1aMOSpwDyTgzuySmsfGEQYK7U"
OPENAI_KEY = "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"

# HATA DÜZELTME: Token doğrudan değişken olarak verildi
TG_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"
GPT_URL = "https://api.openai.com/v1/chat/completions"

print("🧠 V600 GERÇEK AI AKTİF")

# --- HAFIZA ---
try:
    with open("memory.json", "r", encoding="utf-8") as f:
        memory = json.load(f)
except:
    memory = {}

def save():
    with open("memory.json", "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

# --- CHATGPT BEYİN ---
def chatgpt_reply(user_id, text):
    uid = str(user_id)
    if uid not in memory:
        memory[uid] = {"history": []}
    
    memory[uid]["history"].append({"role": "user", "content": text})
    memory[uid]["history"] = memory[uid]["history"][-6:]
    
    messages = [
        {"role": "system", "content": "Sen zeki, karizmatik, hafızalı bir yapay zekasın. Kısa ve etkileyici cevaplar ver."}
    ] + memory[uid]["history"]
    
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.9
    }
    
    try:
        r = requests.post(GPT_URL, headers=headers, json=data, timeout=20).json()
        reply = r["choices"][0]["message"]["content"]
        memory[uid]["history"].append({"role": "assistant", "content": reply})
        save()
        return reply
    except Exception as e:
        print("GPT hata:", e)
        return "Zihin bağlantım koptu, parazit var..."

# --- ANALİZ KOMUTU ---
def analiz(user_id):
    uid = str(user_id)
    if uid not in memory:
        return "Henüz veri yok."
    mesaj_sayisi = len(memory[uid]["history"])
    if mesaj_sayisi < 5:
        seviye = "Yeni kullanıcı"
    elif mesaj_sayisi < 20:
        seviye = "Aktif zihin"
    else:
        seviye = "Özel kullanıcı"
    return f"🧠 KULLANICI ANALİZİ\nSeviye: {seviye}\nMesaj sayısı: {mesaj_sayisi}\nSonuç: Seni tanımaya başlıyorum."

# --- ANA DÖNGÜ ---
offset = 0
while True:
    try:
        # Long Polling: timeout ekleyerek bağlantıyı stabil tuttuk
        r = requests.get(TG_URL + f"getUpdates?offset={offset}&timeout=20").json()
        if "result" in r:
            for update in r["result"]:
                offset = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    user_id = update["message"]["from"]["id"]
                    text = update["message"]["text"]
                    
                    if text == "/start":
                        msg = "🧠 GERÇEK AI AKTİF\nArtık seninle konuşabilirim. Sor bana."
                    elif text == "/analiz":
                        msg = analiz(user_id)
                    else:
                        msg = chatgpt_reply(user_id, text)
                    
                    requests.get(TG_URL + f"sendMessage?chat_id={chat_id}&text={msg}")
    except Exception as e:
        print("Döngü hatası:", e)
        time.sleep(2)
