import backtrader as bt
import datetime
from buyandhold import Strat

#* We need to connect a datafeed to a strategy for backtrader to do its thing. 
cerebro = bt.Cerebro()

STARTINGCASH = 1000000 #* Define starting cash at $1M
cerebro.broker.set_cash(STARTINGCASH)

#* Create a Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname='ORCL.csv', #* Oracle stock data from 1995-2014
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2000, 12, 31),
    reverse=False)

cerebro.adddata(data) #* Import data from feed

cerebro.addstrategy(Strat) #* Import strategy to buy and hold from our strategy directory
cerebro.addsizer(bt.sizers.FixedSize, stake=1000) #* Set order size to 1000 shares (default 1)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#* Plot strategy outcome, which uses matplotlib
cerebro.plot() #! Had to install specific version of backtrader package to prevent issue with matplotlib