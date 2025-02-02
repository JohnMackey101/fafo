import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# Get realtime finance data using yfinance. Let's try Blackrock.

def fetch_options_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    expiry_dates = ticker.options
    nearest_expiry = expiry_dates[0]
    #Use nearest expiry date for analysis
    options_data = ticker.option_chain(nearest_expiry)
    return options_data.calls, options_data.puts 

blk_calls, blk_puts = fetch_options_data('BLK')

blk_stock_data = yf.Ticker('BLK').history(start="2024-01-01", end="2024-12-31")

plt.figure(figsize=(10,5))
plt.plot(blk_stock_data['Close'])
plt.title('BLK Historical Stock Price')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.grid(True)
plt.show()

class BlackScholesModel:
    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def d1(self):
        return (np.log(self.S / self.K) + ((self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T)))
    
    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)
    
    def call_option_price(self):
        return (self.S * si.norm.cdf(self.d1(), 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * si.norm.cdf((self.d2(), 0.0, 1.0)))
    
    def put_option_price(self):
        return (self.S * np.exp(-self.r * self.T) * si.norm.cdf(-self.d2(), 0.0, 1.0) - self.S * si.norm.cdf(-self.d1(), 0.0, 1.0))
    
bsm = BlackScholesModel(S=100, K=100, T=1, r=0.05, sigma=0.2)
print(f"Call Option Price: {bsm.call_option_price()}")
print(f"Put Option Price: {bsm.put_option_price()}")


