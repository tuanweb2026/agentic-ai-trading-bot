from core.live_binance import LiveBinanceExchange

exchange = LiveBinanceExchange()
res = exchange.fetch_real_balance()
print("TOTAL PORTFOLIO USD:", res.get("total_portfolio_usd"))
print("USDT FREE:", res.get("usdt_free"))
print("BALANCES:", res.get("balances"))
