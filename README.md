# Alpha Trader (1M Playbook)
A simple, production-lean trading tool that supports **backtesting** and **live paper trading** on Alpaca.
It includes an EMA crossover strategy with an RSI filter, risk controls, and a CLI.

## Quick start
```bash
# 1) Create and activate a venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install
pip install -r requirements.txt

# 3) Configure
cp .env.example .env  # put your Alpaca paper keys in .env (optional for backtest)

# 4) Backtest example (GOOG, 1h bars)
python main.py backtest --symbol GOOG --interval 1h --start 2023-01-01 --end 2025-08-01

# 5) Live paper trading with Alpaca (poll each minute)
python main.py live --symbol GOOG --interval 1h --use_alpaca
```

## What it does
- Pulls historical candles via yfinance
- Generates signals using an EMA cross plus RSI filter
- Sizes positions by risk percent and stop percent
- Simulates a simple backtest
- Optional live trading on Alpaca Paper with market orders

## Files
- `main.py` — CLI
- `src/alpha_trader/strategy.py` — strategies
- `src/alpha_trader/data.py` — data loading
- `src/alpha_trader/risk.py` — risk and sizing
- `src/alpha_trader/backtest.py` — vector backtester
- `src/alpha_trader/execution.py` — live loop runner
- `src/alpha_trader/broker/alpaca.py` — Alpaca REST broker
- `src/alpha_trader/broker/paper.py` — in-memory paper broker
- `src/alpha_trader/config.py` — settings via env or CLI

## Config
Copy `.env.example` to `.env` and set values:
```
ALPACA_API_KEY_ID=your_key
ALPACA_API_SECRET_KEY=your_secret
ALPACA_PAPER_BASE_URL=https://paper-api.alpaca.markets
CAPITAL=1000000
RISK_PCT=0.01
STOP_LOSS_PCT=0.02
TAKE_PROFIT_PCT=0.04
```
You can override most via CLI flags.

## Disclaimer
This is educational software. Markets are risky. You are responsible for all use.
