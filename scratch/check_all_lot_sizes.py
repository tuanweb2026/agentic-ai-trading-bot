import urllib.request
import json

symbols = {
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", 
    "ADAUSDT", "AVAXUSDT", "NEARUSDT", "LINKUSDT", "DOTUSDT", 
    "INJUSDT", "PEPEUSDT", "ZECUSDT"
}

url = "https://api.binance.com/api/v3/exchangeInfo"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for s in data["symbols"]:
            sym = s["symbol"]
            if sym in symbols:
                for f in s["filters"]:
                    if f["filterType"] == "LOT_SIZE":
                        print(f"{sym:10s} -> minQty: {f['minQty']:12s} | stepSize: {f['stepSize']}")
except Exception as e:
    print("Lỗi:", e)
