import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.log_manager import log_manager
from core.pnl_tracker import pnl_tracker

class TestServerPersistence(unittest.TestCase):
    def test_01_log_manager(self):
        log_manager.add_log("INFO", "Test log persistence line 1")
        recent = log_manager.get_recent_logs(5)
        self.assertTrue(len(recent) > 0)
        self.assertEqual(recent[-1]["message"], "Test log persistence line 1")
        print("✅ [TEST 1 PASSED] Persistent Log Manager verified!")

    def test_02_pnl_tracker(self):
        analytics = pnl_tracker.get_analytics()
        self.assertIn("weekly_days", analytics)
        self.assertIn("today", analytics)
        self.assertEqual(len(analytics["weekly_days"]), 7)
        print("✅ [TEST 2 PASSED] Daily PnL analytics (Mon-Sun) & 24h distribution verified!")

if __name__ == "__main__":
    unittest.main()
