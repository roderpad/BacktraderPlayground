import math
import backtrader as bt

class Strat(bt.Strategy):
    """
    Golden cross strategy (https://www.daytradetheworld.com/trading-blog/golden-cross/)

    Args:
        bt (backtrader strategy): Base strategy that is extended here
    """
    params = (('fast', 50), ('slow', 200), ('order_percentage', 0.95), ('ticker', 'SPY'))
    def __init__(self):
        """
        Upon init being called the strategy already has a list of datas that are present in the platform
        This is a standard Python list and datas can be accessed in the order they were inserted.
        The first data in the list self.datas[0] is the default data for trading operations and to keep all strategy elements synchronized (it’s the system clock)
        """
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname='50 day moving average'
        )
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname='200 day moving average'
        )
        
        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def next(self):
        """
        This method will be called on each bar of the system clock (self.datas[0]). This is true until other things come 
        into play like indicators, which need some bars to start producing an output.
        """
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.buy(size=self.size)
                
        if self.position.size > 0:
            if self.crossover < 0:
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()