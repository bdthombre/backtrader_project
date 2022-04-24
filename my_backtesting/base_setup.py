from backtesting import Backtest

from strategies import SmaCross


class MyTraderBacktesting:
    initial_cash = 10000
    commission = 0.2 / 100  # 2% commission

    def __init__(self, data, ):
        self.bt = Backtest(data, SmaCross, cash=self.initial_cash, commission=self.commission)

    def run_backtest(self):
        stats = self.bt.run()
        return stats

    def get_plot_of_trades(self):
        return self.bt.plot()

    def optimize_sma(self):
        stats = SmaCross.optimize_sma(bt_object=self.bt, n1_low=5, n1_high=30,
                                      n2_low=10, n2_high=70)
        return stats

    # def portfolio_value(self):
    #     self.bt.
