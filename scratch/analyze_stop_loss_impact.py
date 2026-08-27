import json
import os

filepath = os.path.join(os.path.dirname(__file__), "..", "data", "trade_history.json")

with open(filepath, "r", encoding="utf-8") as f:
    trades = json.load(f)

losses = [t for t in trades if t.get("pnl_usd", 0.0) < 0]
total_losses = len(losses)

print("=== STOP LOSS DISTRIBUTION ANALYTICS ===")
print(f"Tổng số lệnh âm/cắt lỗ: {total_losses}")

mid_losses = [t for t in losses if -2.0 <= t.get("pnl_usd", 0.0) <= -1.10]
large_losses = [t for t in losses if t.get("pnl_usd", 0.0) < -2.0]

print(f"Số lệnh âm nằm trong khoảng từ -$1.10 đến -$2.00: {len(mid_losses)}")
print(f"Số lệnh âm nặng hơn -$2.00: {len(large_losses)}")

print("\nChi tiết các lệnh cắt lỗ gần đây nhất:")
for t in trades[-15:]:
    pnl = t.get("pnl_usd", 0.0)
    if pnl < 0:
        print(f"Order: {t['order_id']} | Coin: {t['symbol']} | PnL: ${pnl} | Hour: {t['hour']}h")
