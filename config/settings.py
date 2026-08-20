import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_SECRET_KEY: str = os.getenv("BINANCE_SECRET_KEY", "")
    USE_LIVE_BINANCE_API: bool = True
    
    INITIAL_CAPITAL: float = 432.47
    ALLOCATION_PER_POD: float = 0.20  # 20% vốn mỗi lệnh (~$80.00 USD)
    SINGLE_ORDER_USD: float = 80.00
    
    # 🛑 CẦU DAO AN TOÀN TUYỆT ĐỐI: Dừng 100% Giao dịch nếu Ví < $350.00 USD
    MIN_PORTFOLIO_STOP_LOSS_USD: float = 350.00
    
    # 🎯 CHIẾN LƯỢC PHỤC HỒI VỐN NHANH $80 USD (R:R = 2:1 | TP = +$2.20 USD / SL = -$1.10 USD)
    TAKE_PROFIT_MIN_USD: float = 2.20 # Chốt lời ròng +$2.20 USD (2.8%)
    STOP_LOSS_MAX_USD: float = 1.10   # Cắt lỗ an toàn -$1.10 USD (1.4%)
    
    # ⏱️ KHÓA TẦN SUẤT COOLDOWN 15 PHÚT (900 SECONDS MỖI CẶP COIN)
    ORDER_COOLDOWN_SECONDS: int = 900
    
    # 🔒 GIỚI HẠN TỐI ĐA 3 VỊ THẾ MỞ CÙNG LÚC ($240 USD VỐN - DỰ TRỮ $76+ USDT TIỀN MẶT)
    MAX_CONCURRENT_POSITIONS: int = 3

settings = Settings()
