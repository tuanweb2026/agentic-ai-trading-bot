from pods.pod_base import BasePod
from typing import Dict, Any

class TrendFollowingPod(BasePod):
    """
    Pod Giao dịch theo Xu Hướng trên Thị trường BINANCE SPOT.
    """
    def __init__(self, pod_id: str, symbol: str, allocated_capital: float):
        super().__init__(pod_id, symbol, allocated_capital)
        self.sharpe_ratio = 1.10

    def evaluate(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        price = market_data.get("price", 0.0)
        ema_20 = market_data.get("ema_20", 0.0)
        macd = market_data.get("macd", 0.0)
        
        signal = "NEUTRAL"
        reasoning = ""

        if price > ema_20 and macd > 0:
            signal = "BUY"
            reasoning = f"[BINANCE SPOT] Giá cao hơn EMA20 và MACD dương. Xu hướng Spot tăng điểm, MUA Spot."
        elif price < ema_20 and macd < 0:
            signal = "SELL"
            reasoning = f"[BINANCE SPOT] Giá giảm dưới EMA20 và MACD âm. BÁN chốt Spot về USDT."
        else:
            signal = "NEUTRAL"
            reasoning = f"[BINANCE SPOT] Xu hướng Spot đi ngang. Đứng ngoài quan sát."

        return {
            "pod_id": self.pod_id,
            "strategy": "Trend Following (Spot)",
            "symbol": self.symbol,
            "signal": signal,
            "sharpe_ratio": self.sharpe_ratio,
            "reasoning": reasoning
        }
