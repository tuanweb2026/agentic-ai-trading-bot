from core.live_binance import LiveBinanceExchange

exchange = LiveBinanceExchange()
# Test selling 0.01 SOL/USDT on Binance
res = exchange.create_spot_sell_order("SOL/USDT", 0.01)
print("TEST SELL SOL RESULT:", res)
