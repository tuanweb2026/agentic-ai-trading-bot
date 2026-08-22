import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange

exchange = LiveBinanceExchange()

print("=== 1. ĐỐI SOÁT VÍ TIỀN MẶT VÀ TỔNG TÀI SẢN TỪ BINANCE API ===")
bal = exchange.fetch_real_balance()
print(f"USDT Free: ${bal.get('usdt_free')} USDT")
print(f"Total Portfolio USD: ${bal.get('total_portfolio_usd')} USD")
print("Balances:", bal.get('balances'))
print("USD Values:", bal.get('usd_values'))
print("Prices:", bal.get('prices'))

print("\n=== 2. QUÉT LỊCH SỬ TẤT CẢ LỆNH GIAO DỊCH TRÊN SÀN BINANCE 24H QUA ===")
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "BNBUSDT", "AVAXUSDT", "NEARUSDT", "LINKUSDT", "XRPUSDT", "DOTUSDT"]

recent_orders = []
for sym in symbols:
    res = exchange._signed_request("GET", "/api/v3/allOrders", {"symbol": sym, "limit": 10})
    if isinstance(res, list):
        for o in res:
            # Lấy các lệnh đã khớp (FILLED)
            if o.get("status") == "FILLED":
                t_str = datetime.fromtimestamp(o["time"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                recent_orders.append({
                    "symbol": sym,
                    "orderId": o.get("orderId"),
                    "side": o.get("side"),
                    "qty": o.get("executedQty"),
                    "quoteQty": o.get("cummulativeQuoteQty"),
                    "time": t_str,
                    "timestamp": o.get("time")
                })

# Sắp xếp theo thời gian mới nhất
recent_orders.sort(key=lambda x: x["timestamp"], reverse=True)

print(f"Tìm thấy tổng cộng {len(recent_orders)} lệnh FILLED gần đây:")
for o in recent_orders[:15]:
    print(f"[{o['time']}] {o['side']} {o['symbol']} | Qty: {o['qty']} | Value: ${o['quoteQty']} USDT | Order ID: {o['orderId']}")
