import yfinance as yf
import ta
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class SMAcross(Strategy):
    n1 = 50
    n2 = 100

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n1)
        self.sma2 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()

df = yf.download('FNGU', start='2021-01-01')

# Flatten MultiIndex
df.columns = df.columns.map(lambda x: x[0])

# Optionally reset index
df.reset_index(inplace=True)

# Run the backtest
bt = Backtest(df, SMAcross, cash=100000)
output = bt.run()
print(output)
bt.plot()