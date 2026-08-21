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
    
    # 🎯 CHIẾN LƯỢC v4.0 FULL QUANT ENGINE (OTOCO + TRAILING STOP + 3 CHỈ BÁO KÉP)
    TAKE_PROFIT_MIN_USD: float = 2.20 # Mốc kích hoạt chốt lời/Trailing Stop (+2.8%)
    STOP_LOSS_MAX_USD: float = 1.10   # Cắt lỗ an toàn -$1.10 USD (1.4%)
    
    # 📈 TRAILING STOP SPOT (CALLBACK RATE = 0.8% BÁM DỐC NẾN BAY)
    ENABLE_TRAILING_STOP: bool = True
    TRAILING_STOP_CALLBACK_PCT: float = 0.8
    
    # 🧠 CHỈ BÁO KÉP MACD + RSI + Z-SCORE
    ENABLE_MACD_CONFIRMATION: bool = True
    
    # ⚖️ DYNAMIC POSITION SIZING (BTC/ETH = $100 USD, ALTCOINS = $80 USD)
    ENABLE_DYNAMIC_SIZING: bool = True
    
    # ⏱️ KHÓA TẦN SUẤT COOLDOWN 15 PHÚT (900 SECONDS MỖI CẶP COIN)
    ORDER_COOLDOWN_SECONDS: int = 900
    
    # 🔒 GIỚI HẠN TỐI ĐA 3 VỊ THẾ MỞ CÙNG LÚC ($240 USD VỐN - DỰ TRỮ $76+ USDT TIỀN MẶT)
    MAX_CONCURRENT_POSITIONS: int = 3

settings = Settings()
