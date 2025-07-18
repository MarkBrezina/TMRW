import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta, timezone
import pandas as pd
import yfinance as yf
import numpy as np
import math

# dates in correct format for yahoo finance.
today = date.today() 
today = datetime(today.year,today.month,today.day) #today
one = datetime(today.year-1,today.month,today.day) #one year ago
three = datetime(today.year-3,today.month,today.day) #three years ago
five = datetime(today.year-5,today.month,today.day) #five years ago
ten = datetime(today.year-10,today.month,today.day) #ten years ago
twenty = datetime(today.year-20,today.month,today.day) #twenty years ago

def sdata(x, y, z):
    # x is a stock symbol
    # y is a start date
    # z is an end date
    # kan bruges på commodities, currencies og aktier
    
    #MSFT er en aktier der kan bruges
    #USDEUR=X er en currency der kan bruges
    #GC=F er guld priser
    
    st = pd.DataFrame()
    t = yf.Ticker(x)
    st = t.history(start=y, end=z)
    st.index = pd.to_datetime(st.index).tz_localize(None)
    return(st)

df = pd.DataFrame()
df = sdata("MSFT", five, today)



class backtest:
    
    def __init__(self, data_in, initial):
        self.data = data_in
        self.data = self.data.reset_index(drop = True)
        self.initial = initial
        self.strategy = self._strategy()
        
        self._inventory = 0
        self.inventory = []
        
        self._pnl = self.initial
        self.pnl = []
        
        self._price = 0
        self.price = []
        
    def evaluate(self):
        self.pnl.append(0)
        
        for i in range(len(self.data)-1):
            
            if self.strategy['strategy'][i] == "buy":
                self._inventory = self._inventory + self.initial / self.data['Close'][i+1]
                self.initial = 0
                self._price = self.data['Close'][i+1]
                self.pnl.append(self._pnl)
                self.price.append(self.data['Close'][i+1])
                
            elif self.strategy['strategy'][i] == "sell":
                self._pnl = self._pnl + self.data['Close'][i+1] * self._inventory
                self._inventory = 0
                self._price = self.data['Close'][i+1]
                
                self.pnl.append(self._pnl)
                self.price.append(self.data['Close'][i])
                
            elif self.strategy['strategy'][i] == "":
                self.inventory.append(self._inventory)
                self.pnl.append(self._pnl)
                
                self.price.append(self.data['Close'][i])
        
        if self._inventory != 0:
            self._pnl = self._pnl + self.data['Close'][-1] * self._inventory
        return(self._pnl)
                
    def _strategy(self):
        lst = []
        
        for i in range(1, len(self.data)):
            if i < 5:
                lst.append("")
            else:
            
                if np.mean(self.data['Close'][i-5:i]) > self.data['Close'][i]:
                    lst.append("buy")
                elif np.mean(self.data['Close'][i-5:i]) < self.data['Close'][i]:
                    lst.append("sell")
                else:
                    lst.append("")
        self.df = pd.DataFrame(lst, columns = ["strategy"])
        return(self.df)
    
    def _plot(self):
        fig, (ax1) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

        # Price plot
        ax1[0].set_facecolor('dimgrey')
        ax1[0].plot(self.data.index, self.data['Close'], linewidth = 2, color = "white")

        long_signal_dates = self.df[self.df['strategy'] == "buy"].index
        for date in long_signal_dates:
            ax1[0].annotate('x', xy=(date, self.data.iloc[date, 3]), color='green', fontsize=14, ha='center')

        long_signal_dates = self.df[self.df['strategy'] == "sell"].index
        for date in long_signal_dates:
            ax1[0].annotate('x', xy=(date, self.data.iloc[date, 3]), color='red', fontsize=14, ha='center')

        
        #PNL plot
        ax1[1].plot(bt.pnl)
        long_signal_dates = self.df[self.df['strategy'] == "buy"].index
        for date in long_signal_dates:
            ax1[1].annotate('x', xy=(date, self.pnl[date]), color='green', fontsize=14, ha='center')

        long_signal_dates = self.df[self.df['strategy'] == "sell"].index
        for date in long_signal_dates:
            ax1[1].annotate('x', xy=(date, self.pnl[date]), color='red', fontsize=14, ha='center')
        plt.grid()
        plt.show()



bt = backtest(df, 100)
bt.evaluate()
bt._plot()
