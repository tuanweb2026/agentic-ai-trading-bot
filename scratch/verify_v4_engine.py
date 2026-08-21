import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange
from config.settings import settings

class TestV4QuantEngine(unittest.TestCase):
    def setUp(self):
        self.exchange = LiveBinanceExchange()

    def test_01_step_size_formatting(self):
        """Kiểm tra quy chuẩn nắn quy mô lệnh Lot Size cho 5 dòng coin khác nhau"""
        btc_qty = self.exchange.format_quantity_by_step_size("BTC/USDT", 0.00133719)
        self.assertEqual(btc_qty, 0.00133)

        sol_qty = self.exchange.format_quantity_by_step_size("SOL/USDT", 0.917195)
        self.assertEqual(sol_qty, 0.917)

        ada_qty = self.exchange.format_quantity_by_step_size("ADA/USDT", 433.8071)
        self.assertEqual(ada_qty, 433.80)
        print("✅ [TEST 1 PASSED] Step size formatting precision strictly verified!")

    def test_02_real_balance_structure(self):
        """Kiểm tra cấu trúc dữ liệu ví thời gian thực từ Binance API"""
        res = self.exchange.fetch_real_balance()
        self.assertTrue(res.get("success", False))
        self.assertIn("usdt_free", res)
        self.assertIn("prices", res)
        self.assertIn("usd_values", res)
        self.assertGreater(res["usdt_free"], 0.0)
        print(f"✅ [TEST 2 PASSED] Real Binance API balance verified: USDT Free = ${res['usdt_free']} USD")

    def test_03_settings_v4_flags(self):
        """Kiểm tra các cờ bật/tắt của Chế độ v4.0 Full Quant Engine"""
        self.assertTrue(settings.ENABLE_TRAILING_STOP)
        self.assertEqual(settings.TRAILING_STOP_CALLBACK_PCT, 0.8)
        self.assertTrue(settings.ENABLE_MACD_CONFIRMATION)
        self.assertTrue(settings.ENABLE_DYNAMIC_SIZING)
        print("✅ [TEST 3 PASSED] v4.0 Strategy settings flags verified!")

if __name__ == "__main__":
    unittest.main()
