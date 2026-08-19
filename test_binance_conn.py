import ccxt
from config.settings import settings

print("Checking API Key...", settings.BINANCE_API_KEY[:8])
try:
    ex = ccxt.binance({
        'apiKey': settings.BINANCE_API_KEY,
        'secret': settings.BINANCE_SECRET_KEY,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    bal = ex.fetch_balance()
    usdt = bal.get('free', {}).get('USDT', 0.0)
    total = bal.get('total', {}).get('USDT', 0.0)
    print(f"RESULT_USDT_FREE: {usdt}")
    print(f"RESULT_USDT_TOTAL: {total}")
except Exception as e:
    print(f"RESULT_ERROR: {e}")
