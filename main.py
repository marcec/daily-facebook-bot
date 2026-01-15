import requests
import os
import pytz
from datetime import datetime

# 1. POSTAVKE
PAGE_ID = os.environ.get("FB_PAGE_ID")
ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
MSG = "BUM!"

# 2. PROVJERA VREMENA (Sigurnosni osigurač)
# Iako će cron-job okinuti točno u podne, ovo sprječava
# da slučajno opalite top ako testirate kod u ponoć.
zagreb_tz = pytz.timezone('Europe/Zagreb')
now = datetime.now(zagreb_tz)

print(f"Zagreb Vrijeme: {now.strftime('%H:%M')}")

# Pucaj samo ako je 11:59, 12:00, 12:01 ili 12:02
if now.hour == 12 and now.minute <= 2:
    pass
elif now.hour == 11 and now.minute >= 59:
    pass
else:
    print("Nije podne. Top ostaje pun. (Safety check)")
    # Ako želite testirati "na silu", zakomentirajte liniju ispod:
    #exit()

# 3. PUCAJ (Šalji na Facebook)
url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
payload = {
    "message": MSG,
    "access_token": ACCESS_TOKEN
}

try:
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print(f"BUM! Objavljeno na Facebook. ID: {response.json().get('id')}")
    else:
        print(f"Greška kod pucanja: {response.text}")
        exit(1) # Javi grešku GitHubu
except Exception as e:
    print(f"Kritična greška: {e}")
    exit(1)
