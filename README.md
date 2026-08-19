# 🤖 Agentic AI Trading Bot - Binance 100% Real Live Trading Dashboard

An autonomous, multi-agent AI quantitative trading bot for Binance Spot market based on **Heartbeat Architecture (30s)**, **Pod Theory (Sharpe Ratio Filter > 1.0)**, **Rubber Band Mean Reversion (Z-Score Strain)**, and **Institutional Capital Recovery Architecture (Risk-Reward 2:1, Anti-Overtrading 15m Cooldown, & Safety Circuit Breaker)**.

---

## 🌟 Key Features

- **🔴 100% Live Binance Spot Execution**: Native Python REST API client with zero external dependencies (`urllib.request`, `hmac`, `hashlib`), avoiding third-party library errors.
- **🧠 30-Second Heartbeat Pipeline**: Multi-agent sub-pipeline running 4 steps every 30 seconds:
  1. `0s`: Realtime Binance Market Data Ingest.
  2. `10s`: Rubber Band Z-Score & RSI Strain Summarization.
  3. `10-Pod Evaluation`: Independent Pod evaluation with Sharpe Ratio > 1.0 filter.
  4. `30s`: Binance Spot Order Execution ($40.00 USD allocation per trade).
- **🛡️ Institutional Risk Management**:
  - **Risk-Reward Ratio 2:1**: Target Take-Profit $\ge$ **+$1.20 USD (2.8%)**, Stop-Loss $\le$ **-$0.60 USD (1.4%)**.
  - **Anti-Overtrading Cooldown (15 Minutes)**: Prevents high-frequency over-trading and fee drain.
  - **Duplicate Buy Lock**: Restricts maximum active open positions to 2 concurrent coins.
  - **Safety Circuit Breaker ($350.00 USD)**: Auto-locks all trading if total portfolio value drops below $350.00 USD.
- **💻 Responsive Financial Web Dashboard**: Live web dashboard running on `http://localhost:8000` built with native HTML5, CSS3, JavaScript, and Multi-Threaded TCP HTTP Server.

---

## 📁 Repository Structure

```text
agentic_trading_bot/
├── config/
│   └── settings.py          # Configuration parameters & risk parameters
├── core/
│   └── live_binance.py      # Native Binance REST API client (HMAC SHA256)
├── web/
│   ├── index.html           # Dark financial dashboard UI
│   ├── styles.css           # Modern CSS styling
│   └── app.js               # Frontend application logic & heartbeat timer
├── web_server.py            # Multi-threaded Python HTTP REST API Server
├── .env.example             # Template for Binance API credentials
├── .gitignore               # Ignores sensitive environment files (.env)
└── README.md                # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.8+
- Active Binance Account with Spot Trading enabled API keys.

### 2. Setup Environment
Clone the repository and set up your `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your Binance API Key and Secret Key:
```env
BINANCE_API_KEY=your_actual_binance_api_key
BINANCE_SECRET_KEY=your_actual_binance_secret_key
```

### 3. Run the Trading Server
Start the multi-threaded web server:
```bash
python3 web_server.py
```

Open your browser and navigate to:
```text
http://localhost:8000
```

---

## 📊 Strategy Overview

| Metric | Setting / Parameter | Description |
| :--- | :--- | :--- |
| **Execution Mode** | Binance Spot (1x) | 100% Real Spot Trading. Zero liquidation risk. |
| **Order Allocation** | $40.00 USD / Trade | Dynamic 10% allocation per open position. |
| **Take Profit Target** | `+$1.20 USD` (2.8%) | Net profit target per trade after Binance taker fees. |
| **Stop Loss Limit** | `-$0.60 USD` (1.4%) | Tight stop loss for capital preservation. |
| **Trade Cooldown** | 15 Minutes (900s) | Mandatory pause between orders per asset. |
| **Max Open Positions** | 2 Concurrent Coins | Concentrates capital into high-conviction signals. |
| **Safety Circuit Breaker** | `$350.00 USD` | Emergency halt if portfolio value falls below $350. |

---

## 🛡️ Security & Privacy Notice
- **Never commit your `.env` file or API Keys to GitHub.**
- Disable Withdrawal permissions on your Binance API Key settings for maximum security.

---

## 📜 License
MIT License - Open Source & Free to Customize.
