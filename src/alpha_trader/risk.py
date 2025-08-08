import math

class RiskManager:
    def __init__(self, capital: float, risk_pct: float=0.01, stop_loss_pct: float=0.02, take_profit_pct: float=0.04):
        self.capital = capital
        self.risk_pct = risk_pct
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

    def position_size(self, price: float) -> int:
        risk_amount = self.capital * self.risk_pct
        stop_dist = price * self.stop_loss_pct
        if stop_dist <= 0:
            return 0
        shares = math.floor(risk_amount / stop_dist)
        return max(shares, 0)

    def stops_targets(self, entry: float) -> tuple[float,float]:
        stop = entry * (1 - self.stop_loss_pct)
        target = entry * (1 + self.take_profit_pct)
        return stop, target
