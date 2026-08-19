import math
import statistics
from typing import List, Dict, Any, Tuple

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02, periods_per_year: int = 365 * 24 * 60 * 2) -> float:
    """
    Tính Tỷ lệ Sharpe (Sharpe Ratio) bằng Standard Library (Không phụ thuộc numpy/pandas).
    Video Tóm Tắt yêu cầu Sharpe Ratio > 1.0 để loại bỏ chiến lược Overfitted.
    """
    if len(returns) < 2:
        return 0.0
    
    mean_ret = statistics.mean(returns)
    try:
        std_ret = statistics.stdev(returns)
    except statistics.StatisticsError:
        std_ret = 0.0
        
    if std_ret == 0:
        return 0.0
    
    rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    excess_mean = mean_ret - rf_per_period
    sharpe = (excess_mean / std_ret) * math.sqrt(periods_per_year)
    return float(sharpe)

def calculate_z_score_strain(prices: List[float], window: int = 20) -> float:
    """
    Tính 'Độ căng sợi dây thun' (Rubber-Band Strain / Z-Score Deviation).
    Dùng trong Pod Mean Reversion: khi Z-score > 2.0 hoặc < -2.0, dây thun căng tối đa và chuẩn bị bật ngược lại.
    """
    if len(prices) < window:
        return 0.0
    
    sub = prices[-window:]
    mean = statistics.mean(sub)
    try:
        std = statistics.stdev(sub)
    except statistics.StatisticsError:
        std = 0.0
        
    if std == 0:
        return 0.0
    
    latest_price = prices[-1]
    z_score = (latest_price - mean) / std
    return float(z_score)

def calculate_ema(prices: List[float], period: int) -> float:
    if not prices:
        return 0.0
    k = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = (p * k) + (ema * (1 - k))
    return float(ema)

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0
    
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(diff))
            
    avg_gain = statistics.mean(gains[-period:])
    avg_loss = statistics.mean(losses[-period:])
    
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)

def calculate_macd(prices: List[float]) -> float:
    if len(prices) < 26:
        return 0.0
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)
    return float(ema_12 - ema_26)
