import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List

class PnLTracker:
    def __init__(self, data_file: str = None):
        if not data_file:
            data_file = os.path.join(os.path.dirname(__file__), "..", "data", "trade_history.json")
        self.data_file = os.path.abspath(data_file)
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.trades = self._load_trades()

    def _load_trades(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_trades(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.trades, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Error saving trades:", e)

    def record_trade(self, symbol: str, side: str, amount_usd: float, pnl_usd: float, order_id: str) -> Dict[str, Any]:
        """Ghi nhận lệnh giao dịch đã đóng. Nếu Order ID đã tồn tại với PnL=0, tự động cập nhật PnL thực tế."""
        order_id_str = str(order_id)
        if not order_id_str:
            return {"success": False, "reason": "Order ID rỗng"}

        # 🚀 KIỂM TRA XEM ORDER ID ĐÃ TỒN TẠI TRƯỚC ĐÓ CHƯA
        for t in self.trades:
            if str(t.get("order_id")) == order_id_str:
                # Nếu lệnh trước đó lưu PnL = 0.0 mà bây giờ có PnL thực tế khác 0 -> CẬP NHẬT PNL THỰC TẾ!
                if t.get("pnl_usd", 0.0) == 0.0 and pnl_usd != 0.0:
                    t["pnl_usd"] = round(pnl_usd, 2)
                    if amount_usd > 0:
                        t["amount_usd"] = round(amount_usd, 2)
                    self._save_trades()
                    return {"success": True, "updated": True, "trade": t}
                return {"success": False, "reason": "Lệnh đã tồn tại trong lịch sử"}

        now = datetime.now()
        timestamp = int(now.timestamp())
        date_str = now.strftime("%Y-%m-%d")
        day_name = now.strftime("%A")
        hour = now.hour

        trade = {
            "order_id": order_id_str,
            "symbol": symbol,
            "side": side.upper(),
            "amount_usd": round(amount_usd, 2),
            "pnl_usd": round(pnl_usd, 2),
            "timestamp": timestamp,
            "date_str": date_str,
            "day_name": day_name,
            "hour": hour
        }

        self.trades.append(trade)
        self._save_trades()
        return {"success": True, "trade": trade}

    def get_analytics(self) -> Dict[str, Any]:
        """Tổng hợp phân tích PnL hàng ngày (T2 -> CN), Biểu đồ 24h và Thống kê 60 ngày"""
        total_trades = len(self.trades)
        wins = [t for t in self.trades if t.get("pnl_usd", 0.0) > 0]
        losses = [t for t in self.trades if t.get("pnl_usd", 0.0) < 0]

        win_rate_pct = round((len(wins) / total_trades * 100), 1) if total_trades > 0 else 100.0
        total_pnl_usd = round(sum(t.get("pnl_usd", 0.0) for t in self.trades), 2)

        # Tính toán 7 ngày trong tuần hiện tại (từ Thứ 2 đến Chủ Nhật)
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())

        day_names_vi = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        weekly_days = []
        weekly_pnl = 0.0

        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_str = day_date.strftime("%Y-%m-%d")

            day_trades = [t for t in self.trades if t.get("date_str") == day_str]
            day_pnl = round(sum(t.get("pnl_usd", 0.0) for t in day_trades), 2)
            weekly_pnl += day_pnl

            day_wins = len([t for t in day_trades if t.get("pnl_usd", 0.0) > 0])
            day_losses = len([t for t in day_trades if t.get("pnl_usd", 0.0) < 0])

            hourly_map = {h: 0.0 for h in range(24)}
            for t in day_trades:
                h = t.get("hour", 0)
                hourly_map[h] = round(hourly_map.get(h, 0.0) + t.get("pnl_usd", 0.0), 2)

            weekly_days.append({
                "date_str": day_str,
                "day_name_vi": day_names_vi[i],
                "pnl_usd": day_pnl,
                "trades_count": len(day_trades),
                "wins": day_wins,
                "losses": day_losses,
                "hourly": hourly_map
            })

        # Phân tích ngày hôm nay
        today_str = today.strftime("%Y-%m-%d")
        today_trades = [t for t in self.trades if t.get("date_str") == today_str]
        today_pnl = round(sum(t.get("pnl_usd", 0.0) for t in today_trades), 2)
        today_hourly = {h: 0.0 for h in range(24)}
        for t in today_trades:
            h = t.get("hour", 0)
            today_hourly[h] = round(today_hourly.get(h, 0.0) + t.get("pnl_usd", 0.0), 2)

        today_summary = {
            "date_str": today_str,
            "day_name_vi": day_names_vi[today.weekday()],
            "pnl_usd": today_pnl,
            "trades_count": len(today_trades),
            "wins": len([t for t in today_trades if t.get("pnl_usd", 0.0) > 0]),
            "losses": len([t for t in today_trades if t.get("pnl_usd", 0.0) < 0]),
            "hourly": today_hourly
        }

        # Tìm ngày lời nhất (Best Day) và ngày lời ít nhất / lỗ nhất (Worst Day)
        days_grouped = {}
        for t in self.trades:
            d_str = t.get("date_str")
            if d_str not in days_grouped:
                days_grouped[d_str] = []
            days_grouped[d_str].append(t)

        best_day = None
        worst_day = None
        best_pnl = -999999.0
        worst_pnl = 999999.0

        for d_str, d_trades in days_grouped.items():
            d_pnl = round(sum(t.get("pnl_usd", 0.0) for t in d_trades), 2)
            d_obj = datetime.strptime(d_str, "%Y-%m-%d")
            d_name_vi = day_names_vi[d_obj.weekday()]

            summary_item = {
                "date_str": d_str,
                "day_name_vi": d_name_vi,
                "pnl_usd": d_pnl,
                "trades_count": len(d_trades),
                "wins": len([t for t in d_trades if t.get("pnl_usd", 0.0) > 0]),
                "losses": len([t for t in d_trades if t.get("pnl_usd", 0.0) < 0]),
            }

            if d_pnl > best_pnl:
                best_pnl = d_pnl
                best_day = summary_item

            if d_pnl < worst_pnl:
                worst_pnl = d_pnl
                worst_day = summary_item

        return {
            "total_trades": total_trades,
            "win_rate_pct": win_rate_pct,
            "total_pnl_usd": total_pnl_usd,
            "weekly_pnl_usd": round(weekly_pnl, 2),
            "weekly_days": weekly_days,
            "today": today_summary,
            "best_day": best_day,
            "worst_day": worst_day,
            "history_60_days": list(days_grouped.keys())[-60:]
        }

pnl_tracker = PnLTracker()
