import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pnl_tracker import pnl_tracker

class TestPnLTracker(unittest.TestCase):
    def test_01_load_and_analytics(self):
        """Kiểm tra xem dữ liệu PnL Analytics có trả về đúng cấu trúc ngày, tuần, 24h không"""
        analytics = pnl_tracker.get_analytics()
        self.assertIn("total_trades", analytics)
        self.assertIn("win_rate_pct", analytics)
        self.assertIn("weekly_days", analytics)
        self.assertIn("today", analytics)
        self.assertIn("hourly", analytics["today"])
        self.assertEqual(len(analytics["weekly_days"]), 7)
        self.assertEqual(len(analytics["today"]["hourly"]), 24)
        print("✅ [TEST 1 PASSED] PnL Analytics & 24-Hour Timeline data structure verified!")

    def test_02_record_trade(self):
        """Kiểm tra hàm ghi nhận giao dịch mới và tính toán 24h PnL"""
        res = pnl_tracker.record_trade("SOL/USDT", "SELL", 80.00, 2.15, "test_order_99999")
        self.assertTrue(res.get("success", False))
        
        analytics = pnl_tracker.get_analytics()
        self.assertGreaterEqual(analytics["total_trades"], 1)
        print(f"✅ [TEST 2 PASSED] Recorded new trade! Total Trades: {analytics['total_trades']}, Win Rate: {analytics['win_rate_pct']}%")

if __name__ == "__main__":
    unittest.main()
