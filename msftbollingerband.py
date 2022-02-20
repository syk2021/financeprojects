# December 28, 2021

# MSFT Bollinger Band and Intraday Intensity (II)

# Intraday Intensity
## Intraday Intensity Index is a volume-based technical indicator that examines volume and a security's price.
## The Intraday Intensity Index can be used to follow how intraday highs and lows are moving with volume in comparison to the previous day's closing price.

import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

msft = pdr.get_data_yahoo('msft', '2021-01-01')

msft['SMA20'] = msft['Close'].rolling(window=20).mean()
msft['stdev'] = msft['Close'].rolling(window=20).std()
msft['upper'] = msft['SMA20'] + (msft['stdev'] * 2)
msft['lower'] = msft['SMA20'] - (msft['stdev'] * 2)
msft['PB'] = (msft['Close'] - msft['lower']) / (msft['upper'] - msft['lower'])

msft['II'] = (2 * msft['Close'] - msft['High'] - msft['Low'])/(msft['High'] - msft['Low']) * msft['volume']
msft['IIP21'] = msft['II'].rolling(window=21).sum()/msft['Volume'].rolling(window=21).sum()*100
msft = msft.dropna()

plt.figure(figsize=(9, 9))
msft.subplot(3, 1, 1)
plt.title('MSFT Bollinger Band (20 day, 2 std) - Reversals')
plt.plot(msft.index, msft['Close'], 'b', label='Close')
plt.plot(msft.index, msft['upper'], 'r--', label='Upper band')
plt.plot(msft.index, msft['SMA20'], 'k--', label='Simple Moving Average 20')
plt.plot(msft.index, msft['lower'], 'c--', label='Lower band')
plt.fill_between(msft.index, msft['upper'], msft['lower'], color='0.9')
plt.legend(loc='best')

plt.subplot(3, 1, 2)
plt.plot(msft.index, msft['PB'], 'b', label='%B')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(3, 1, 3)
plt.bar(msft.index, msft['IIP21'], color='g', label='II% 21day')
for i in range(0, len(msft.close)):
    if msft.PB.values[i] < 0.05 and msft.IIP21.values[i] > 0:
        plt.plot(msft.index.values[i], 0, 'r^')
    elif msft.PB.values[i] > 0.95 and msft.IIP21.values[i] < 0:
        plt.plot(msft.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()
