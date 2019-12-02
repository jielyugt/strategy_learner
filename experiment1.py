from StrategyLearner import StrategyLearner
from ManualStrategy import ManualStrategy
from marketsimcode import compute_portvals
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt


def experiment1():
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000

    manual = ManualStrategy()
    manual_trades = manual.testPolicy([symbol], sd=sd, ed=ed, sv=sv)
    manual_portval = compute_portvals(manual_trades, start_val = sv, commission=0, impact=0.000)
    print_stats(manual_portval, "Manual Trader")

    learner = StrategyLearner(verbose = False, impact = 0.000)
    learner.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = sv)
    learner_trades = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv)
    learner_portval = compute_portvals(learner_trades, start_val = sv, commission=0, impact=0.000)
    print_stats(learner_portval, "Strategy Learner")
    plot_graphes(manual_portval, learner_portval)

def print_stats(portval, name):
    portval = portval['value']

    # [Cumulative Return]
    cr = portval[-1] / portval[0] - 1

    # adily return in percentage
    dr = (portval / portval.shift(1) - 1).iloc[1:]

    # [Stdev of daily returns]
    sddr = dr.std()

    # [Mean of daily returns]
    adr = dr.mean()

    print("[" + name + "]")
    print("Cumulative return: " + str(cr))
    print("Stdev of daily returns: " + str(sddr))
    print("Mean of daily returns: " + str(adr))
    print()

def plot_graphes(manual_portvals, strategy_portvals):

    # normalize	
    manual_portvals['value'] = manual_portvals['value'] / manual_portvals['value'][0]
    strategy_portvals['value'] = strategy_portvals['value'] / strategy_portvals['value'][0]

    plt.figure(figsize=(14,8))
    plt.title("Manual vs Q Learning Bot")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(manual_portvals, label="manual", color = "green")
    plt.plot(strategy_portvals, label="q learning bot", color = "red")

    plt.legend()
    plt.savefig("experiment1.png", bbox_inches='tight')
    # plt.show()
    plt.clf()

def author():
    return 'jlyu31'

if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    experiment1()

"""

[Manual Trader]
Cumulative return: 0.2246999999999999
Stdev of daily returns: 0.01074570841256326
Mean of daily returns: 0.00045979043433848544

[Strategy Learner]
Cumulative return: 0.0024999999999999467
Stdev of daily returns: 0.014096792695730696
Mean of daily returns: 0.00010429369834201319

"""
