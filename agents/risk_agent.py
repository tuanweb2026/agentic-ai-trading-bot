from typing import Dict, Any
from config.settings import settings

class RiskManagementAgent:
    """
    Chief Risk Officer (CRO) Agent - Quản trị rủi ro cứng.
    Đảm bảo:
    1. Sharpe Ratio >= 1.0 (Loại trừ chiến lược Overfitted như video lưu ý).
    2. Total Drawdown không vượt quá MAX_DAILY_DRAWDOWN (5%).
    3. Tỷ lệ R:R >= 1.5.
    4. Tính toán Size vị thế chính xác (max 1% vốn per trade).
    """
    def __init__(self):
        self.name = "Risk-Officer-Agent"

    def evaluate_risk(self, proposed_signal: Dict[str, Any], portfolio_summary: Dict[str, Any]) -> Dict[str, Any]:
        drawdown_pct = portfolio_summary.get("drawdown_pct", 0.0) / 100.0
        sharpe_ratio = proposed_signal.get("sharpe_ratio", 0.0)
        action = proposed_signal.get("signal", "NEUTRAL")
        symbol = proposed_signal.get("symbol", "")
        
        # Rule 1: Kiểm tra Max Drawdown
        if drawdown_pct >= settings.MAX_DAILY_DRAWDOWN:
            return {
                "approved": False,
                "reason": f"CRITICAL: Drawdown hiện tại ({drawdown_pct*100:.2f}%) chạm giới hạn tối đa ({settings.MAX_DAILY_DRAWDOWN*100}%). Khóa mở vị thế mới!",
                "adjusted_amount": 0.0
            }

        # Rule 2: Bộ lọc Tỷ lệ Sharpe Ratio > 1.0 (Ngừa Overfitting)
        if action in ["BUY", "SELL"] and sharpe_ratio < settings.MIN_SHARPE_RATIO:
            return {
                "approved": False,
                "reason": f"REJECTED: Tỷ lệ Sharpe của Pod ({sharpe_ratio:.2f}) dưới ngưỡng tối thiểu ({settings.MIN_SHARPE_RATIO}). Chiến lược có nguy cơ bị Overfitted!",
                "adjusted_amount": 0.0
            }

        if action == "NEUTRAL":
            return {"approved": False, "reason": "Signal is NEUTRAL", "adjusted_amount": 0.0}

        # Rule 3: Tính toán Position Size (Max 1% vốn rủi ro)
        total_balance = portfolio_summary.get("total_portfolio_value", 10000.0)
        max_risk_amount = total_balance * settings.MAX_RISK_PER_POD
        price = proposed_signal.get("price", 100.0)
        
        if price <= 0:
            return {"approved": False, "reason": "Invalid asset price", "adjusted_amount": 0.0}
            
        calculated_amount = round(max_risk_amount / price, 4)

        return {
            "approved": True,
            "reason": f"APPROVED: Lệnh đáp ứng Sharpe Ratio > 1.0 ({sharpe_ratio:.2f}) và kiểm soát rủi ro {settings.MAX_RISK_PER_POD*100}% vốn.",
            "adjusted_amount": max(0.0001, calculated_amount),
            "stop_loss_pct": 0.02, # 2% Stop loss
            "take_profit_pct": 0.04 # 4% Take profit (R:R = 2.0 >= 1.5)
        }
