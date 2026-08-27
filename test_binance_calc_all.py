import urllib.request
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.indicators import calculate_rsi, calculate_z_score_strain, calculate_macd, calculate_ema

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "NEARUSDT", "LINKUSDT", "DOTUSDT"]

print("=== LIVE INDICATORS CALCULATION TEST ===")
for sym in symbols:
    url = f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=5m&limit=50"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            klines = json.loads(resp.read().decode('utf-8'))
            closes = [float(k[4]) for k in klines]
            
            rsi = calculate_rsi(closes)
            z_score = calculate_z_score_strain(closes)
            macd = calculate_macd(closes)
            ema_20 = calculate_ema(closes, 20)
            
            print(f"Coin: {sym:8s} | Price: {closes[-1]:10.2f} | RSI: {rsi:6.2f} | Z-Score: {z_score:6.2f} | MACD: {macd:6.2f} | EMA20: {ema_20:10.2f}")
    except Exception as e:
        print(f"Error fetching {sym}: {e}")
