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
        #self.dataclose = self.datas[0].close #* keeps a reference to the close line. Only one level of indirection is later needed to access the close values.
        #self.order = None #* Initialize order status as None, to keep track of pending orders
        
    # def log(self, txt, dt=None):
    #     """
    #     Logging method for orders placed.

    #     Args:
    #         txt (str): Text to log
    #         dt (datetime, optional): Date that logging occurred. Defaults to None.
    #     """
    #     dt = dt or self.datas[0].datetime.date(0)
    #     print('%s, %s' % (dt.isoformat(), txt))

    # def notify_order(self, order):
    #     """
    #     Method to notify when an order has taken place.

    #     Args:
    #         order (order): An order object for the given order in question.
    #     """
    #     if order.status in [order.Submitted, order.Accepted]: #* If order status is IP, do nothing
    #         return
        
    #     if order.status in [order.Completed]: #* If order completed:
    #         if order.isbuy(): #* If you bought, log price
    #             self.log('BUY EXECUTED {}'.format(order.executed.price))
    #         elif order.issell(): #* Else, if you sold, log price
    #             self.log('SELL EXECUTED {}'.format(order.executed.price))
            
    #         self.bar_executed = len(self)
            
    #     elif order.status in [order.Canceled, order.Margin, order.Rejected]: #* Else, if order was rejected/canceled
    #         self.log('Order Canceled/Margin/Rejected')
        
    #     self.order = None #* No pending order

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
        # self.log('Close, %.2f' % self.dataclose[0]) #* Log the closing price of the series from the reference
        
        # if self.order: #* If order is pending
        #     return #* Don't send a second order
        
        # if not self.position: #* If we are in the market:
        #     if self.dataclose[0] < self.dataclose[-1]: #* Potentially buy if stock is down first day
        #         # current close less than previous close

        #         if self.dataclose[-1] < self.dataclose[-2]: #* Stock is down 2 days in a row, buy!
        #             # previous close less than the previous close
        #             # BUY, BUY, BUY!!! (with all possible default parameters)
        #             self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #             self.order = self.buy() #* Keep track of the created order to avoid a 2nd order
        # else:
        #     if len(self) >= (self.bar_executed + 5): #* Sell if we've held position for 5 days
        #         self.log('SELL CREATED {}'.format(self.dataclose[0]))
        #         self.order = self.sell() #* Keep track of the created order to avoid a 2nd order