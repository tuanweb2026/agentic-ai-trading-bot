import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.live_binance import LiveBinanceExchange

ex = LiveBinanceExchange()

bal = ex.fetch_real_balance()
inj_free = bal.get("balances", {}).get("INJ", 0.0)
print(f"Số lượng INJ khả dụng thực tế trên Binance: {inj_free} INJ")

if inj_free > 0:
    res = ex.create_spot_sell_order("INJ/USDT", inj_free)
    print("Kết quả đặt lệnh bán INJ:", res)
else:
    print("Không có INJ trong ví.")
