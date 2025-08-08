from __future__ import annotations
import pandas as pd
import numpy as np
from .risk import RiskManager

def backtest(signals_df: pd.DataFrame, risk: RiskManager, slippage_bps: float=1.0) -> dict:
    df = signals_df.copy()
    df = df.dropna().copy()
    df['position'] = df['signal'].shift(1).fillna(0)
    df['ret'] = df['close'].pct_change().fillna(0)
    df['gross'] = df['position'] * df['ret']

    slippage = (slippage_bps / 10000.0)
    df['net'] = df['gross'] - abs(df['position'].diff().fillna(0)) * slippage

    equity = [risk.capital]
    for r in df['net']:
        equity.append(equity[-1] * (1 + r))
    df['equity'] = equity[1:]

    stats = {
        'start_equity': risk.capital,
        'end_equity': float(df['equity'].iloc[-1]) if len(df) else risk.capital,
        'return_pct': float((df['equity'].iloc[-1] / risk.capital - 1) * 100) if len(df) else 0.0,
        'max_drawdown_pct': float(((df['equity'] / df['equity'].cummax()).min() - 1) * 100) if len(df) else 0.0,
        'trades': int(df['position'].diff().abs().sum())
    }
    return {'stats': stats, 'equity_curve': df[['equity']]}
