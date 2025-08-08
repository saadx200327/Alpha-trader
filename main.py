from __future__ import annotations
import argparse
from src.alpha_trader.data import load_ohlc
from src.alpha_trader.strategy import EMACrossRSIStrategy
from src.alpha_trader.risk import RiskManager
from src.alpha_trader.backtest import backtest
from src.alpha_trader.config import Settings
from src.alpha_trader.execution import run_live
from src.alpha_trader.broker.paper import PaperBroker
from src.alpha_trader.broker.alpaca import AlpacaBroker

def cli():
    parser = argparse.ArgumentParser(description='Alpha Trader CLI')
    sub = parser.add_subparsers(dest='cmd')

    bt = sub.add_parser('backtest', help='Run backtest')
    bt.add_argument('--symbol', required=True)
    bt.add_argument('--interval', default='1h', help='1m 5m 15m 1h 1d etc')
    bt.add_argument('--start', required=True)
    bt.add_argument('--end', required=True)
    bt.add_argument('--ema_fast', type=int, default=None)
    bt.add_argument('--ema_slow', type=int, default=None)
    bt.add_argument('--rsi_len', type=int, default=None)

    lv = sub.add_parser('live', help='Run live paper trading (Alpaca or in-memory)')
    lv.add_argument('--symbol', required=True)
    lv.add_argument('--interval', default='1h')
    lv.add_argument('--use_alpaca', action='store_true', help='If set, use Alpaca credentials from .env')
    lv.add_argument('--poll', type=int, default=60)

    args = parser.parse_args()
    cfg = Settings()

    if args.cmd == 'backtest':
        df = load_ohlc(args.symbol, args.interval, start=args.start, end=args.end)
        strat = EMACrossRSIStrategy(
            ema_fast=args.ema_fast or cfg.ema_fast,
            ema_slow=args.ema_slow or cfg.ema_slow,
            rsi_len=args.rsi_len or cfg.rsi_len,
        )
        sigs = strat.generate_signals(df)
        risk = RiskManager(cfg.capital, cfg.risk_pct, cfg.stop_loss_pct, cfg.take_profit_pct)
        res = backtest(sigs, risk)
        print('Backtest stats:', res['stats'])
    elif args.cmd == 'live':
        strat = EMACrossRSIStrategy(cfg.ema_fast, cfg.ema_slow, cfg.rsi_len)
        risk = RiskManager(cfg.capital, cfg.risk_pct, cfg.stop_loss_pct, cfg.take_profit_pct)
        if args.use_alpaca and cfg.alpaca_key and cfg.alpaca_secret:
            broker = AlpacaBroker(cfg.alpaca_key, cfg.alpaca_secret, cfg.alpaca_base_url)
        else:
            broker = PaperBroker()
            print('Using in-memory paper broker (no live orders).')
        run_live(args.symbol, args.interval, strat, broker, risk, poll_seconds=args.poll)
    else:
        parser.print_help()

if __name__ == '__main__':
    cli()
