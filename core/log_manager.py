"""
Module Quản lý & Lưu trữ Bền Vững Nhật Ký Hệ Thống (Live Feed Logs) qua các lần Restart Server.
Lưu giữ tối đa 100 log mới nhất vào file `data/server_logs.json`.
"""
import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any

class LogManager:
    def __init__(self, data_file: str = None):
        if not data_file:
            data_file = os.path.join(os.path.dirname(__file__), "..", "data", "server_logs.json")
        self.data_file = os.path.abspath(data_file)
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.logs = self._load_logs()

    def _load_logs(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_logs(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.logs[-100:], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print("Error saving logs:", e)

    def add_log(self, type_str: str, message: str) -> Dict[str, Any]:
        """Thêm một dòng log mới và lưu bền vững vào đĩa"""
        now_str = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "type": type_str.upper(),
            "time": now_str,
            "message": message,
            "timestamp": int(time.time())
        }
        self.logs.append(log_entry)
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
        self._save_logs()
        return log_entry

    def get_recent_logs(self, limit: int = 35) -> List[Dict[str, Any]]:
        """Lấy danh sách log mới nhất để hiển thị lại trên khung Live Feed"""
        return self.logs[-limit:]

log_manager = LogManager()
