import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange

exchange = LiveBinanceExchange()

print("--- KIỂM TRA LỆNH MUA ETH/USDT ---")
res_buy = exchange._signed_request("GET", "/api/v3/order", {"symbol": "ETHUSDT", "orderId": 49153273221})
print("Lệnh Mua:", res_buy)

print("\n--- KIỂM TRA LỆNH BÁN ETH/USDT ---")
res_sell = exchange._signed_request("GET", "/api/v3/order", {"symbol": "ETHUSDT", "orderId": 49153274838})
print("Lệnh Bán:", res_sell)

print("\n--- LỊCH SỬ 5 LỆNH GẦN NHẤT ETH/USDT ---")
res_all = exchange._signed_request("GET", "/api/v3/allOrders", {"symbol": "ETHUSDT", "limit": 5})
print("Lịch sử lệnh ETH/USDT:", res_all)
