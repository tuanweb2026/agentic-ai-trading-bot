from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePod(ABC):
    def __init__(self, pod_id: str, symbol: str, allocated_capital: float):
        self.pod_id = pod_id
        self.symbol = symbol
        self.allocated_capital = allocated_capital
        self.sharpe_ratio = 1.2  # Dynamic Sharpe metric

    @abstractmethod
    def evaluate(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Đánh giá thị trường và đưa ra tín hiệu Pod (Signal, Target Price, Stop Loss, Sharpe Ratio).
        """
        pass
