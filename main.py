import time
import sys
from typing import Dict, Any
from core.market_data import MarketDataEngine
from core.paper_engine import PaperTradingEngine
from graphs.heartbeat_graph import HeartbeatWorkflow
from config.settings import settings

def print_dashboard(cycle_number: int, result: Dict[str, Any]):
    print("=" * 80)
    print(f"🤖 AGENTIC AI TRADING BOT - HEARTBEAT CYCLE #{cycle_number}")
    print(f"⏱️  Architecture: 30s Heartbeat Loop | Pod Theory (Multi-Pod Diversification)")
    print("=" * 80)

    # 1. Preprocessor Summary
    prep = result.get("preprocessed_summary", {})
    print("\n🔍 [0s-10s] SUB-AGENT PREPROCESSOR SUMMARY:")
    for sym_info in prep.get("preprocessed_symbols", []):
        print(f"   • {sym_info['symbol']:<10} | Price: ${sym_info['price']:<9.2f} | RSI: {sym_info['rsi']:<4.1f} | Z-Score: {sym_info['z_score']:<5.2f} | Status: {sym_info['strain_status']}")

    # 2. Pod Signals & Sharpe Check
    print("\n🎯 [20s] THE POD THEORY EVALUATION (Sharpe Ratio Guardrail > 1.0):")
    for pod_sig in result.get("pod_signals", []):
        sig = pod_sig['signal']
        color_sig = f"🟢 {sig}" if sig == "BUY" else (f"🔴 {sig}" if sig == "SELL" else f"⚪ {sig}")
        print(f"   • [{pod_sig['pod_id']}] Signal: {color_sig:<12} | Sharpe: {pod_sig['sharpe_ratio']:.2f} | Strategy: {pod_sig['strategy']}")
        if pod_sig.get("reasoning"):
            print(f"     └─ Rationale: {pod_sig['reasoning']}")

    # 3. Executed Actions & Risk Officer Verdict
    print("\n⚡ [30s] RISK OFFICER & ORCHESTRATION EXECUTIONS:")
    actions = result.get("executed_actions", [])
    if not actions:
        print("   • No trades executed in this cycle (Market neutral / Risk hold).")
    else:
        for act in actions:
            if act.get("action") == "BLOCKED_BY_RISK":
                print(f"   🛡️  [RISK BLOCK] {act['pod_id']} ({act['symbol']}): {act['reason']}")
            else:
                print(f"   ✅ [EXECUTION] {act['action']} {act['amount']} {act['symbol']} @ ${act['price']:.2f} (Pod: {act['pod_id']})")

    # 4. Portfolio State
    port = result.get("portfolio_summary", {})
    print("\n📊 PORTFOLIO STATUS (PAPER TRADING):")
    print(f"   • Total Portfolio Value: ${port['total_portfolio_value']:,.2f} USD")
    print(f"   • Cash Balance:          ${port['cash_balance']:,.2f} USD")
    print(f"   • Total Return PnL:      {port['total_return_pct']:+.2f}%")
    print(f"   • Max Drawdown:          {port['drawdown_pct']:.2f}% (Limit: {settings.MAX_DAILY_DRAWDOWN*100}%)")
    print(f"   • Open Positions:        {port['open_positions_count']}")
    
    for pos in port.get("positions", []):
        pnl = pos['unrealized_pnl']
        pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
        print(f"     └─ {pos['symbol']:<9} ({pos['side']:<4}) | Entry: ${pos['entry']:<8.2f} | Amount: {pos['amount']} | PnL: {pnl_str}")
    print("=" * 80 + "\n")

def run_trading_bot(cycles: int = 3, interval: int = 5):
    print("\n🚀 Khởi chạy Agentic AI Trading Bot theo Kiến trúc Nhịp Tim (Heartbeat Architecture)...")
    print(f"💰 Vốn khởi tạo giả lập (Paper Balance): ${settings.INITIAL_BALANCE:,.2f} USD\n")

    market_engine = MarketDataEngine(symbols=settings.TARGET_PAIRS)
    paper_engine = PaperTradingEngine(initial_balance=settings.INITIAL_BALANCE)
    workflow = HeartbeatWorkflow(paper_engine)

    for c in range(1, cycles + 1):
        # 1. Cào dữ liệu nến realtime / simulated
        raw_market_data = {}
        for sym in settings.TARGET_PAIRS:
            raw_market_data[sym] = market_engine.get_latest_ticker(sym)

        # 2. Chạy vòng lặp LangGraph Heartbeat 30s
        cycle_res = workflow.run_cycle(raw_market_data)

        # 3. Hiển thị Dashboard
        print_dashboard(c, cycle_res)

        if c < cycles:
            time.sleep(interval)

if __name__ == "__main__":
    cycles_to_run = 3
    if len(sys.argv) > 1:
        try:
            cycles_to_run = int(sys.argv[1])
        except ValueError:
            pass
    run_trading_bot(cycles=cycles_to_run, interval=2)
