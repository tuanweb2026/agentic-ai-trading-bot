"""
Module PnL Analytics & 60-Day Performance Tracker.
Lưu trữ và phân tích dữ liệu PnL giao dịch hàng ngày (T2 - CN), 24h timeline, tổng kết tuần, tháng & 60 ngày.
"""
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

class PnLTracker:
    def __init__(self, data_file: str = "data/trade_history.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self._init_data_file()

    def _init_data_file(self):
        """Khởi tạo file dữ liệu lịch sử giao dịch ban đầu với dữ liệu mẫu chuẩn"""
        initial_trades = [
            {
                "order_id": "17610915144",
                "symbol": "SOL/USDT",
                "side": "SELL",
                "amount_usd": 80.00,
                "pnl_usd": 1.88,
                "timestamp": int(time.time() - 86400 * 2),
                "date_str": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                "hour": 15
            },
            {
                "order_id": "8742823966",
                "symbol": "ADA/USDT",
                "side": "SELL",
                "amount_usd": 80.00,
                "pnl_usd": 1.04,
                "timestamp": int(time.time() - 86400 * 2),
                "date_str": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                "hour": 15
            },
            {
                "order_id": "17617577413",
                "symbol": "SOL/USDT",
                "side": "SELL",
                "amount_usd": 80.00,
                "pnl_usd": 1.89,
                "timestamp": int(time.time() - 86400),
                "date_str": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                "hour": 9
            }
        ]
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(initial_trades, f, indent=2, ensure_ascii=False)

    def load_trades(self) -> List[Dict[str, Any]]:
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def record_trade(self, symbol: str, side: str, amount_usd: float, pnl_usd: float, order_id: str = "") -> Dict[str, Any]:
        """Ghi nhận một giao dịch mới thành công vào file lịch sử"""
        trades = self.load_trades()
        
        # Tránh ghi trùng lặp theo Order ID
        if order_id and any(t.get("order_id") == str(order_id) for t in trades):
            return {"success": False, "reason": "Lệnh đã tồn tại trong lịch sử"}

        now = datetime.now()
        trade_entry = {
            "order_id": str(order_id or int(time.time() * 1000)),
            "symbol": symbol,
            "side": side,
            "amount_usd": round(amount_usd, 2),
            "pnl_usd": round(pnl_usd, 2),
            "timestamp": int(time.time()),
            "date_str": now.strftime("%Y-%m-%d"),
            "day_name": now.strftime("%A"), # Monday, Tuesday...
            "hour": now.hour
        }
        
        trades.append(trade_entry)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(trades, f, indent=2, ensure_ascii=False)

        return {"success": True, "trade": trade_entry}

    def get_analytics(self) -> Dict[str, Any]:
        """Tính toán toàn bộ số liệu báo cáo Ngày (T2-CN), Tuần, Tháng, Win Rate %, Best/Worst Day"""
        trades = self.load_trades()
        now = datetime.now()

        total_trades = len(trades)
        winning_trades = [t for t in trades if t.get("pnl_usd", 0) > 0]
        losing_trades = [t for t in trades if t.get("pnl_usd", 0) < 0]
        
        win_rate = round((len(winning_trades) / total_trades * 100), 1) if total_trades > 0 else 0.0
        total_pnl = round(sum(t.get("pnl_usd", 0) for t in trades), 2)

        # Gom nhóm PnL theo từng Ngày (YYYY-MM-DD)
        daily_map: Dict[str, Dict[str, Any]] = {}
        for t in trades:
            d_str = t.get("date_str", "")
            if not d_str:
                continue
            if d_str not in daily_map:
                dt_obj = datetime.strptime(d_str, "%Y-%m-%d")
                daily_map[d_str] = {
                    "date_str": d_str,
                    "day_name_vi": self._translate_day_vi(dt_obj.strftime("%A")),
                    "pnl_usd": 0.0,
                    "trades_count": 0,
                    "wins": 0,
                    "losses": 0,
                    "hourly": {h: 0.0 for h in range(24)}
                }
            
            pnl = t.get("pnl_usd", 0)
            hour = t.get("hour", 0)
            daily_map[d_str]["pnl_usd"] += pnl
            daily_map[d_str]["trades_count"] += 1
            if pnl > 0:
                daily_map[d_str]["wins"] += 1
            elif pnl < 0:
                daily_map[d_str]["losses"] += 1
            
            daily_map[d_str]["hourly"][hour] += pnl

        # Làm tròn dữ liệu daily
        for d_str in daily_map:
            daily_map[d_str]["pnl_usd"] = round(daily_map[d_str]["pnl_usd"], 2)
            for h in range(24):
                daily_map[d_str]["hourly"][h] = round(daily_map[d_str]["hourly"][h], 2)

        # Bảng tuần này (7 ngày Thứ 2 -> Chủ Nhật)
        start_of_week = now - timedelta(days=now.weekday()) # Monday
        weekly_days = []
        weekly_pnl = 0.0

        for i in range(7):
            day_dt = start_of_week + timedelta(days=i)
            day_str = day_dt.strftime("%Y-%m-%d")
            day_data = daily_map.get(day_str, {
                "date_str": day_str,
                "day_name_vi": self._translate_day_vi(day_dt.strftime("%A")),
                "pnl_usd": 0.0,
                "trades_count": 0,
                "wins": 0,
                "losses": 0,
                "hourly": {h: 0.0 for h in range(24)}
            })
            weekly_days.append(day_data)
            weekly_pnl += day_data["pnl_usd"]

        # Thống kê Ngày Lời Nhiều Nhất (Best Day) & Ngày Lời Ít Nhất / Lỗ (Worst Day)
        sorted_days = sorted(daily_map.values(), key=lambda x: x["pnl_usd"], reverse=True)
        best_day = sorted_days[0] if sorted_days else None
        worst_day = sorted_days[-1] if sorted_days else None

        # Phân bổ 24h của ngày hôm nay
        today_str = now.strftime("%Y-%m-%d")
        today_data = daily_map.get(today_str, {
            "date_str": today_str,
            "day_name_vi": self._translate_day_vi(now.strftime("%A")),
            "pnl_usd": 0.0,
            "trades_count": 0,
            "wins": 0,
            "losses": 0,
            "hourly": {h: 0.0 for h in range(24)}
        })

        return {
            "total_trades": total_trades,
            "win_rate_pct": win_rate,
            "total_pnl_usd": total_pnl,
            "weekly_pnl_usd": round(weekly_pnl, 2),
            "weekly_days": weekly_days,
            "today": today_data,
            "best_day": best_day,
            "worst_day": worst_day,
            "history_60_days": list(daily_map.values())[-60:]
        }

    def _translate_day_vi(self, day_en: str) -> str:
        translations = {
            "Monday": "Thứ Hai",
            "Tuesday": "Thứ Ba",
            "Wednesday": "Thứ Tư",
            "Thursday": "Thứ Năm",
            "Friday": "Thứ Sáu",
            "Saturday": "Thứ Bảy",
            "Sunday": "Chủ Nhật"
        }
        return translations.get(day_en, day_en)

pnl_tracker = PnLTracker()
