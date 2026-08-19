import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.indicators import calculate_sharpe_ratio, calculate_z_score_strain
from core.paper_engine import PaperTradingEngine
from pods.mean_reversion_pod import MeanReversionPod
from agents.risk_agent import RiskManagementAgent

class TestAgenticTradingBot(unittest.TestCase):
    def test_sharpe_ratio_calculator(self):
        returns = [0.01, 0.02, -0.005, 0.015, 0.03, -0.01, 0.02]
        sharpe = calculate_sharpe_ratio(returns)
        self.assertGreater(sharpe, 0.0)

    def test_z_score_strain(self):
        prices = [100.0 + i*0.5 for i in range(25)]
        z_score = calculate_z_score_strain(prices)
        self.assertIsInstance(z_score, float)

    def test_paper_engine_execution(self):
        engine = PaperTradingEngine(initial_balance=10000.0)
        res = engine.execute_order("BTC/USDT", "Pod-01", "BUY", price=60000.0, amount=0.1)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(engine.cash, 10000.0 - 6000.0)
        self.assertEqual(len(engine.positions), 1)

    def test_risk_agent_sharpe_guardrail(self):
        risk_agent = RiskManagementAgent()
        portfolio_summary = {"total_portfolio_value": 10000.0, "drawdown_pct": 0.0}
        
        # Test bị từ chối nếu Sharpe < 1.0 (như video lưu ý)
        rejected_signal = {"signal": "BUY", "sharpe_ratio": 0.4, "price": 60000.0, "symbol": "BTC/USDT"}
        verdict = risk_agent.evaluate_risk(rejected_signal, portfolio_summary)
        self.assertFalse(verdict["approved"])
        self.assertIn("REJECTED", verdict["reason"])

        # Test được chấp thuận nếu Sharpe >= 1.0
        approved_signal = {"signal": "BUY", "sharpe_ratio": 1.25, "price": 60000.0, "symbol": "BTC/USDT"}
        verdict_app = risk_agent.evaluate_risk(approved_signal, portfolio_summary)
        self.assertTrue(verdict_app["approved"])

if __name__ == "__main__":
    unittest.main()
