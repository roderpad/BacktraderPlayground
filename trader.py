import os, sys, argparse
import backtrader as bt
import pandas as pd
from Strats.buyandhold import Strat

#* We need to connect a datafeed to a strategy for backtrader to do its thing. 
cerebro = bt.Cerebro()

STARTINGCASH = 1000000 #* Define starting cash at $1M
cerebro.broker.set_cash(STARTINGCASH)

#* Get prices from historical data
orcl_prices = 'Data/ORCL.csv'
spy_prices = pd.read_csv('Data/SPY.csv', index_col='Date', parse_dates=True)

#* Create Data Feeds
# data = bt.feeds.YahooFinanceCSVData(
#     dataname='ORCL.csv', #* Oracle stock data from 1995-2014
#     # Do not pass values before this date
#     fromdate=datetime.datetime(2000, 1, 1),
#     # Do not pass values after this date
#     todate=datetime.datetime(2000, 12, 31),
#     reverse=False)
ORCLyfFeed = bt.feeds.YahooFinanceCSVData(dataname=orcl_prices) #* Oracle stock data from 1995-2014, from Yahoo data download
SPYyfFeed = bt.feeds.PandasData(dataname=spy_prices) #* S&P500 stock data from 2000-current, from Yahoo data download

cerebro.adddata(ORCLyfFeed) #* Import ORCL data from feed

cerebro.addstrategy(Strat) #* Import strategy to buy and hold from our strategy directory
cerebro.addsizer(bt.sizers.FixedSize, stake=1000) #* Set order size to 1000 shares (default 1)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#* Plot strategy outcome, which uses matplotlib
cerebro.plot() #! Had to install specific version of backtrader package to prevent issue with matplotlib