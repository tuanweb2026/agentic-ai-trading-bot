from typing import Dict, Any
from agents.orchestrator_agent import MainOrchestratorAgent
from core.paper_engine import PaperTradingEngine

class HeartbeatWorkflow:
    """
    Workflow điều phối 30s Heartbeat Architecture bằng Python Standard State Engine.
    Hoạt động độc lập 100% không yêu cầu cài đặt thư viện bên thứ 3.
    """
    def __init__(self, paper_engine: PaperTradingEngine):
        self.orchestrator = MainOrchestratorAgent(paper_engine)

    def run_cycle(self, raw_market_data: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        # 1. Ingest Data (0s)
        state = {"raw_market_data": raw_market_data}
        
        # 2. Execute 30s Heartbeat Loop (10s Preprocessor -> 20s Pods -> 30s CIO Orchestrator & Risk Guardrails)
        cycle_result = self.orchestrator.heartbeat_cycle(state["raw_market_data"])
        return cycle_result
