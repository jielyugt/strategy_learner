"""
An improved version of your marketsim code that accepts a "trades" data frame (instead of a file)
"""
"""
Student Name: Jie Lyu 		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jlyu31  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903329676 
"""

import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import os  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			  	 		  		  		    	 		 		   		 		  


def compute_portvals(orders_df, start_val = 1000000, commission=9.95, impact=0.005):  		   	  			  	 		  		  		    	 		 		   		 		  

    ##### setting up
    start_date, end_date, orders_dates = get_dates(orders_df)
    portvals = get_data(['SPY'], pd.date_range(start_date, end_date), addSPY=True, colname = 'Adj Close')
    portvals = portvals.rename(columns={'SPY': 'value'})
    dates = portvals.index
    
    #TODO Modification for Project 6
    symbol = orders_df.columns[0]

    ##### my account
    current_cash = start_val
    shares_owned = {}           # symbol (str) -> number (int)
    symbol_table = {}        # symbol (str) -> prices (pd.df)

    ##### going through dates
    for date in dates:


        #TODO Modification for Project 6
        trade = orders_df.loc[date].loc[symbol]

        if trade != 0:
            if trade < 0:
                order = 'SELL'
                shares = abs(trade)
            else:
                order = 'BUY'
                shares = trade
            
            current_cash, shares_owned, symbol_table = \
                update_share_cash(symbol, order, shares, current_cash, shares_owned, symbol_table, date, end_date, commission, impact)
        
        ### calculating current protfolio value
        portvals.loc[date].loc['value'] = compute_portval(date, current_cash, shares_owned, symbol_table)

    return portvals  		    



"""########
Helper functions for compute_portvals
"""########


# returns the start_date, end_date and orders_dates
def get_dates(orders_df):
    orders_dates = orders_df.index
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    return start_date, end_date, orders_dates


# update current_cash and shares_owned from an order
def update_share_cash(symbol, order, shares, current_cash, shares_owned, symbol_table, curr_date, end_date, commission, impact):

    # if we have not loaded the symbol information yet
    if symbol not in symbol_table:
        # get the df for the symbol
        symbol_df = get_data([symbol], pd.date_range(curr_date, end_date), addSPY=True, colname = 'Adj Close')  
        # back fill and forward fill missing informations on market opend dates
        symbol_df = symbol_df.ffill().bfill()
        # add the symbol df to symbol_table
        symbol_table[symbol] = symbol_df

    # update the share and cash information
    if order == 'BUY':
        share_change = shares
        cash_change = -symbol_table[symbol].loc[curr_date].loc[symbol] * (1 + impact) * shares
    elif order == 'SELL':
        share_change = -shares
        cash_change = symbol_table[symbol].loc[curr_date].loc[symbol] * (1 - impact) * shares
    else:
        print('ERROR: unknow order type')

    shares_owned[symbol] = shares_owned.get(symbol, 0) + share_change
    current_cash += cash_change - commission

    return current_cash, shares_owned, symbol_table


# compute the portfolio value for a day
def compute_portval(curr_date, current_cash, shares_owned, symbol_table):
    shares_worth = 0
    for symbol in shares_owned:
        shares_worth += symbol_table[symbol].loc[curr_date].loc[symbol] * shares_owned[symbol]
    return current_cash + shares_worth


"""########
end of helper functions
"""########


def author():
    return 'jlyu31'
	  			  	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    pass