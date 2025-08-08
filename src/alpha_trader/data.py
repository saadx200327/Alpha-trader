import pandas as pd
import yfinance as yf

YF_INTERVALS = {
    '1m':'1m','2m':'2m','5m':'5m','15m':'15m','30m':'30m','60m':'60m','90m':'90m',
    '1h':'60m', '1d':'1d', '1wk':'1wk', '1mo':'1mo'
}

def load_ohlc(symbol: str, interval: str='1h', start: str|None=None, end: str|None=None) -> pd.DataFrame:
    yf_interval = YF_INTERVALS.get(interval, '60m')
    df = yf.download(symbol, interval=yf_interval, start=start, end=end, progress=False, auto_adjust=False)
    if df is None or df.empty:
        raise RuntimeError(f"No data returned for {symbol} with interval {interval}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0].capitalize() for c in df.columns]
    df = df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Adj Close':'adj_close','Volume':'volume'})
    df = df.dropna().copy()
    return df
