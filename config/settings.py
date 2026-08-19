import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_SECRET_KEY: str = os.getenv("BINANCE_SECRET_KEY", "")
    USE_LIVE_BINANCE_API: bool = True
    
    INITIAL_CAPITAL: float = 432.47
    ALLOCATION_PER_POD: float = 0.10  # 10% vốn mỗi lệnh (~$40.00 USD)
    SINGLE_ORDER_USD: float = 40.00
    
    # 🛑 CẦU DAO AN TOÀN TUYỆT ĐỐI: Dừng 100% Giao dịch nếu Ví < $350.00 USD
    MIN_PORTFOLIO_STOP_LOSS_USD: float = 350.00
    
    # 🎯 MỐC TỶ LỆ VÀNG RISK-REWARD 2:1 (TP = +$1.20 USD / SL = -$0.60 USD)
    TAKE_PROFIT_MIN_USD: float = 1.20 # Chốt lời +$1.20 USD (2.8%)
    STOP_LOSS_MAX_USD: float = 0.60   # Cắt lỗ -$0.60 USD (1.4%)
    
    # ⏱️ KHÓA TẦN SUẤT CAO CẤP (COOLDOWN 15 PHÚT / 900 SECONDS MỖI CẶP COIN)
    ORDER_COOLDOWN_SECONDS: int = 900
    
    # 🔒 GIỚI HẠN TỐI ĐA 2 VỊ THẾ MỞ CÙNG LÚC TRÁNH PHÂN TÁN VỐN
    MAX_CONCURRENT_POSITIONS: int = 2

settings = Settings()
