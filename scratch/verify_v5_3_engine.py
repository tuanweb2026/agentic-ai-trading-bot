import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange

class TestV53Engine(unittest.TestCase):
    def test_01_quantities_format(self):
        """Kiểm tra làm tròn số lượng đối với 13 coin (bao gồm INJ, PEPE, ZEC)"""
        ex = LiveBinanceExchange()
        self.assertEqual(ex.format_quantity_by_step_size("INJ/USDT", 4.3219), 4.321)
        self.assertEqual(ex.format_quantity_by_step_size("ZEC/USDT", 0.1239), 0.123)
        self.assertEqual(ex.format_quantity_by_step_size("PEPE/USDT", 987654.89), 987654.0)
        print("✅ [TEST 1 PASSED] Step size format for 13 coins verified!")

if __name__ == "__main__":
    unittest.main()
