import urllib.request
import urllib.parse
import hmac
import hashlib
import time
import json
from config.settings import settings

api_key = settings.BINANCE_API_KEY
secret_key = settings.BINANCE_SECRET_KEY

ts = int(time.time() * 1000)
query = f"timestamp={ts}"
sig = hmac.new(secret_key.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
url = f"https://api.binance.com/api/v3/account?{query}&signature={sig}"

req = urllib.request.Request(url, headers={"X-MBX-APIKEY": api_key, "User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        balances = data.get('balances', [])
        print("--- BINANCE ACCOUNT BALANCES ---")
        for b in balances:
            free = float(b['free'])
            locked = float(b['locked'])
            if free > 0 or locked > 0:
                print(f"ASSET: {b['asset']} | FREE: {free} | LOCKED: {locked}")
except Exception as e:
    print("NATIVE_ERROR:", str(e))
