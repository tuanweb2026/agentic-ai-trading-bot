import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange

class TestV54CoreEngine(unittest.TestCase):
    def test_01_core_step_sizes(self):
        """Kiểm tra làm tròn số lượng đối với 10 coin Core"""
        ex = LiveBinanceExchange()
        self.assertEqual(ex.format_quantity_by_step_size("BTC/USDT", 0.001239), 0.00123)
        self.assertEqual(ex.format_quantity_by_step_size("ETH/USDT", 0.03978), 0.0397)
        self.assertEqual(ex.format_quantity_by_step_size("SOL/USDT", 0.8529), 0.852)
        self.assertEqual(ex.format_quantity_by_step_size("AVAX/USDT", 10.458), 10.45)
        self.assertEqual(ex.format_quantity_by_step_size("ADA/USDT", 25.89), 25.8)
        print("✅ [TEST 1 PASSED] 10 Core coins LOT_SIZE precision verified!")

if __name__ == "__main__":
    unittest.main()
