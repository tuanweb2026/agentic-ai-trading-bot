import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pnl_tracker import pnl_tracker

# 1. Lệnh bán cắt lỗ ETH/USDT lúc 17:10 (Order ID: 49221337315, PnL: -$1.36 USD)
res1 = pnl_tracker.record_trade(
    symbol="ETH/USDT",
    side="SELL",
    amount_usd=100.00,
    pnl_usd=-1.36,
    order_id="49221337315"
)
print("Ghi nhận ETH:", res1)

# 2. Lệnh bán cắt lỗ SOL/USDT lúc 17:27 (Order ID: 17639080380, PnL: -$1.73 USD)
res2 = pnl_tracker.record_trade(
    symbol="SOL/USDT",
    side="SELL",
    amount_usd=80.00,
    pnl_usd=-1.73,
    order_id="17639080380"
)
print("Ghi nhận SOL:", res2)

analytics = pnl_tracker.get_analytics()
print("\nThống kê PnL Analytics mới nhất:", analytics)
