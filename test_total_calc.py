from core.live_binance import LiveBinanceExchange

exchange = LiveBinanceExchange()
bal = exchange.fetch_real_balance()
print("REAL BALANCE DATA:", bal)
