import backtrader as bt
import backtrader.feeds as btfeeds


class MyTrader:

    # BASE PARAMETER
    initial_cash = 1000000
    broker_commission = 0.1/100
    data = None

    print("Setting Cerebro...")
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(broker_commission)

    def __init__(self, data):
        print("Adding data to cerebro..")
        self.data = MyTrader.convert_data(data)
        self.cerebro.adddata(self.data)

    @staticmethod
    def convert_data(data):
        """
        Converts the pandas datat to Cerebro DataFeed type
        :param data: the pandas dataframe object with OHLC format
        :return: DataFeed object
        """
        pf = btfeeds.PandasData(dataname=data)  # learned this after lot of efforts
        return pf

    def portfolio_value(self):

        current_value = self.cerebro.broker.getvalue()
        print(f"Portfolio value:{current_value}")
        return current_value

    def run_cerebro(self):
        runner = self.cerebro.run()
        return runner

    # def reset_cerebro(self):
    #     self.cerebro = bt.Cerebro()
    #     self.cerebro.broker.set_cash(self.initial_cash)
    #     self.cerebro.adddata(self.data)

    def add_strategy(self, strategy):
        self.cerebro.addstrategy(strategy)



