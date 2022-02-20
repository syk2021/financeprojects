import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

apple = pdr.get_data_yahoo('AAPL', start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')

# Make plot of Close Prices of AAPL and MSFT
plt.plot(apple.index, apple.Close, 'b', label='AAPL')
plt.plot(msft.index, msft.Close, 'r--', label='MSFT')
plt.legend(loc='best')
plt.show()

# Make plot of Cumulative Sum of Close Price Changes of AAPL and MSFT
apple_dpc = (apple['Close']-apple['Close'].shift(1)) / apple['Close'].shift(1) * 100
apple_dpc_cs = apple_dpc.cumsum()

plt.plot(apple.index, apple_dpc_cs, 'r--', label="Apple")
plt.show()