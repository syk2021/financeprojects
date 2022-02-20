from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance as yf
yf.pdr_override()

# Plot of SPYG and SPYV
spyg = pdr.get_data_yahoo('SPYG', '2000-12-18')
spyv = pdr.get_data_yahoo('SPYV', '2000-12-18')

plt.figure(figsize=(9,5))
plt.plot(spyg.index, spyg.Close, 'r-', label="SPYG")
plt.plot(spyv.index, spyv.Close, 'b', label="SPYV")
plt.grid(True)
plt.legend(loc='best')
plt.show()

plt.scatter(spyg, spyv, marker='.')
plt.show()
