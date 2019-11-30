"""
Your code that implements your indicators as functions that operate on dataframes
The "main" code in indicators.py should generate the charts that illustrate your indicators in the report
"""

"""
Student Name: Jie Lyu 		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jlyu31  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903329676 
"""


import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data


# Exponential Moving Average
# price < ema, BUY
# price > ema, SELL
# window_size is the lag in days
def ema(sd, ed, symbol, plot = False, window_size = 20):

    # look up history to calculate the ema for the first window_size - 1 days
    delta = dt.timedelta(window_size * 2)
    extedned_sd = sd - delta

    df_price = get_data([symbol], pd.date_range(extedned_sd, ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()

    df_ema = df_price.ewm(span=window_size, adjust=False).mean()

    # remove history price
    df_ema = df_ema.truncate(before=sd)

    return df_ema


# MACD: Moving Average Convergence Divergence
# macd_signal > macd_raw, SELL
# macd_signal < macd_raw, BUY
def macd(sd, ed, symbol, plot = False):

    # look up history to calculate the ema for the 28 days
    # since the max ema windows size is 26, we can say 52 is safe
    delta = dt.timedelta(52)
    extedned_sd = sd - delta

    df_price = get_data([symbol], pd.date_range(extedned_sd, ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()

    ema_12 = df_price.ewm(span=12, adjust=False).mean()
    ema_26 = df_price.ewm(span=26, adjust=False).mean()
    macd_raw = ema_12 - ema_26
    macd_signal = macd_raw.ewm(span=9, adjust=False).mean()

    # remove history price
    df_price = df_price.truncate(before=sd)
    ema_12 = ema_12.truncate(before=sd)
    ema_26 = ema_26.truncate(before=sd)
    macd_raw = macd_raw.truncate(before=sd)
    macd_signal = macd_signal.truncate(before=sd)
    return macd_raw, macd_signal


# TSI: True Strength Index
# tsi < 0, SELL
# tsi > 0, BUY
# add a cushion to be more condifent e.g. tsi < -0.05 and tsi > 0.05
def tsi(sd, ed, symbol, plot = False):

    # look up history to calculate the ema for the 24 days
    # since the max ema windows size is 20, we can say 50 is safe
    delta = dt.timedelta(70)
    extedned_sd = sd - delta

    df_price = get_data([symbol], pd.date_range(extedned_sd, ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()

    # calculate, smoothing and double smoothing price change
    diff = df_price - df_price.shift(1)
    ema_25 = diff.ewm(span=25, adjust=False).mean()
    ema_13 = ema_25.ewm(span=13, adjust=False).mean()

    # calculate, smoothing and double smoothing absolute price change
    abs_diff = abs(diff)
    abs_ema_25 = abs_diff.ewm(span=25, adjust=False).mean()
    abs_ema_13 = abs_ema_25.ewm(span=13, adjust=False).mean()

    df_tsi = ema_13 / abs_ema_13

    # remove history price
    df_tsi = df_tsi.truncate(before=sd)

    return df_tsi

def author():
	return 'jlyu31'

if __name__ == "__main__":
	print("indicates something")