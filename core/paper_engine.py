from typing import Dict, List, Any
from datetime import datetime

class Position:
    def __init__(self, symbol: str, pod_id: str, side: str, entry_price: float, amount: float, stop_loss: float = 0.0, take_profit: float = 0.0):
        self.symbol = symbol
        self.pod_id = pod_id
        self.side = side  # 'BUY', 'SELL', 'HEDGE'
        self.entry_price = entry_price
        self.amount = amount
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def current_pnl(self, current_price: float) -> float:
        if self.side in ['BUY', 'HEDGE']:
            return (current_price - self.entry_price) * self.amount
        else:
            return (self.entry_price - current_price) * self.amount

class PaperTradingEngine:
    def __init__(self, initial_balance: float = 432.0):
        self.initial_balance = initial_balance
        self.cash = initial_balance
        self.positions: List[Position] = []
        self.trade_history: List[Dict[str, Any]] = []
        self.peak_portfolio_value = initial_balance

    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        unrealized_pnl = sum(
            pos.current_pnl(current_prices.get(pos.symbol, pos.entry_price))
            for pos in self.positions
        )
        total_val = self.cash + unrealized_pnl
        if total_val > self.peak_portfolio_value:
            self.peak_portfolio_value = total_val
        return total_val

    def get_drawdown(self, current_prices: Dict[str, float]) -> float:
        current_val = self.get_portfolio_value(current_prices)
        if self.peak_portfolio_value <= 0:
            return 0.0
        drawdown = (self.peak_portfolio_value - current_val) / self.peak_portfolio_value
        return max(0.0, float(drawdown))

    def execute_order(self, symbol: str, pod_id: str, action: str, price: float, amount: float, stop_loss: float = 0.0, take_profit: float = 0.0) -> Dict[str, Any]:
        cost = price * amount
        if action in ['BUY', 'HEDGE']:
            if self.cash < cost:
                return {"status": "REJECTED", "reason": "Insufficient Cash"}
            self.cash -= cost
            pos = Position(symbol, pod_id, action, price, amount, stop_loss, take_profit)
            self.positions.append(pos)
            res = {"status": "SUCCESS", "action": action, "symbol": symbol, "price": price, "amount": amount, "pod_id": pod_id, "timestamp": datetime.now().strftime("%H:%M:%S")}
        elif action in ['CLOSE', 'SELL']:
            matched = [p for p in self.positions if p.symbol == symbol and p.pod_id == pod_id]
            if not matched:
                return {"status": "REJECTED", "reason": "No position found to close"}
            pos = matched[0]
            pnl = pos.current_pnl(price)
            self.cash += (pos.entry_price * pos.amount) + pnl
            self.positions.remove(pos)
            res = {"status": "CLOSED", "action": "CLOSE", "symbol": symbol, "price": price, "realized_pnl": pnl, "pod_id": pod_id, "timestamp": datetime.now().strftime("%H:%M:%S")}
        else:
            res = {"status": "SKIPPED", "action": action}

        self.trade_history.append(res)
        return res

    def get_summary(self, current_prices: Dict[str, float]) -> Dict[str, Any]:
        port_val = self.get_portfolio_value(current_prices)
        drawdown = self.get_drawdown(current_prices)
        return {
            "total_portfolio_value": round(port_val, 2),
            "cash_balance": round(self.cash, 2),
            "open_positions_count": len(self.positions),
            "drawdown_pct": round(drawdown * 100, 2),
            "total_return_pct": round(((port_val - self.initial_balance) / self.initial_balance) * 100, 2),
            "positions": [
                {
                    "symbol": p.symbol,
                    "pod": p.pod_id,
                    "side": p.side,
                    "entry": p.entry_price,
                    "amount": p.amount,
                    "unrealized_pnl": round(p.current_pnl(current_prices.get(p.symbol, p.entry_price)), 2)
                }
                for p in self.positions
            ]
        }
