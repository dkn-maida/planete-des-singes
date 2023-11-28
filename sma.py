import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch historical data for ETH
eth_data = yf.download('ETH-USD', start='2020-01-01', end='2023-01-01')

# Calculate the 50-day SMA
eth_data['SMA'] = eth_data['Close'].rolling(window=5).mean()

# Implement the strategy
eth_data['Position'] = np.where(eth_data['Close'] > eth_data['SMA'], 1, 0)
eth_data['Strategy'] = eth_data['Position'].shift(1) * eth_data['Close'].pct_change()
eth_data['Buy_and_Hold'] = eth_data['Close'].pct_change()

# Calculate cumulative returns
eth_data['Strategy_Cumulative'] = (1 + eth_data['Strategy'].fillna(0)).cumprod()
eth_data['Buy_and_Hold_Cumulative'] = (1 + eth_data['Buy_and_Hold'].fillna(0)).cumprod()

# Plot cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(eth_data['Strategy_Cumulative'], label='Strategy')
plt.plot(eth_data['Buy_and_Hold_Cumulative'], label='Buy and Hold')
plt.title('Strategy vs Buy and Hold Cumulative Returns')
plt.legend()
plt.show()

# Calculate performance metrics
annual_return = eth_data['Strategy'].mean() * 252
annual_volatility = eth_data['Strategy'].std() * np.sqrt(252)
sharpe_ratio = annual_return / annual_volatility

print(f"Annual Return: {annual_return}")
print(f"Annual Volatility: {annual_volatility}")
print(f"Sharpe Ratio: {sharpe_ratio}")

# Compare with Buy and Hold
buy_and_hold_annual_return = eth_data['Buy_and_Hold'].mean() * 252
buy_and_hold_annual_volatility = eth_data['Buy_and_Hold'].std() * np.sqrt(252)
buy_and_hold_sharpe_ratio = buy_and_hold_annual_return / buy_and_hold_annual_volatility

print(f"Buy and Hold Annual Return: {buy_and_hold_annual_return}")
print(f"Buy and Hold Annual Volatility: {buy_and_hold_annual_volatility}")
print(f"Buy and Hold Sharpe Ratio: {buy_and_hold_sharpe_ratio}")
