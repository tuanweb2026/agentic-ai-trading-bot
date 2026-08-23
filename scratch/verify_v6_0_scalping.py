import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pnl_tracker import pnl_tracker

class TestV60ScalpingEngine(unittest.TestCase):
    def test_01_v6_dedicated_logging(self):
        res = pnl_tracker.record_trade(
            symbol="ETH/USDT",
            side="SELL",
            amount_usd=100.0,
            pnl_usd=0.75,
            order_id="v6_test_order_001",
            version="v6.0"
        )
        self.assertTrue(res["success"])
        analytics = pnl_tracker.get_analytics()
        self.assertIn("v6_analytics", analytics)
        self.assertTrue(analytics["v6_analytics"]["v6_total_trades"] > 0)
        print("✅ [TEST 1 PASSED] v6.0 dedicated trade logging & analytics verified!")

if __name__ == "__main__":
    unittest.main()
