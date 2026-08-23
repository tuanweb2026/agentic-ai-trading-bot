import json
import os
import sys

filepath = os.path.join(os.path.dirname(__file__), "..", "data", "trade_history.json")

with open(filepath, "r", encoding="utf-8") as f:
    trades = json.load(f)

print("=== DEEP QUANT AUDIT OF RECENT TRADES ===")
print(f"Tổng số lệnh đã lưu: {len(trades)}")

wins = [t for t in trades if t.get("pnl_usd", 0.0) > 0]
losses = [t for t in trades if t.get("pnl_usd", 0.0) < 0]

print(f"Lệnh Thắng: {len(wins)} | Lệnh Thua: {len(losses)}")

total_win_amount = sum(t["pnl_usd"] for t in wins)
total_loss_amount = sum(t["pnl_usd"] for t in losses)

print(f"Tổng Lãi từ lệnh Thắng: +${total_win_amount:.2f} USD")
print(f"Tổng Lỗ từ lệnh Thua: -${abs(total_loss_amount):.2f} USD")
if len(wins) > 0:
    print(f"Lãi Trung Bình / Lệnh Thắng: +${total_win_amount / len(wins):.2f} USD")
if len(losses) > 0:
    print(f"Lỗ Trung Bình / Lệnh Thua: -${abs(total_loss_amount) / len(losses):.2f} USD")

print("\n--- CHI TIẾT TỪNG LỆNH ---")
for i, t in enumerate(trades, 1):
    symbol = t.get("symbol")
    pnl = t.get("pnl_usd")
    date_str = t.get("date_str")
    hour = t.get("hour")
    print(f"Lệnh #{i:02d} | {symbol:10s} | PnL: ${pnl:+6.2f} USD | Ngày: {date_str} {hour:02d}h")
