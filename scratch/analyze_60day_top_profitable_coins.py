import urllib.request
import json
import time
import math
from datetime import datetime, timedelta

def fetch_klines(symbol, interval="1d", limit=60):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            closes = [float(k[4]) for k in data]
            highs = [float(k[2]) for k in data]
            lows = [float(k[3]) for k in data]
            return closes, highs, lows
    except Exception as e:
        return [], [], []

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return [50.0] * len(prices)
    
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(diff))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    rsis = [50.0] * period
    for i in range(period, len(prices) - 1):
        avg_gain = (avg_gain * 13 + gains[i]) / 14.0
        avg_loss = (avg_loss * 13 + losses[i]) / 14.0
        if avg_loss == 0:
            rsis.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsis.append(100.0 - (100.0 / (1.0 + rs)))
    return rsis

def calculate_zscore(prices, window=20):
    zscores = [0.0] * len(prices)
    for i in range(window, len(prices)):
        slice_p = prices[i-window:i]
        mean = sum(slice_p) / window
        variance = sum((x - mean) ** 2 for x in slice_p) / window
        std = math.sqrt(variance)
        if std > 0:
            zscores[i] = (prices[i] - mean) / std
        else:
            zscores[i] = 0.0
    return zscores

# 20 Cặp Coin Spot Phổ Biến Hàng Đầu Trên Binance
candidates = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "BNBUSDT", 
    "AVAXUSDT", "ADAUSDT", "LINKUSDT", "DOTUSDT", "XRPUSDT",
    "SUIUSDT", "FETUSDT", "PEPEUSDT", "APTUSDT", "INJUSDT",
    "TIAUSDT", "SEIUSDT", "RENDERUSDT", "TAOUSDT", "WIFUSDT"
]

results = []

for sym in candidates:
    closes, highs, lows = fetch_klines(sym, interval="1d", limit=60)
    if len(closes) < 30:
        continue

    rsis = calculate_rsi(closes)
    zscores = calculate_zscore(closes)

    # Giả lập Chiến lược Quant v5.2 với vốn $80 USD / lệnh
    base_usd = 80.00
    in_position = False
    entry_price = 0.0
    total_pnl = 0.0
    win_trades = 0
    loss_trades = 0

    for i in range(20, len(closes)):
        price = closes[i]
        rsi = rsis[i] if i < len(rsis) else 50.0
        z = zscores[i] if i < len(zscores) else 0.0

        if not in_position:
            # Điều kiện Mua
            if z < -1.8 or rsi < 38:
                in_position = True
                entry_price = price
        else:
            # Kiểm tra Take Profit (+2.8%) hoặc Stop Loss (-1.4%)
            pnl_pct = ((price - entry_price) / entry_price) * 100
            if pnl_pct >= 2.8:
                pnl_usd = base_usd * (pnl_pct / 100)
                total_pnl += pnl_usd
                win_trades += 1
                in_position = False
            elif pnl_pct <= -1.4:
                pnl_usd = base_usd * (pnl_pct / 100)
                total_pnl += pnl_usd
                loss_trades += 1
                in_position = False

    total_trades = win_trades + loss_trades
    win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0.0

    results.append({
        "symbol": sym.replace("USDT", "/USDT"),
        "total_pnl_usd": round(total_pnl, 2),
        "total_trades": total_trades,
        "win_trades": win_trades,
        "loss_trades": loss_trades,
        "win_rate_pct": round(win_rate, 1),
        "avg_profit_per_trade": round(total_pnl / total_trades, 2) if total_trades > 0 else 0.0
    })

# Sắp xếp theo tổng lợi nhuận ($) cao nhất
results.sort(key=lambda x: x["total_pnl_usd"], reverse=True)

print("=== BÁO CÁO RANKING TOP 10 COIN SINH LỜI NHIỀU NHẤT TRONG 60 NGÀY QUA ===")
for idx, r in enumerate(results[:10], 1):
    print(f"Top {idx:2d}: {r['symbol']:10s} | Tổng Lãi: +${r['total_pnl_usd']:6.2f} USD | Win Rate: {r['win_rate_pct']:5.1f}% | Số Lệnh: {r['win_trades']} Thắng / {r['loss_trades']} Thua | Lãi TRB: +${r['avg_profit_per_trade']:.2f}/lệnh")
