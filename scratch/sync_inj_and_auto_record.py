import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pnl_tracker import pnl_tracker

# Đồng bộ chính xác lệnh cắt lỗ INJ/USDT lúc 16:20 PM (Order ID: 3131893691)
res = pnl_tracker.record_trade(
    symbol="INJ/USDT",
    side="SELL",
    amount_usd=70.00,
    pnl_usd=-1.13,
    order_id="3131893691"
)

print("Đã ghi nhận lệnh INJ vào Báo Cáo PnL:", res)
analytics = pnl_tracker.get_analytics()
print("\nThống kê PnL Analytics mới nhất:", analytics)
