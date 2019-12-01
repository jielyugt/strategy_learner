"""  		   	  			  	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			  	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			  	 		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			  	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			  	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			  	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			  	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			  	 		  		  		    	 		 		   		 		  
or edited.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			  	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			  	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			  	 		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Jie Lyu  		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jlyu31  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903329676  		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import util as ut  		   	  			  	 		  		  		    	 		 		   		 		  
import random  		   
import QLearner as ql	  	
import indicators	
from marketsimcode import compute_portvals  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # constructor  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			  	 		  		  		    	 		 		   		 		  
        self.impact = impact  
        random.seed(903329676)	 
        # initialize the learner
        # 3 actions: 1: LONG, 2: CASH, 3: SHORT
        self.learner = ql.QLearner(num_states=96,\
            num_actions = 3, \
            alpha = 0.2, \
            gamma = 0.9, \
            rar = 0.98, \
            radr = 0.999, \
            dyna = 200, \
            verbose=False)  	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  	
        
        # get indicator data
        ema_20, ema_30, ema_50, macd, tsi = get_discretized_indicators(sd, ed, symbol)

        # set up
        df_prices, df_trades = get_df_prices(sd, ed, symbol)
        df_trades = df_trades.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
        df_trades[:] = 0
        dates = df_prices.index
	  	 		  		  		    	 		 		   		 		  			  	 		  		  		    	 		 		   		 		  

        curr_position = 0
        curr_cash = sv
        prev_cash = sv

        # train the learner
        for i in range(1, len(dates)):
            today = dates[i]
            yesterday = dates[i - 1]

            s_prime = compute_current_state(curr_position, ema_20.loc[today], 
                ema_30.loc[today], ema_50.loc[today], macd.loc[today], tsi.loc[today])

            r = curr_position * df_prices.loc[today].loc[symbol] + curr_cash - curr_position * df_prices.loc[yesterday].loc[symbol] - prev_cash

            # {0: SHORT, 1: CASH, 2: LONG}
            next_action = self.learner.query(s_prime, r)
            if next_action == 0:
                trade = -1000 - curr_position
            elif next_action == 1:
                trade = -curr_position
            else:
                trade = 1000 - curr_position
            
            # if self.verbose:
            #     print("This trade will return: " + str(r))
            #     print()
            #     print(today)
            #     print("Price today: " + str(df_prices.loc[today].loc[symbol]))
            #     print(decode_current_state(s_prime))
            #     print("Trade: {}".format(trade))

            curr_position += trade
            df_trades.loc[today].loc[symbol] = trade

            if trade > 0:
                impact = self.impact
            else:
                impact = -self.impact
            
            prev_cash = curr_cash
            curr_cash += -df_prices.loc[today].loc[symbol] * (1 + impact) * trade
        
        print("[benchmark]")
        print(get_benchmark(sd, ed, sv))
        print()

        print("[traning performance]")
        print(compute_portvals(df_trades, start_val = sv, commission=0, impact=0.000))
        print()

        return df_trades


  	  			  	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			  	 		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):  		   	  			  	 		  		  		    	 		 		   		 		  

        # get indicator data
        ema_20, ema_30, ema_50, macd, tsi = get_discretized_indicators(sd, ed, symbol)

        # set up
        df_prices, df_trades = get_df_prices(sd, ed, symbol)
        df_trades = df_trades.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
        df_trades[:] = 0
        dates = df_prices.index
	  	 		  		  		    	 		 		   		 		  			  	 		  		  		    	 		 		   		 		  
        curr_position = 0

        # train the learner
        for i in range(1, len(dates)):
            today = dates[i]
            yesterday = dates[i - 1]

            s_prime = compute_current_state(curr_position, ema_20.loc[today], 
                ema_30.loc[today], ema_50.loc[today], macd.loc[today], tsi.loc[today])

            # {0: SHORT, 1: CASH, 2: LONG}
            next_action = self.learner.querysetstate(s_prime)
            if next_action == 0:
                trade = -1000 - curr_position
            elif next_action == 1:
                trade = -curr_position
            else:
                trade = 1000 - curr_position
            
            # if self.verbose:
            #     print(today)
            #     print("Price today: " + str(df_prices.loc[today].loc[symbol]))
            #     print(decode_current_state(s_prime))
            #     print("Trade: {}".format(trade))
            #     print()

            curr_position += trade
            df_trades.loc[today].loc[symbol] = trade
  
        print("[benchmark]")
        print(get_benchmark(sd, ed, sv))
        print()

        print("[traning performance]")
        print(compute_portvals(df_trades, start_val = sv, commission=0, impact=0.000))
        print()  	  			  	 		  		  		    	 		 		   		 		  
	   	  			  	 		  		  		    	 		 		   		 		  
        return df_trades  		  

def get_df_prices(sd, ed, symbol):
    syms=[symbol]  		   	  			  	 		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
    df = ut.get_data(syms, dates)	   	  			  	 		  		  		    	 		 		   		 		  
    prices = df[syms]
    prices = prices.ffill().bfill()
    spy = df[['SPY']]
    return prices, spy

def get_discretized_indicators(sd, ed, symbol):
    prices, _ = get_df_prices(sd, ed, symbol)

    # EMA 2 States: Price <= EMA: 0, Price > EMA: 1
    ema_20 = indicators.ema(sd, ed, symbol, window_size = 20)
    ema_30 = indicators.ema(sd, ed, symbol, window_size = 30)
    ema_50 =indicators.ema(sd, ed, symbol, window_size = 50)

    ema_20 = (prices > ema_20) * 1
    ema_30 = (prices > ema_30) * 1
    ema_50 = (prices > ema_50) * 1

    # MACD 2 States: MACD <= Signal: 0, MACD > Signal: 1
    macd_raw, macd_signal = indicators.macd(sd, ed, symbol)
    macd = (macd_raw > macd_signal) * 1

    # TSI 2 States: TSI <= 0: 0, TSI > 0: 1
    tsi = indicators.tsi(sd, ed, symbol)
    tsi = (tsi > 0) * 1

    return ema_20, ema_30, ema_50, macd, tsi

def compute_current_state(position, ema_20, ema_30, ema_50, macd, tsi):
    # 96 states in total, each permutation of indicators + position return between 0 and 95
    # position: -1000, ema_20: 0, ema_30: 0, ema_50: 0, macd: 0, tsi:0 => 0
    # position: 1000, ema_20: 1, ema_30: 1, ema_50: 1, macd: 1, tsi:1 => 95

    idx = 0
    if position == 0:
        idx += 32
    elif position == 1000:
        idx += 64
    idx += ema_20 * 16 + ema_30 * 8 + ema_50 * 4 + macd * 2 + tsi
    return int(idx)

def decode_current_state(idx):
    output = ""
    if idx >= 64:
        output += "Position: Long\n"
    elif idx >= 32:
        output += "Position: CASH\n"
    else:
        output += "Position: SHORT\n"
    idx %= 32
    if idx >= 16:
        output += "Price > EMA 20\n"
    else:
        output += "Price < EMA 20\n"
    idx %= 16
    if idx >= 8:
        output += "Price > EMA 30\n"
    else:
        output += "Price < EMA 30\n"
    idx %= 8
    if idx >= 4:
        output += "Price > EMA 50\n"
    else:
        output += "Price < EMA 50\n"
    idx %= 4
    if idx >= 2:
        output += "MACD > Signal\n"
    else:
        output += "MACD < Signal\n"
    idx %= 2
    if idx >= 1:
        output += "TSI > 0"
    else:
        output += "TSI < 0"
    return output

def get_benchmark(sd, ed, sv):
    # starting with $100,000 cash, investing in 1000 shares of JPM and holding that position

    df_trades = ut.get_data(['SPY'], pd.date_range(sd, ed))
    df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
    df_trades[:] = 0
    df_trades.loc[df_trades.index[0]] = 1000
    portvals = compute_portvals(df_trades, sv, commission=0, impact=0.005)
    return portvals

def test():
    learner = StrategyLearner(verbose = True, impact = 0.005) # constructor
    learner.addEvidence(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
    df_trades = learner.testPolicy(symbol = "JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000)

def author():
    return 'jlyu31'

if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    # print("One does not simply think up a strategy")  	
    test()

# # example usage of the old backward compatible util function  		   	  			  	 		  		  		    	 		 		   		 		  
# syms=[symbol]  		   	  			  	 		  		  		    	 		 		   		 		  
# dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
# prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
# prices = prices_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
# prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
# if self.verbose: print(prices)  		   	  			  	 		  		  		    	 		 		   		 		  
                                                                                    
# # example use with new colname  		   	  			  	 		  		  		    	 		 		   		 		  
# volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
# volume = volume_all[syms]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
# volume_SPY = volume_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
# if self.verbose: print(volume)






# # here we build a fake set of trades  		   	  			  	 		  		  		    	 		 		   		 		  
# # your code should return the same sort of data  		   	  			  	 		  		  		    	 		 		   		 		  
# dates = pd.date_range(sd, ed)  		   	  			  	 		  		  		    	 		 		   		 		  
# prices_all = ut.get_data([symbol], dates)  # automatically adds SPY  		   	  			  	 		  		  		    	 		 		   		 		  
# trades = prices_all[[symbol,]]  # only portfolio symbols  		   	  			  	 		  		  		    	 		 		   		 		  
# trades_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[:,:] = 0 # set them all to nothing  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[0,:] = 1000 # add a BUY at the start  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[40,:] = -1000 # add a SELL  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[41,:] = 1000 # add a BUY  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[60,:] = -2000 # go short from long  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[61,:] = 2000 # go long from short  		   	  			  	 		  		  		    	 		 		   		 		  
# trades.values[-1,:] = -1000 #exit on the last day  		   	  			  	 		  		  		    	 		 		   		 		  
# if self.verbose: print(type(trades)) # it better be a DataFrame!  		   	  			  	 		  		  		    	 		 		   		 		  
# if self.verbose: print(trades)  		   	  			  	 		  		  		    	 		 		   		 		  
# if self.verbose: print(prices_all)  	







# def test_compute_current_state():
#     lis = []
#     for position in [-1000, 0, 1000]:
#         for ema_20 in range(2):
#             for ema_30 in range(2):
#                 for ema_50 in range(2):
#                     for macd in range(2):
#                         for tsi in range(2):
#                             lis.append(compute_current_state(position, ema_20, ema_30, ema_50, macd, tsi))
#     print(lis == list(range(96)))