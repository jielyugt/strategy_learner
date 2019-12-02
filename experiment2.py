from StrategyLearner import StrategyLearner
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals

def experiment2():
    symbol = "JPM"
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000

    learner1 = StrategyLearner(verbose = False, impact = 0.000)
    learner1.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = sv)
    df_trades1 = learner1.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv)
    trades1_portval = compute_portvals(df_trades1, start_val = sv, commission=0, impact=0.000)

    learner2 = StrategyLearner(verbose = False, impact = 0.005)
    learner2.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = sv)
    df_trades2 = learner2.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv)
    trades2_portval = compute_portvals(df_trades2, start_val = sv, commission=0, impact=0.005)

    learner3 = StrategyLearner(verbose = False, impact = 0.01)
    learner3.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = sv)
    df_trades3 = learner3.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv)
    trades3_portval = compute_portvals(df_trades3, start_val = sv, commission=0, impact=0.01)
    plot_graphes(trades1_portval, trades2_portval, trades3_portval)

    long, short = get_trades(df_trades1)
    plot_trades(trades1_portval, long, short, "0", len(long) + len(short))

    long, short = get_trades(df_trades3)
    plot_trades(trades3_portval, long, short, "0.01", len(long) + len(short))

def plot_graphes(trade1, trade2, trade3):

    # normalize	
    trade1['value'] = trade1['value'] / trade1['value'][0]
    trade2['value'] = trade2['value'] / trade2['value'][0]
    trade3['value'] = trade3['value'] / trade3['value'][0]

    plt.figure(figsize=(14,8))
    plt.title("Experiment 2: Impact Value")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(trade1, label="impact: 0.000", color = "green")
    plt.plot(trade2, label="impact: 0.005", color = "red")
    plt.plot(trade3, label="impact: 0.01", color = "blue")

    plt.legend()
    plt.savefig("experiment2.png", bbox_inches='tight')
    # plt.show()
    plt.clf()

def get_trades(df_trades):
    long = []
    short = []
    current = 0
    last_action = 'OUT'
    for date in df_trades.index:
        current += df_trades.loc[date].loc['JPM']
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
    return long, short

def plot_trades(trade, long, short, label, total):

    trade['value'] = trade['value'] / trade['value'][0]

    plt.figure(figsize=(14,8))
    plt.title("Experiment 2 Impact {}, {} trades in total".format(label, str(total)))
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(trade, color = "green")


    for date in short:
        plt.axvline(date, color = "black")
    
    for date in long:
        plt.axvline(date, color = "blue")

    plt.legend()
    plt.savefig("experiment2_{}.png".format(label), bbox_inches='tight')
    # plt.show()
    plt.clf()


def author():
    return 'jlyu31'

if __name__=="__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    experiment2()

