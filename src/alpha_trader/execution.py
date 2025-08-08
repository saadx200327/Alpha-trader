from __future__ import annotations
import time
import pandas as pd
from .data import load_ohlc
from .risk import RiskManager

def run_live(symbol: str, interval: str, strategy, broker, risk: RiskManager, poll_seconds: int=60):
    print(f"Starting live loop for {symbol} on {interval}. Poll every {poll_seconds}s.")
    last_ts = None
    while True:
        df = load_ohlc(symbol, interval=interval)
        sigs = strategy.generate_signals(df)
        row = sigs.iloc[-1]
        ts = sigs.index[-1]

        if last_ts == ts:
            time.sleep(poll_seconds)
            continue
        last_ts = ts

        signal = int(row['signal'])
        price = float(row['close'])
        current_qty = broker.position_qty(symbol)

        desired_qty = 0
        if signal == 1:
            shares = risk.position_size(price)
            desired_qty = shares

        delta = desired_qty - current_qty
        if delta > 0:
            print(f"[{ts}] BUY {delta} {symbol} @ ~{price:.2f}")
            broker.submit_market_order(symbol, delta, 'buy')
        elif delta < 0:
            print(f"[{ts}] SELL {abs(delta)} {symbol} @ ~{price:.2f}")
            broker.submit_market_order(symbol, abs(delta), 'sell')
        else:
            print(f"[{ts}] HOLD {symbol} qty={current_qty}")

        time.sleep(poll_seconds)
