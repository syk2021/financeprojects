# December 28, 2021

# Bollinger Band
# A project exploring the Bollinger Band of AAPL.

# Definition of Bollinger Band
# A Bollinger Band gives a set of trendlines plotted two standard deviations (both positively and negatively) away from
# the simple moving average (20-day SMA) of a security's price.
# The band gives investors insight into when an asset is oversold or overbought. 
# The closer prices move to the upper band, the more overbought the market,
# and the closer prices move to the lower band, the more oversold the market.

import matplotlib.pyplot as plt
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

aapl = pdr.get_data_yahoo('aapl', '2020-01-01')

# Calculate 20-Day Simple Moving Average (SMA20) and standard deviation
aapl['SMA20'] = aapl['Close'].rolling(window=20).mean()
aapl['stdev'] = aapl['Close'].rolling(window=20).std()

# Upper and lower bands
aapl['upper'] = aapl['SMA20'] + (2 * aapl['stdev'])
aapl['lower'] = aapl['SMA20'] - (2 * aapl['stdev'])

# Bollinger Band Percent (BB %B) quantifies a symbol relative to the Bollinger Bands.
# %B = 1 if closing price is at upper band, and exceeds 1 if above the upper band.
# %B = 0.5 if closing price is at the middle.
# %B = 0 if closing price is at lower band, and is below 0 if below the lower band.
aapl['PB'] = (aapl['Close'] - aapl['lower']) / (aapl['upper'] - aapl['lower'])
aapl['bandwidth'] = (aapl['upper'] - aapl['lower']) / aapl['SMA20'] * 100

# Bollinger Band and Money Flow Index (MFI)
aapl['TP'] = (aapl['High'] + aapl['Low'] + aapl['Close']) / 3 # Calculation of TP (Typical Price)
aapl['PMF'] = 0 # Positive Money Flow
aapl['NMF'] = 0 # Negative Money Flow
for i in range(len(aapl.Close)-1):
    if aapl.TP.values[i] < aapl.TP.values[i+1]: # If Positive Money Flow
        aapl.PMF.values[i+1] = aapl.TP.values[i+1] * aapl.Volume.values[i+1]
        aapl.NMF.values[i+1] = 0
    else: # Else Negative Money Flow
        aapl.NMF.values[i+1] = aapl.TP.values[i+1] * aapl.volume.values[i+1]
        aapl.PMF.values[i+1] = 0
aapl['MFR'] = aapl.PMF.rolling(window=10).sum() / aapl.NMF.rolling(window=10).sum() # Money Flow Ratio
aapl['MFI10'] = 100 - 100 / (1 + aapl['MFR'])
aapl = aapl[19:]

plt.figure(figsize=(9,5))
plt.subplot(2, 1, 1)
plt.plot(aapl.index, aapl['Close'], color='#0000ff', label='Close')
plt.plot(aapl.index, aapl['upper'], 'r--', label = 'Upper band')
plt.plot(aapl.index, aapl['SMA20'], 'k--', label="Simple Moving Average")
plt.plot(aapl.index, aapl['lower'], 'c--', label='Lower band')
plt.fill_between(aapl.index, aapl['upper'], aapl['lower'], color='0.9')
for i in range(len(aapl.Close)): # Trend Following Buy-Sell Strategy
    if aapl.PB.values[i] > 0.8 and aapl.MFI10.values[i] > 80:
        plt.plot(aapl.index.values[i], aapl.Close.values[i], 'r^') # a red up triangle marks where investor should buy
    elif aapl.PB.values[i] < 0.2 and aapl.MFI10.values[i] < 20:
        plt.plot(aapl.index.values[i], aapl.Close.values[i], 'bv') # a blue down triangle marks where investor should sell
plt.legend(loc='best')
plt.title('AAPL Bollinger Band (20 day, 2 std)')
plt.show()

plt.subplot(2, 1, 2)
plt.plot(aapl.index, aapl['PB'] * 100, color='b', label='%B * 100')
plt.plot(aapl.index, aapl['MFI10'], 'g--', label='MFI(10 day)')
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])
for i in range(len(aapl.Close)):
    if aapl.PB.values[i] > 0.8 and aapl.MFI10.values[i] > 80:
        plt.plot(aapl.index.values[i], 0, 'r^')
    elif aapl.PB.values[i] < 0.2 and aapl.MFI10.values[i] < 20:
        plt.plot(aapl.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()

# Several Notes, from Investopedia:
## Because standard deviation is a measure of volatility, when markets become more volatile, bands widen, whereas in less volatile periods, bands contract.
## The Squeeze
### The squeeze is when Bollinger Bands come together and constrict the moving average.
### The squeeze occurs in periods of low volatility, and is considered by traders to be a potential sign of future increased volatility and possible trading opportunities.
### Conversely, the wider the bands move apart, the more likely the chance of a decrease in volatility and greater the possibility of exiting a trade.
### Squeeze can be examined with the bandwidth variable in the aapl dataframe.
### Per the 68-95-99.7 Rule from statistics, price will be in between the bands 95% of the time. Thus any price movement that exceeds the bands is a breakout (a rare event).

