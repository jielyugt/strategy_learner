"""
Code implementing a ManualStrategy object
It should implement testPolicy() which returns a trades data frame (see below)
The main part of this code should call marketsimcode as necessary to generate the plots used in the report
"""

"""
Student Name: Jie Lyu 		   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jlyu31  		   	  			  	 		  		  		    	 		 		   		 		  
GT ID: 903329676 
"""


"""
[Constrains]
possible actions {-2000, -1000, 0, 1000, 2000}
possible positions {-1000, 0, 1000}
Commission: $9.95, Impact: 0.005

[Policy]
If price goes up tomorrow, I go long.
If price goes down tomorrow, I go short.
"""




from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import indicators


class ManualStrategy:

    def testPolicy(self, symbol, sd, ed, sv):

        # setting up
        symbol = symbol[0]
        df = get_data([symbol], pd.date_range(sd, ed))
        df_price = df[[symbol]]
        df_price = df_price.ffill().bfill()
        normalized_df_price = df_price[symbol] / df_price[symbol][0]

        df_trades = df[['SPY']]
        df_trades = df_trades.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
        df_trades[:] = 0
        dates = df_trades.index

        # getting indicators
        ema_20 = indicators.ema(sd, ed, symbol, plot=True, window_size=20)
        ema_20 = ema_20[symbol] / ema_20[symbol][0]

        macd_raw, macd_signal = indicators.macd(sd, ed, symbol, plot=True)
        tsi = indicators.tsi(sd, ed, symbol, plot=True)

        # current_cash = sv
        current_position = 0
        last_action = 0

        # making trades
        for i in range(len(dates)):
            today = dates[i]
            last_action += 1
            
            # EMA_20 Vote
            normalized_df_price_today = normalized_df_price.loc[today]
            ema_20_today = ema_20.loc[today]
            # if normalized_df_price_today > ema_20_today + 0.1:
            if normalized_df_price_today > ema_20_today:
                ema_vote = 1
            # elif normalized_df_price_today < ema_20_today - 0.1:
            elif normalized_df_price_today < ema_20_today:
                ema_vote = -1
            else:
                ema_vote = 0
            
            # MACD Vote
            macd_raw_today = macd_raw.loc[today].loc[symbol]
            macd_signal_today = macd_signal.loc[today].loc[symbol]
            # if macd_signal_today > macd_raw_today + 0.2:
            if macd_signal_today > macd_raw_today:
                macd_vote = 2
            # elif macd_signal_today < macd_raw_today - 0.2:
            elif macd_signal_today < macd_raw_today:
                macd_vote = -10
            else:
                macd_vote = 1
            
            # TSI vote
            tsi_today = tsi.loc[today].loc[symbol]
            # if tsi_today > 0.05:
            if tsi_today > 0.1:
                tsi_vote = 1
            # elif tsi_today < -0.05:
            elif tsi_today < 0.1:        
                tsi_vote = -1
            else:
                tsi_vote = 0

            # pooling the votes
            pool = macd_vote + tsi_vote + ema_vote
            if pool >= 3:
                # long
                action = 1000 - current_position

            elif pool <= -3:
                # short
                action = - 1000 - current_position
            else:
                # out
                action = -current_position

            # don't trade too frequent
            if last_action >= 3:
                df_trades.loc[dates[i]].loc[symbol] = action
                current_position += action
                last_action = 0

        return df_trades



def get_benchmark(sd, ed, sv):
    # starting with $100,000 cash, investing in 1000 shares of JPM and holding that position

    df_trades = get_data(['SPY'], pd.date_range(sd, ed))
    df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
    df_trades[:] = 0
    df_trades.loc[df_trades.index[0]] = 1000
    portvals = compute_portvals(df_trades, sv, commission=9.95, impact=0.005)
    return portvals

# takes in pd.df and prints stats
def print_stats(benchmark, theoretical):
    benchmark, theoretical = benchmark['value'], theoretical['value']

    # [Cumulative Return]
    cr_ben = benchmark[-1] / benchmark[0] - 1
    cr_the = theoretical[-1] / theoretical[0] - 1

    # adily return in percentage
    dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
    dr_the = (theoretical / theoretical.shift(1) - 1).iloc[1:]

    # [Stdev of daily returns]
    sddr_ben = dr_ben.std()
    sddr_the = dr_the.std()

    # [Mean of daily returns]
    adr_ben = dr_ben.mean()
    adr_the = dr_the.mean()

    print("")
    print("[ManualStrategy]")
    print("Cumulative return: " + str(cr_the))
    print("Stdev of daily returns: " + str(sddr_the))
    print("Mean of daily returns: " + str(adr_the))
    print("")
    print("[Benchmark]")
    print("Cumulative return: " + str(cr_ben))
    print("Stdev of daily returns: " + str(sddr_ben))
    print("Mean of daily returns: " + str(adr_ben))
    print("")

# takes in pd.df and plots graphs
# TODO: implement trade points
def plot_graphes(benchmark_portvals, theoretical_portvals, short, long, label):

    # normalize	
    benchmark_portvals['value'] = benchmark_portvals['value'] / benchmark_portvals['value'][0]
    theoretical_portvals['value'] = theoretical_portvals['value'] / theoretical_portvals['value'][0]

    plt.figure(figsize=(14,8))
    plt.title("ManualStragety on " + label)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(benchmark_portvals, label="benchmark", color = "green")
    plt.plot(theoretical_portvals, label="manual", color = "red")

    if label == 'in_sample':
        for date in short:
            plt.axvline(date, color = "black")
        
        for date in long:
            plt.axvline(date, color = "blue")

    plt.legend()
    plt.savefig("report/manual_{}.png".format(label), bbox_inches='tight')
    # plt.show()
    plt.clf()


def report():

    # testing conditions

    # IS
    sv = 100000
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009,12,31)
    symbol = ['JPM']

    # OOS
    sv = 100000
    sd = dt.datetime(2010, 1, 1)
    ed = dt.datetime(2011,12,31)
    symbol = ['JPM']

    # get theoretical performance
    ms = ManualStrategy()
    df_trades = ms.testPolicy(symbol, sd=sd, ed=ed, sv=sv)
    manual_portvals = compute_portvals(df_trades, sv, commission=9.95, impact=0.005)

    # get benchmark performance
    benchmark_portvals = get_benchmark(sd, ed, sv)

    # get stats
    print_stats(benchmark_portvals, manual_portvals)

    # plot graph

    long = []
    short = []
    current = 0
    last_action = 'OUT'
    for date in df_trades.index:
        current += df_trades.loc[date].loc[symbol[0]]
        if current < 0:
            if last_action == 'OUT' or last_action == 'LONG':
                last_action = 'SHORT'
                short.append(date)
        elif current > 0:
            if last_action == 'OUT' or last_action == 'SHORT':
                last_action = 'LONG'
                long.append(date)
        else:
            last_action = 'OUT'

    # plot_graphes(benchmark_portvals, manual_portvals, short, long, 'in_sample')
    plot_graphes(benchmark_portvals, manual_portvals, short, long, 'out_sample')


def author():
    return 'jlyu31'

if __name__ == "__main__":
    report()
