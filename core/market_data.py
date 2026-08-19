import time
import random
from typing import Dict, List, Any
from core.indicators import calculate_rsi, calculate_z_score_strain, calculate_macd, calculate_ema

class MarketDataEngine:
    def __init__(self, symbols: List[str] = None):
        self.symbols = symbols or [
            "BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT",
            "ADA/USDT", "AVAX/USDT", "NEAR/USDT", "LINK/USDT", "NVDA"
        ]
        self.price_history: Dict[str, List[float]] = {}
        for sym in self.symbols:
            self._init_symbol_history(sym)

    def _init_symbol_history(self, symbol: str, count: int = 50):
        base_prices = {
            "BTC/USDT": 65000.0,
            "ETH/USDT": 3500.0,
            "SOL/USDT": 150.0,
            "BNB/USDT": 580.0,
            "XRP/USDT": 0.58,
            "ADA/USDT": 0.38,
            "AVAX/USDT": 24.5,
            "NEAR/USDT": 4.25,
            "LINK/USDT": 11.8,
            "NVDA": 125.0
        }
        start = base_prices.get(symbol, 100.0)
        random.seed(hash(symbol) % 10000)
        prices = [start]
        for _ in range(count - 1):
            change = random.gauss(0, 0.005)
            prices.append(max(0.001, prices[-1] * (1 + change)))
        self.price_history[symbol] = prices

    def get_latest_ticker(self, symbol: str) -> Dict[str, float]:
        if symbol not in self.price_history:
            self._init_symbol_history(symbol)
            
        history = self.price_history[symbol]
        latest = max(0.001, history[-1] * (1 + random.gauss(0.0001, 0.003)))
        history.append(latest)
        if len(history) > 200:
            history.pop(0)

        rsi = calculate_rsi(history)
        z_score = calculate_z_score_strain(history)
        macd = calculate_macd(history)
        ema_20 = calculate_ema(history, 20)

        return {
            "symbol": symbol,
            "price": float(latest),
            "rsi": float(rsi),
            "z_score": float(z_score),
            "macd": float(macd),
            "ema_20": float(ema_20)
        }
