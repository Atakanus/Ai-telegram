import requests
import time
import json

TOKEN = "BURAYA_BOT_TOKEN"
URL = f"https://api.telegram.org/bot{"8483969480:AAGlFsDGFu1aMOSpwDyTgzuySmsfGEQYK7U"}/"

beyin = {"ogrenilenler":{}}

def mesaj_gonder(chat_id, text):
    requests.get(URL+"sendMessage", params={"chat_id":chat_id,"text":text})

def ogren(konu):
    try:
        r = requests.get(f"https://tr.wikipedia.org/api/rest_v1/page/summary/{konu}")
        j = r.json()
        if "extract" in j:
            beyin["ogrenilenler"][konu]=j["extract"][:500]
    except:
        pass

def cevap(m):
    m=m.lower()
    for k,v in beyin["ogrenilenler"].items():
        if k in m:
            return v

    if len(m)>4:
        ogren(m)

    return "Öğreniyorum..."

def calis():
    offset=None
    while True:
        r = requests.get(URL+"getUpdates", params={"timeout":100,"offset":offset}).json()
        for u in r["result"]:
            offset=u["update_id"]+1
            chat=u["message"]["chat"]["id"]
            text=u["message"].get("text","")
            mesaj_gonder(chat, cevap(text))
        time.sleep(1)

calis()
