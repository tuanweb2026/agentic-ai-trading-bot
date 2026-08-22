import sys
import os
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange

exchange = LiveBinanceExchange()

seven_days_ago_ms = int((time.time() - 7 * 86400) * 1000)
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "BNBUSDT", "AVAXUSDT", "NEARUSDT", "LINKUSDT", "XRPUSDT", "DOTUSDT"]

coin_stats = {}

for sym in symbols:
    coin = sym.replace("USDT", "")
    res = exchange._signed_request("GET", "/api/v3/allOrders", {"symbol": sym, "startTime": seven_days_ago_ms, "limit": 1000})
    
    buy_count = 0
    sell_count = 0
    buy_vol_usd = 0.0
    sell_vol_usd = 0.0

    if isinstance(res, list):
        for o in res:
            if o.get("status") == "FILLED":
                quote_qty = float(o.get("cummulativeQuoteQty", 0.0))
                side = o.get("side")
                if side == "BUY":
                    buy_count += 1
                    buy_vol_usd += quote_qty
                elif side == "SELL":
                    sell_count += 1
                    sell_vol_usd += quote_qty

    coin_stats[coin] = {
        "buy_count": buy_count,
        "sell_count": sell_count,
        "total_orders": buy_count + sell_count,
        "buy_vol_usd": round(buy_vol_usd, 2),
        "sell_vol_usd": round(sell_vol_usd, 2),
        "total_vol_usd": round(buy_vol_usd + sell_vol_usd, 2)
    }

# Sắp xếp theo số lượt mua nhiều nhất
sorted_by_buys = sorted(coin_stats.items(), key=lambda x: x[1]["buy_count"], reverse=True)

print("=== BÁO CÁO THỐNG KÊ TẦN SUẤT GIAO DỊCH 7 NGÀY QUA TRÊN BINANCE API ===")
for coin, stats in sorted_by_buys:
    print(f"Coin: {coin:5s} | Mua: {stats['buy_count']:2d} lệnh (${stats['buy_vol_usd']:7.2f} USD) | Bán: {stats['sell_count']:2d} lệnh (${stats['sell_vol_usd']:7.2f} USD) | Tổng Lệnh: {stats['total_orders']:2d}")

