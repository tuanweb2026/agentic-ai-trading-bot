import urllib.request
import json

url = "https://api.binance.com/api/v3/exchangeInfo?symbol=INJUSDT"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        symbol_info = data["symbols"][0]
        print("Symbol:", symbol_info["symbol"])
        for f in symbol_info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                print("LOT_SIZE Filter:", f)
            elif f["filterType"] == "MIN_NOTIONAL" or f["filterType"] == "NOTIONAL":
                print("NOTIONAL Filter:", f)
except Exception as e:
    print("Lỗi:", e)
