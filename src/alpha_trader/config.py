from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    alpaca_key: str | None = os.getenv("ALPACA_API_KEY_ID")
    alpaca_secret: str | None = os.getenv("ALPACA_API_SECRET_KEY")
    alpaca_base_url: str = os.getenv("ALPACA_PAPER_BASE_URL", "https://paper-api.alpaca.markets")

    capital: float = float(os.getenv("CAPITAL", "1000000"))
    risk_pct: float = float(os.getenv("RISK_PCT", "0.01"))
    stop_loss_pct: float = float(os.getenv("STOP_LOSS_PCT", "0.02"))
    take_profit_pct: float = float(os.getenv("TAKE_PROFIT_PCT", "0.04"))

    # Strategy defaults
    ema_fast: int = int(os.getenv("EMA_FAST", "9"))
    ema_slow: int = int(os.getenv("EMA_SLOW", "20"))
    rsi_len: int = int(os.getenv("RSI_LEN", "14"))
    rsi_buy_below: int = int(os.getenv("RSI_BUY_BELOW", "60"))
    rsi_sell_above: int = int(os.getenv("RSI_SELL_ABOVE", "40"))
