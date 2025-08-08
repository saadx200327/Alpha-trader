from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    qty: int
    side: str   # 'buy' or 'sell'
    type: str   # 'market'
    time_in_force: str = 'gtc'

class PaperBroker:
    def __init__(self):
        self.positions = {}

    def submit_market_order(self, symbol: str, qty: int, side: str):
        if side not in ('buy','sell'):
            raise ValueError('side must be buy or sell')
        pos = self.positions.get(symbol, 0)
        self.positions[symbol] = pos + qty if side=='buy' else pos - qty
        return Order(symbol=symbol, qty=qty, side=side, type='market')

    def position_qty(self, symbol: str) -> int:
        return self.positions.get(symbol, 0)
