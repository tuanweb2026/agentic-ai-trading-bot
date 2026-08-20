# 🤖 Agentic AI Trading Bot - Binance 100% Real Live Trading Dashboard

An autonomous, multi-agent AI quantitative trading bot for Binance Spot market based on **Heartbeat Architecture (30s)**, **Pod Theory (Sharpe Ratio Filter > 1.0)**, **Rubber Band Mean Reversion (Z-Score Strain)**, and **Fast Capital Recovery Architecture ($80.00 USD Order Allocation, Max 3 Concurrent Positions ($240 USD Total), Risk-Reward 2:1, Anti-Overtrading 15m Cooldown, & Safety Circuit Breaker)**.

---

## 🌟 Key Features

- **🔴 100% Live Binance Spot Execution**: Native Python REST API client with zero external dependencies (`urllib.request`, `hmac`, `hashlib`), avoiding third-party library errors.
- **🚀 Fast Capital Recovery Strategy ($80.00 USD / Trade, Max 3 Positions)**: Upgraded allocation per trade to $80 USD with up to 3 concurrent active positions ($240 USD total active capital) for accelerated capital recovery.
- **🧠 30-Second Heartbeat Pipeline**: Multi-agent sub-pipeline running 4 steps every 30 seconds:
  1. `0s`: Realtime Binance Market Data Ingest.
  2. `10s`: Rubber Band Z-Score & RSI Strain Summarization.
  3. `10-Pod Evaluation`: Independent Pod evaluation with Sharpe Ratio > 1.0 filter.
  4. `30s`: Binance Spot Order Execution ($80.00 USD allocation per trade).
- **🛡️ Institutional Risk Management**:
  - **Risk-Reward Ratio 2:1**: Target Take-Profit $\ge$ **+$2.20 USD (2.8%)**, Stop-Loss $\le$ **-$1.10 USD (1.4%)**.
  - **Anti-Overtrading Cooldown (15 Minutes)**: Prevents high-frequency over-trading and fee drain.
  - **Duplicate Buy & Dust Filter**: Cleanly filters out wallet dust (< $15 USD) and restricts maximum active open positions to 3 concurrent coins ($240 USD total allocation).
  - **Safety Circuit Breaker ($350.00 USD)**: Auto-locks all trading if total portfolio value drops below $350.00 USD.
- **💻 Responsive Financial Web Dashboard**: Live web dashboard running on `http://localhost:8000` built with native HTML5, CSS3, JavaScript, and Multi-Threaded TCP HTTP Server.

---

## 📁 Repository Structure

```text
agentic_trading_bot/
├── config/
│   └── settings.py          # Configuration parameters ($80 USD order size, 3 max positions, Risk-Reward 2:1)
├── core/
│   └── live_binance.py      # Native Binance REST API client (HMAC SHA256)
├── web/
│   ├── index.html           # Dark financial dashboard UI (v19.0)
│   ├── styles.css           # Modern CSS styling
│   └── app.js               # Frontend application logic & heartbeat timer ($80 USD, 3 positions mode)
├── web_server.py            # Multi-threaded Python HTTP REST API Server
├── .env.example             # Template for Binance API credentials
├── .gitignore               # Ignores sensitive environment files (.env)
└── README.md                # Project documentation
```

---

## 📊 Strategy Parameters (v3.0 - 3 Concurrent Orders $80 USD Fast Recovery)

| Metric | Setting / Parameter | Description |
| :--- | :--- | :--- |
| **Execution Mode** | Binance Spot (1x) | 100% Real Spot Trading. Zero liquidation risk. |
| **Order Allocation** | `$80.00 USD` / Trade | 20% allocation per open position for fast capital recovery. |
| **Take Profit Target** | `+$2.20 USD` (2.8%) | Net profit target per trade after Binance taker fees. |
| **Stop Loss Limit** | `-$1.10 USD` (1.4%) | Tight stop loss for capital preservation. |
| **Trade Cooldown** | 15 Minutes (900s) | Mandatory pause between orders per asset. |
| **Max Open Positions** | 3 Concurrent Coins | $240 USD total active allocation, maintaining $76+ USDT cash reserve. |
| **Safety Circuit Breaker** | `$350.00 USD` | Emergency halt if portfolio value falls below $350. |

---

## 📜 License
MIT License - Open Source & Free to Customize.
