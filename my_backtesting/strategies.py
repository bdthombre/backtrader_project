from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
import backtesting as bt


def SMA(values, n):
    """
    Returns Rolling avg of values at each step of n interval
    """
    return pd.Series(values).rolling(n).mean()


class SmaCross(Strategy):
    n1 = 5
    n2 = 15

    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        self.sma2 = None
        self.sma1 = None

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()

    # Optimizers

    @staticmethod
    def optimize_sma(bt_object: bt.Backtest, n1_low, n1_high, n2_low, n2_high):
        return bt_object.optimize(
            n1=range(n1_low, n1_high, 5),
            n2=range(n2_low, n2_high, 5),
            constraint=lambda param: param.n1 < param.n2
        )

