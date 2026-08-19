import json
from typing import Dict, Any, List
from config.settings import settings
from agents.preprocessor_agent import PreprocessorAgent
from agents.risk_agent import RiskManagementAgent
from pods.mean_reversion_pod import MeanReversionPod
from pods.trend_following_pod import TrendFollowingPod
from core.paper_engine import PaperTradingEngine

class MainOrchestratorAgent:
    """
    Chief Investment Officer (CIO) Agent - Vòng lặp Nhịp tim 30 Giây (30s Heartbeat).
    Quản lý 10 Pods độc lập cho 10 tài sản theo Thuyết đồ nhóm (Phân bổ $50 / Pod từ tổng vốn $500).
    """
    def __init__(self, paper_engine: PaperTradingEngine):
        self.name = "30s-CIO-Orchestrator"
        self.paper_engine = paper_engine
        self.preprocessor = PreprocessorAgent()
        self.risk_agent = RiskManagementAgent()
        
        # Khởi tạo 10 Pods độc lập với $50/pod ($500 tổng vốn)
        self.pods = [
            MeanReversionPod(pod_id="Pod-01-RubberBand-BTC", symbol="BTC/USDT", allocated_capital=50.0),
            TrendFollowingPod(pod_id="Pod-02-Trend-ETH", symbol="ETH/USDT", allocated_capital=50.0),
            MeanReversionPod(pod_id="Pod-03-RubberBand-SOL", symbol="SOL/USDT", allocated_capital=50.0),
            TrendFollowingPod(pod_id="Pod-04-Trend-BNB", symbol="BNB/USDT", allocated_capital=50.0),
            MeanReversionPod(pod_id="Pod-05-RubberBand-XRP", symbol="XRP/USDT", allocated_capital=50.0),
            TrendFollowingPod(pod_id="Pod-06-Trend-ADA", symbol="ADA/USDT", allocated_capital=50.0),
            MeanReversionPod(pod_id="Pod-07-RubberBand-AVAX", symbol="AVAX/USDT", allocated_capital=50.0),
            TrendFollowingPod(pod_id="Pod-08-Trend-NEAR", symbol="NEAR/USDT", allocated_capital=50.0),
            MeanReversionPod(pod_id="Pod-09-RubberBand-LINK", symbol="LINK/USDT", allocated_capital=50.0),
            TrendFollowingPod(pod_id="Pod-10-Trend-NVDA", symbol="NVDA", allocated_capital=50.0)
        ]

    def heartbeat_cycle(self, raw_market_data: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        current_prices = {sym: data["price"] for sym, data in raw_market_data.items()}
        
        preprocessed_state = self.preprocessor.process(raw_market_data)

        pod_evaluations = []
        for pod in self.pods:
            market_info = raw_market_data.get(pod.symbol, {})
            evaluation = pod.evaluate(market_info)
            evaluation["price"] = market_info.get("price", 0.0)
            pod_evaluations.append(evaluation)

        portfolio_summary = self.paper_engine.get_summary(current_prices)
        executed_actions = []

        for eval_item in pod_evaluations:
            signal = eval_item["signal"]
            symbol = eval_item["symbol"]
            pod_id = eval_item["pod_id"]
            price = eval_item["price"]

            if signal in ["BUY", "SELL"]:
                risk_verdict = self.risk_agent.evaluate_risk(eval_item, portfolio_summary)
                
                if risk_verdict["approved"]:
                    amount = risk_verdict["adjusted_amount"]
                    stop_loss = price * (1 - risk_verdict["stop_loss_pct"]) if signal == "BUY" else price * (1 + risk_verdict["stop_loss_pct"])
                    take_profit = price * (1 + risk_verdict["take_profit_pct"]) if signal == "BUY" else price * (1 - risk_verdict["take_profit_pct"])

                    exec_res = self.paper_engine.execute_order(
                        symbol=symbol,
                        pod_id=pod_id,
                        action=signal,
                        price=price,
                        amount=amount
                    )
                    executed_actions.append({
                        "pod_id": pod_id,
                        "action": signal,
                        "symbol": symbol,
                        "price": price,
                        "amount": amount,
                        "status": exec_res.get("status"),
                        "reasoning": eval_item["reasoning"]
                    })
                else:
                    executed_actions.append({
                        "pod_id": pod_id,
                        "action": "BLOCKED_BY_RISK",
                        "symbol": symbol,
                        "reason": risk_verdict["reason"]
                    })

        updated_portfolio = self.paper_engine.get_summary(current_prices)

        return {
            "cycle_status": "COMPLETED",
            "heartbeat_seconds": 30,
            "preprocessed_summary": preprocessed_state,
            "pod_signals": pod_evaluations,
            "executed_actions": executed_actions,
            "portfolio_summary": updated_portfolio
        }
