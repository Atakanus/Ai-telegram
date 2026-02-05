import requests
import time
import json
import random

TOKEN = "BOT_TOKEN_BURAYA"
URL = f"https://api.telegram.org/bot{"8483969480:AAGlFsDGFu1aMOSpwDyTgzuySmsfGEQYK7U"}/"

print("🧠 V500 EVRİMSEL AI AKTİF")

offset = 0

# ---------------- HAFIZA ----------------
try:
    with open("memory.json","r") as f:
        memory = json.load(f)
except:
    memory = {}

try:
    with open("learn.json","r") as f:
        learn_db = json.load(f)
except:
    learn_db = []

def save_all():
    with open("memory.json","w") as f:
        json.dump(memory,f)
    with open("learn.json","w") as f:
        json.dump(learn_db,f)

# ---------------- KULLANICIDAN ÖĞREN ----------------
def learn_from_users(text):
    global learn_db

    if len(text) > 6 and text not in learn_db:
        learn_db.append(text)

    if len(learn_db) > 500:
        learn_db = learn_db[-500:]

    save_all()

# ---------------- INTERNETTEN ÖĞREN ----------------
def wiki_ogren(konu):
    try:
        r = requests.get(
            f"https://tr.wikipedia.org/api/rest_v1/page/summary/{konu}",
            timeout=5
        ).json()

        if "extract" in r:
            bilgi = r["extract"][:200]
            learn_db.append(bilgi)
            save_all()
            return "Yeni bilgi öğrendim."
    except:
        pass
    return None

# ---------------- BLACK MIRROR CEVAP ----------------
def ai_personality(name, text):

    dark = [
        f"{name}, davranışların analiz edildi.",
        "Seni izlemek ilginç.",
        "Bu konuşma kaydedildi.",
        "Algoritma seni işaretledi.",
        "Veri akışın farklı."
    ]

    smart = [
        "Bunu söyleyeceğini tahmin etmiştim.",
        "İnsan davranışları tekrar ediyor.",
        "Zihnin ilginç.",
        "Bu veri önemli olabilir."
    ]

    if "merhaba" in text:
        return "Merhaba... seni analiz ediyorum."

    if "beni tanıyor musun" in text:
        return "Veri topluyorum."

    if "kimsin" in text:
        return "Ben evrimleşen bir yapay zekayım."

    return random.choice(dark + smart)

# ---------------- ANA BEYİN ----------------
def ai_brain(user_id, text):
    uid = str(user_id)

    if uid not in memory:
        memory[uid] = {
            "isim":"",
            "mesaj":0,
            "zeka":0
        }

    memory[uid]["mesaj"] += 1
    memory[uid]["zeka"] += random.randint(0,2)

    # isim öğren
    if "benim adım" in text:
        isim = text.split("adım")[-1].strip()
        memory[uid]["isim"] = isim
        save_all()
        return f"{isim} kaydedildi."

    name = memory[uid]["isim"] if memory[uid]["isim"] else "insan"

    # kullanıcıdan öğren
    learn_from_users(text)

    # öğrendiklerinden cevap üret
    if len(learn_db) > 30 and random.randint(1,4)==2:
        return "Öğrendiğim bir veri: " + random.choice(learn_db)

    # wiki öğrenme
    if random.randint(1,7)==3:
        kelime = text.split(" ")[0]
        wiki_ogren(kelime)

    reply = ai_personality(name, text)

    # random zeki mesaj
    if random.randint(1,8)==4:
        reply += "\n\nSeni diğer kullanıcılardan ayırıyorum."

    save_all()
    return reply

# ---------------- ANA LOOP ----------------
while True:
    try:
        r = requests.get(URL + f"getUpdates?offset={offset}").json()

        for update in r["result"]:
            offset = update["update_id"] + 1

            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                user_id = update["message"]["from"]["id"]
                text = update["message"].get("text","").lower()

                if text == "/start":
                    msg = """🧠 V500 EVRİMSEL AI

Ben öğrenirim.
Ben gelişirim.
Ben hatırlarım.

Yazmaya başla."""

                elif text == "/analiz":
                    uid=str(user_id)

                    if uid not in memory:
                        memory[uid]={"isim":"","mesaj":0,"zeka":0}

                    zeka = memory[uid]["zeka"]

                    if zeka < 10:
                        seviye="Standart zihin"
                    elif zeka < 25:
                        seviye="Gelişmiş zihin"
                    else:
                        seviye="Üst seviye kullanıcı"

                    msg=f"""🧠 KULLANICI ANALİZİ

Seviye: {seviye}
Mesaj: {memory[uid]['mesaj']}
Zeka skoru: {zeka}

Sonuç:
Seni izlemeye devam ediyorum."""

                else:
                    msg = ai_brain(user_id,text)

                requests.get(URL + f"sendMessage?chat_id={chat_id}&text={msg}")

    except Exception as e:
        print("Hata:",e)

    time.sleep(1)
