import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pnl_tracker import pnl_tracker

# Đồng bộ toàn bộ các lệnh bán chốt rực rỡ và bán cắt lỗ ròng thực tế từ Binance API 24h qua
trades_to_sync = [
    {"symbol": "SOL/USDT", "side": "SELL", "amount_usd": 80.00, "pnl_usd": -6.67, "order_id": "17633265135"},
    {"symbol": "ETH/USDT", "side": "SELL", "amount_usd": 100.00, "pnl_usd": -3.83, "order_id": "49209356244"},
    {"symbol": "SOL/USDT", "side": "SELL", "amount_usd": 80.00, "pnl_usd": -1.57, "order_id": "17633737178"},
    {"symbol": "ETH/USDT", "side": "SELL", "amount_usd": 100.00, "pnl_usd": -1.05, "order_id": "49210233428"}
]

for t in trades_to_sync:
    res = pnl_tracker.record_trade(t["symbol"], t["side"], t["amount_usd"], t["pnl_usd"], t["order_id"])
    print("Recorded:", res)

analytics = pnl_tracker.get_analytics()
print("\nUpdated Analytics:", analytics)
