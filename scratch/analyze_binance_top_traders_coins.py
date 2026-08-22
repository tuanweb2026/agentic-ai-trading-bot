import urllib.request
import json
import time

# Quét danh sách các coin Spot có khối lượng giao dịch và mức tăng trưởng PnL ấn tượng nhất 60 ngày qua trên Binance
url = "https://api.binance.com/api/v3/ticker/24hr"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        
    usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and float(d['quoteVolume']) > 10000000]
    
    # Lấy nến 60 ngày cho các coin Top Volume trên Binance
    rankings = []
    
    for item in usdt_pairs[:25]:
        sym = item['symbol']
        kline_url = f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=1d&limit=60"
        k_req = urllib.request.Request(kline_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(k_req, timeout=3) as k_resp:
                klines = json.loads(k_resp.read().decode('utf-8'))
                if len(klines) >= 60:
                    start_price = float(klines[0][4]) # Giá đóng cửa 60 ngày trước
                    current_price = float(klines[-1][4]) # Giá hiện tại
                    pct_change_60d = ((current_price - start_price) / start_price) * 100
                    quote_vol_24h = float(item['quoteVolume']) / 1000000 # Triệu USD
                    
                    rankings.append({
                        "symbol": sym.replace("USDT", "/USDT"),
                        "pct_change_60d": round(pct_change_60d, 2),
                        "start_price": start_price,
                        "current_price": current_price,
                        "vol_24h_m": round(quote_vol_24h, 2)
                    })
        except Exception:
            pass

    rankings.sort(key=lambda x: x['pct_change_60d'], reverse=True)
    
    print("=== BÁO CÁO THỐNG KÊ TOP 10 COIN TĂNG TRƯỞNG & LỜI NHIỀU NHẤT TRÊN SÀN BINANCE (60 NGÀY QUA) ===")
    for idx, r in enumerate(rankings[:10], 1):
        print(f"Top {idx:2d}: {r['symbol']:12s} | Tăng Trưởng 60d: +{r['pct_change_60d']:6.2f}% | Giá 60d trước: ${r['start_price']} -> Giá Hiện Tại: ${r['current_price']} | Vol 24h: ${r['vol_24h_m']}M USD")

except Exception as e:
    print("Lỗi:", e)
