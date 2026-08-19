import json
from typing import Dict, Any
from config.settings import settings
from config.prompt_templates import PREPROCESSOR_AGENT_PROMPT

class PreprocessorAgent:
    """
    Sub-Agent Siêu Nhỏ (10-Second Fast Preprocessor).
    Tóm tắt dữ liệu nến, orderbook & chỉ báo thành định dạng JSON nhỏ gọn cho Main LLM.
    """
    def __init__(self):
        self.name = "10s-Preprocessor-SubAgent"

    def process(self, raw_market_summary: Dict[str, Any]) -> Dict[str, Any]:
        # Phân tích định lượng siêu tốc mà không làm phì dung lượng Token
        symbols_analysis = []
        for symbol, ticker_info in raw_market_summary.items():
            z_score = ticker_info.get("z_score", 0.0)
            rsi = ticker_info.get("rsi", 50.0)
            price = ticker_info.get("price", 0.0)
            
            # Đánh giá Rubber Band Strain
            strain_status = "NORMAL"
            if z_score > 2.0:
                strain_status = "OVERSTRETCHED_UP (Overbought - Rubber Band Tight)"
            elif z_score < -2.0:
                strain_status = "OVERSTRETCHED_DOWN (Oversold - Rubber Band Tight)"

            symbols_analysis.append({
                "symbol": symbol,
                "price": price,
                "rsi": round(rsi, 1),
                "z_score": round(z_score, 2),
                "strain_status": strain_status
            })

        return {
            "timestamp_stage": "10s_preprocessed",
            "preprocessed_symbols": symbols_analysis,
            "system_health": "OPTIMAL"
        }
