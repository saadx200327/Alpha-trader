from __future__ import annotations
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False).mean()

def rsi(series: pd.Series, length: int=14) -> pd.Series:
    delta = series.diff()
    gain = (delta.clip(lower=0)).rolling(length).mean()
    loss = (-delta.clip(upper=0)).rolling(length).mean()
    rs = gain / (loss.replace(0, np.nan))
    return 100 - (100 / (1 + rs))

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

class EMACrossRSIStrategy(BaseStrategy):
    def __init__(self, ema_fast: int=9, ema_slow: int=20, rsi_len: int=14, rsi_buy_below: float=60, rsi_sell_above: float=40):
        self.ema_fast = ema_fast
        self.ema_slow = ema_slow
        self.rsi_len = rsi_len
        self.rsi_buy_below = rsi_buy_below
        self.rsi_sell_above = rsi_sell_above

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out['ema_fast'] = ema(out['close'], self.ema_fast)
        out['ema_slow'] = ema(out['close'], self.ema_slow)
        out['rsi'] = rsi(out['close'], self.rsi_len)
        out['cross_up'] = (out['ema_fast'] > out['ema_slow']) & (out['ema_fast'].shift(1) <= out['ema_slow'].shift(1))
        out['cross_down'] = (out['ema_fast'] < out['ema_slow']) & (out['ema_fast'].shift(1) >= out['ema_slow'].shift(1))

        long_signal = out['cross_up'] & (out['rsi'] < self.rsi_buy_below)
        flat_signal = out['cross_down'] & (out['rsi'] > self.rsi_sell_above)

        out['signal'] = 0
        out.loc[long_signal, 'signal'] = 1
        out.loc[flat_signal, 'signal'] = 0
        out['signal'] = out['signal'].ffill().fillna(0).astype(int)
        return out
