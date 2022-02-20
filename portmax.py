# December 28, 2021
# Research Question:
# The Two Fund Separation Theorem gives that investors should invest in
# a combination of the market portfolio and the risk free asset.
# The question then is what weight the ratio should put in the risky and risk free asset.
# To research this, this code examines SPY, SPDR S&P 500 Trust ETF, and TLT, the iShares 20 Plus Year Treasury Bond, to examine what weight ratio an investor should put in.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()

# Close Price Changes of SPY and TLT, 2001 - 2021
aapl = pdr.get_data_yahoo('AAPL', '2001-01-01')
msft = pdr.get_data_yahoo('MSFT', '2001-01-01')
pg = pdr.get_data_yahoo('PG', '2001-01-01')
o = pdr.get_data_yahoo('O', '2001-01-01')

plt.figure(figsize=(9,5))
plt.plot(spy.index, spy.Close, 'r--', label="SPY")
plt.plot(tlt.index, tlt.Close, 'b', label="TLT")
plt.grid(True)
plt.legend(loc='best')
plt.show()

## Create a merged dataframe
spyclose = spy[['Close']]
tltclose = tlt[['Close']]
print(spyclose.head())
print(tltclose.head())
df = spyclose.join(tltclose, how="inner", lsuffix="_spy", rsuffix="_tlt")
print(df.head())

## Calculate returns with pct_change(); stored in newdf
dailyret = df.pct_change()
dailyret = dailyret.dropna()
print(dailyret.head())

## Calculate annual returns (dailyreturn.mean() * 252, with 252 being average market days)
annualret = dailyret.mean() * 252
print(annualret)

## Calculate covariance
dailycov = dailyret.cov()
annualcov = dailycov * 252
print(dailycov.head())
print(annualcov)

# A Monte Carlo Simulation with 20,000 different portfolio weights = Efficient Frontier
## Portfolio optimization, done with Sharpe Ratio
port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []
assets = ['SPY', 'TLT']

for _ in range(20000):
    weights = np.random.random(len(assets))
    weights /= np.sum(weights)

    returns = np.dot(weights, annualret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annualcov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns - 0.0147/risk) # 10-Year U.S. government bond yield rate used as risk-free rate in calculation of Sharpe Ratio

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}
for i, s in enumerate(assets):
    portfolio[s] = [weight[i] for weight in port_weights]
portdf = pd.DataFrame(portfolio)
portdf = portdf[['Returns', 'Risk', 'Sharpe'] + [s for s in assets]]

#Maximum Sharpe Ratio Portfolio
max_sharpe = portdf.loc[portdf['Sharpe'] == portdf['Sharpe'].max()]
# Minimum Variance Portfolio (MVP)
min_risk = portdf.loc[portdf['Risk'] == portdf['Risk'].min()]

portdf.plot.scatter(x='Risk', y='Returns', figsize=(10, 7), grid=True)
plt.title("Efficient Frontier of Portfolio of SPY and TLT")
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', s=300) # maximum sharpe ratio portfolio
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='b', s=200) # minimum variance portfolio
plt.xlabel('Portfolio Risk')
plt.ylabel('Portfolio Expected Return')
plt.show()
