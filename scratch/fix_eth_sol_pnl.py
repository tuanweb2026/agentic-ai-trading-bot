import json
import os

filepath = os.path.join(os.path.dirname(__file__), "..", "data", "trade_history.json")

with open(filepath, "r", encoding="utf-8") as f:
    trades = json.load(f)

for t in trades:
    if t.get("order_id") == "49221337315":
        t["pnl_usd"] = -1.36
    elif t.get("order_id") == "17639080380":
        t["pnl_usd"] = -1.73

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(trades, f, indent=2, ensure_ascii=False)

print("Đã cập nhật PnL thực tế cho ETH (-$1.36) và SOL (-$1.73) trong data/trade_history.json!")
