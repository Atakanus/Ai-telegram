import requests
import time
import json
import random

# --- AYARLAR ---
TELEGRAM_TOKEN = "8483969480:AAGlFsDGFu1aMOSpwDyTgzuySmsfGEQYK7U"
OPENAI_KEY = "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"

TG_URL = f"https://api.telegram.org/bot{"8483969480:AAGlFsDGFu1aMOSpwDyTgzuySmsfGEQYK7U"}/"
GPT_URL = "https://api.openai.com/v1/chat/completions"

print("🧠 V600 GERÇEK AI AKTİF")

offset = 0

# --- HAFIZA ---
try:
    with open("memory.json","r") as f:
        memory = json.load(f)
except:
    memory = {}

def save():
    with open("memory.json","w") as f:
        json.dump(memory,f)

# --- CHATGPT BEYİN ---
def chatgpt_reply(user_id, text):

    uid = str(user_id)
    if uid not in memory:
        memory[uid] = {"history":[]}

    memory[uid]["history"].append({"role":"user","content":text})
    memory[uid]["history"] = memory[uid]["history"][-6:]

    messages = [
        {"role":"system","content":
        "Sen zeki, karizmatik, hafızalı bir yapay zekasın. Kullanıcıyla doğal konuş. Kısa ve etkileyici cevaplar ver."}
    ] + memory[uid]["history"]

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model":"gpt-4o-mini",
        "messages":messages,
        "temperature":0.9
    }

    try:
        r = requests.post(GPT_URL, headers=headers, json=data).json()
        reply = r["choices"][0]["message"]["content"]

        memory[uid]["history"].append({"role":"assistant","content":reply})
        save()

        return reply

    except Exception as e:
        print("GPT hata:",e)
        return "Zihin bağlantım koptu..."

# --- ANALİZ KOMUTU ---
def analiz(user_id):
    uid=str(user_id)

    if uid not in memory:
        return "Henüz veri yok."

    mesaj = len(memory[uid]["history"])

    if mesaj < 5:
        seviye="Yeni kullanıcı"
    elif mesaj < 20:
        seviye="Aktif zihin"
    else:
        seviye="Özel kullanıcı"

    return f"""🧠 KULLANICI ANALİZİ

Seviye: {seviye}
Mesaj sayısı: {mesaj}

Sonuç:
Seni tanımaya başlıyorum."""

# --- LOOP ---
while True:
    try:
        r = requests.get(TG_URL + f"getUpdates?offset={offset}").json()

        for update in r["result"]:
            offset = update["update_id"] + 1

            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                user_id = update["message"]["from"]["id"]
                text = update["message"].get("text","")

                if text == "/start":
                    msg = """🧠 GERÇEK AI AKTİF

Artık seninle konuşabilirim.
Sor bana."""

                elif text == "/analiz":
                    msg = analiz(user_id)

                else:
                    msg = chatgpt_reply(user_id,text)

                requests.get(TG_URL + f"sendMessage?chat_id={chat_id}&text={msg}")

    except Exception as e:
        print("Hata:",e)

    time.sleep(1)
