from pods.pod_base import BasePod
from typing import Dict, Any

class MeanReversionPod(BasePod):
    """
    Pod Giao dịch Đảo chiều Trung bình trên Thị trường BINANCE SPOT.
    - Spot BUY: Khi Z-Score < -2.0 và RSI < 30 (Sợi dây thun bị nén quá bán) ➔ Mua tích sản Spot.
    - Spot SELL: Khi Z-Score > 2.0 và RSI > 70 (Sợi dây thun căng quá mua) ➔ Bán chốt lời Spot ra USDT.
    """
    def __init__(self, pod_id: str, symbol: str, allocated_capital: float):
        super().__init__(pod_id, symbol, allocated_capital)
        self.sharpe_ratio = 1.15

    def evaluate(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        z_score = market_data.get("z_score", 0.0)
        rsi = market_data.get("rsi", 50.0)
        signal = "NEUTRAL"
        reasoning = ""

        if z_score < -2.0 and rsi < 30:
            signal = "BUY"
            reasoning = f"[BINANCE SPOT] Sợi dây thun nén quá bán (Z-Score = {z_score:.2f}, RSI = {rsi:.1f}). Đề xuất MUA tích sản Spot."
        elif z_score > 2.0 and rsi > 70:
            signal = "SELL"
            reasoning = f"[BINANCE SPOT] Sợi dây thun căng quá mua (Z-Score = {z_score:.2f}, RSI = {rsi:.1f}). Đề xuất BÁN chốt lời ra USDT."
        else:
            signal = "NEUTRAL"
            reasoning = f"[BINANCE SPOT] Z-score = {z_score:.2f} bình thường. Quan sát thị trường Spot."

        return {
            "pod_id": self.pod_id,
            "strategy": "Mean Reversion (Spot Rubber Band)",
            "symbol": self.symbol,
            "signal": signal,
            "sharpe_ratio": self.sharpe_ratio,
            "reasoning": reasoning
        }
