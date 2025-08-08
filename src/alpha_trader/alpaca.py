from __future__ import annotations
import alpaca_trade_api as tradeapi

class AlpacaBroker:
    def __init__(self, api_key: str, api_secret: str, base_url: str):
        self.api = tradeapi.REST(api_key, api_secret, base_url=base_url, api_version='v2')

    def submit_market_order(self, symbol: str, qty: int, side: str):
        order = self.api.submit_order(symbol=symbol, qty=qty, side=side, type='market', time_in_force='gtc')
        return order

    def position_qty(self, symbol: str) -> int:
        try:
            pos = self.api.get_position(symbol)
            return int(float(pos.qty))
        except Exception:
            return 0
