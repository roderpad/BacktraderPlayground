import sys, argparse
import backtrader as bt
import pandas as pd
from Strats.buyandhold5days import Strat as BuyAndHold5days
from Strats.goldencross import Strat as GoldenCross

#* Create dict of available strategies
strats = {
    "golden_cross": GoldenCross,
    "buy_hold5days": BuyAndHold5days
}

#* Create dict of available tickers
tickerData = {
    "ORCL": 'Data/ORCL.csv',
    "SPY": 'Data/SPY.csv'
}

#* Get input information
parser = argparse.ArgumentParser() #* Initialize parser
parser.add_argument("strategy", help="which strat to run", type=str) #* File runs with expected "strategy" argument
parser.add_argument("ticker", help="ticker symbol", type=str) #* Which data to use
parser.add_argument("starting_cash", help="how much cash to start with", type=float) #* How much cash to start with
parser.add_argument("order_size", help="typical order size", type=float) #* How many shares to order per order
args = parser.parse_args() #* Parse input arguments
strat = args.strategy
ticker = args.ticker
STARTINGCASH = args.starting_cash #* Define starting cash
ORDERSIZE = args.order_size #* Define order size

if not args.strategy in strats: #* If input args doesn't include a valid strategy, inform and bail
    print("Invalid strategy, must be one of {}".format(strats.keys()))
    sys.exit()
    
if not args.ticker in tickerData: #* If input args doesn't include data that we have, inform and bail
    print("Invalid ticker, must be one of {} (or add this data and retry)".format(strats.keys())) #TODO: If it data doesn't exist, get it programmatically
    sys.exit()

#* We need to connect a datafeed to a strategy for backtrader to do its thing. 
cerebro = bt.Cerebro()
cerebro.broker.set_cash(STARTINGCASH)

#* Get prices from historical data
#TODO: Automate this
orcl_prices = 'Data/ORCL.csv'
spy_prices = pd.read_csv('Data/SPY.csv', index_col='Date', parse_dates=True)

#* Create Data Feeds
#TODO: Allow for inputing daterange in args
# data = bt.feeds.YahooFinanceCSVData(
#     dataname='ORCL.csv', #* Oracle stock data from 1995-2014
#     # Do not pass values before this date
#     fromdate=datetime.datetime(2000, 1, 1),
#     # Do not pass values after this date
#     todate=datetime.datetime(2000, 12, 31),
#     reverse=False)
if ticker == 'ORCL':
    Feed = bt.feeds.YahooFinanceCSVData(dataname=orcl_prices) #* Oracle stock data from 1995-2014, from Yahoo data download
elif ticker == 'SPY':
    Feed = bt.feeds.PandasData(dataname=spy_prices) #* S&P500 stock data from 2000-current, from Yahoo data download

cerebro.adddata(Feed) #* Import data from feed

cerebro.addstrategy(strats[strat]) #* Import strategy to buy and hold from our strategy directory
cerebro.addsizer(bt.sizers.FixedSize, stake=ORDERSIZE) #* Set order size (default 1)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#* Plot strategy outcome, which uses matplotlib
cerebro.plot() #! Had to install specific version of backtrader package to prevent issue with matplotlib