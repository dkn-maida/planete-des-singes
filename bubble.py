import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Download historical 5-minute data for ETH-USD
eth_data_5m = yf.download('ETH-USD', period='60d', interval='5m')  # Adjust period as needed

# Calculate Bollinger Bands
period = 20  # Bollinger Band moving average period
std_dev_factor = 2  # Standard deviation factor
eth_data_5m['MA'] = eth_data_5m['Close'].rolling(window=period).mean()
eth_data_5m['Upper_BB'] = eth_data_5m['MA'] + (std_dev_factor * eth_data_5m['Close'].rolling(window=period).std())
eth_data_5m['Lower_BB'] = eth_data_5m['MA'] - (std_dev_factor * eth_data_5m['Close'].rolling(window=period).std())

# Define the strategy
cash = 10000
holdings = 0
eth_data_5m['Position'] = 0  # 1 when we hold ETH, 0 when we don't
eth_data_5m['Portfolio_Value'] = cash

for i in range(len(eth_data_5m)):
    close = eth_data_5m.loc[eth_data_5m.index[i], 'Close']
    lower_bb = eth_data_5m.loc[eth_data_5m.index[i], 'Lower_BB']
    ma = eth_data_5m.loc[eth_data_5m.index[i], 'MA']

    # Buy if the close is lower than the lower band and we have cash
    if close < lower_bb and cash > 0:
        holdings = cash / close
        cash = 0
        eth_data_5m.loc[eth_data_5m.index[i], 'Position'] = 1
    # Sell if the close is higher than the moving average and we have holdings
    elif close > ma and holdings > 0:
        cash = holdings * close
        holdings = 0
        eth_data_5m.loc[eth_data_5m.index[i], 'Position'] = 0
    
    # Update the portfolio value
    eth_data_5m.loc[eth_data_5m.index[i], 'Portfolio_Value'] = cash + (holdings * close)


# Calculate the buy and hold portfolio value for comparison
eth_data_5m['Buy_Hold_Value'] = 10000 * (eth_data_5m['Close'] / eth_data_5m['Close'].iloc[0])

# Calculate cumulative returns
eth_data_5m['Strategy_Cumulative_Return'] = eth_data_5m['Portfolio_Value'] / eth_data_5m['Portfolio_Value'].iloc[0]
eth_data_5m['Buy_Hold_Cumulative_Return'] = eth_data_5m['Buy_Hold_Value'] / eth_data_5m['Buy_Hold_Value'].iloc[0]

# Plot cumulative returns
plt.figure(figsize=(10, 6))
plt.plot(eth_data_5m.index, eth_data_5m['Strategy_Cumulative_Return'], label='Bollinger Band Strategy')
plt.plot(eth_data_5m.index, eth_data_5m['Buy_Hold_Cumulative_Return'], label='Buy and Hold Strategy')
plt.legend()
plt.title('Cumulative Returns')
plt.show()

# Calculate performance metrics
strategy_returns = eth_data_5m['Portfolio_Value'].pct_change().dropna()
buy_hold_returns = eth_data_5m['Buy_Hold_Value'].pct_change().dropna()

strategy_annual_return = strategy_returns.mean() * (60*24*365)
strategy_annual_volatility = strategy_returns.std() * np.sqrt(60*24*365)
strategy_sharpe_ratio = strategy_annual_return / strategy_annual_volatility

buy_hold_annual_return = buy_hold_returns.mean() * (60*24*365)
buy_hold_annual_volatility = buy_hold_returns.std() * np.sqrt(60*24*365)
buy_hold_sharpe_ratio = buy_hold_annual_return / buy_hold_annual_volatility

print(f"Strategy Annual Return: {strategy_annual_return}")
print(f"Strategy Annual Volatility: {strategy_annual_volatility}")
print(f"Strategy Sharpe Ratio: {strategy_sharpe_ratio}")
print(f"Buy and Hold Annual Return: {buy_hold_annual_return}")
print(f"Buy and Hold Annual Volatility: {buy_hold_annual_volatility}")
print(f"Buy and Hold Sharpe Ratio: {buy_hold_sharpe_ratio}")
