import json
import os

filepath = os.path.join(os.path.dirname(__file__), "..", "data", "trade_history.json")

with open(filepath, "r", encoding="utf-8") as f:
    trades = json.load(f)

order_ids = [t["order_id"] for t in trades]
print("Tất cả các Order ID trong data/trade_history.json:")
for t in trades:
    print(f"Order ID: {t['order_id']} | Symbol: {t['symbol']} | PnL: ${t['pnl_usd']} | Hour: {t['hour']}h ({t['date_str']})")

print("\nKiểm tra Order ID 49221337315 (ETH 5:10 PM):", "49221337315" in order_ids)
print("Kiểm tra Order ID 17639080380 (SOL 5:27 PM):", "17639080380" in order_ids)
