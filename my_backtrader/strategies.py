import backtrader as bt


# First Strategy
class TestStrategy(bt.Strategy):
    master_log = []
    #bar_executed = 0

    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        self.master_log.append('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.bar_executed = None
        self.dataclose = self.datas[0].close
        self.order = None
        self.tradeprice = None
        self.tradecomm = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"Buy Executed, {order.executed.price:2f}")
                self.tradeprice = order.executed.price
                self.tradecomm = order.executed.comm
            elif order.issell():
                self.log(f"Sell Executed, {order.executed.price:2f}")
                self.tradeprice = order.executed.price
                self.tradecomm = order.executed.comm
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f"OPERATION PROFIT, Gross: {trade.pnl:2f}, Net: {trade.pnlcomm:2f}")

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            # order if pending we don't place second order
            return

        # Check if we are in market
        if not self.position:
            print(self.position)
            if self.order is not None:
                print(self.order.status)
            # Buy Strategy
            # two day strategy
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log(f"Buy Create, {self.dataclose[-2]:2f}")
                    self.order = self.buy()
        else:
            # Already in market, you can sell
            if len(self) >= (self.bar_executed + 5):
                self.log(f"Sell Create, {self.dataclose[0]}")
                self.order = self.sell()



