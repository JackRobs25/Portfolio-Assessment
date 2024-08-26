import pandas as pd
import matplotlib.pyplot as plt
import math

def get_data(start, end, symbols, column_name="Adj Close", include_spy=True, data_folder="./data"):
    dates = pd.date_range(start, end)
    df1 = pd.DataFrame(index=dates)
    df2 = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True, usecols=['Date', column_name])
    df2.rename(columns={column_name: "SPY"}, inplace=True)
    df1 = df1.join(df2, how='inner')
    for symbol in symbols:
        tmp_df = pd.read_csv(data_folder + '/'+ symbol + ".csv", index_col='Date', parse_dates=True, usecols=['Date', column_name])
        tmp_df.rename(columns={column_name: symbol}, inplace=True)
        df1 = df1.join(tmp_df, how='left', rsuffix='_'+symbol)
    if (not include_spy):
        df1.drop('SPY', axis=1, inplace=True)
    return df1

def assess_portfolio (start_date, end_date, symbols, allocations,
                      starting_value=1000000, risk_free_rate=0.0,
                      sample_freq=252, plot_returns=True):
    daily_prices_df = get_data(start_date, end_date, symbols)
    # Normalize stock prices to the first day
    normalized_prices = daily_prices_df / daily_prices_df.iloc[0]
    # Multiply each column by the allocation to that stock
    allocated_prices = normalized_prices.iloc[:, 1:] * allocations
    # Multiply normalized allocations by starting portfolio dollar value
    portfolio_values = allocated_prices * starting_value
    # Sum each date (across the stocks) to get daily portfolio dollar value
    daily_portfolio_value = portfolio_values.sum(axis=1)
    cumulative_return = (daily_portfolio_value.iloc[-1] / daily_portfolio_value.iloc[0]) - 1
    # pct_change() --> Fractional change between the current and a prior element
    daily_returns = daily_portfolio_value.pct_change().dropna()
    average_daily_return = daily_returns.mean()
    stdev_daily_return = daily_returns.std()
    # Calculate Sharpe Ratio
    excess_daily_returns = daily_returns - risk_free_rate
    sharpe_ratio = (excess_daily_returns.mean() / excess_daily_returns.std()) * math.sqrt(sample_freq)
    end_value = daily_portfolio_value.iloc[-1]
    print("Start Date: ", start_date)
    print("End Date: ", end_date)
    print("Symbols: ", symbols)
    print("Allocations: ", allocations)
    print("Sharpe Ratio: ", sharpe_ratio)
    print("Volatility (stdev of daily returns): ", stdev_daily_return)
    print("Average Daily Returns: ", average_daily_return)
    print("Cumulative Return: ", cumulative_return)
    print("Ending Value: ", end_value)

    if plot_returns:
        spy_data = get_data(start_date, end_date, [], include_spy=True)

        plt.figure(figsize=(10, 6))
        plt.plot(spy_data.index, (spy_data['SPY'] / spy_data['SPY'].iloc[0]) - 1, label='SPY')
        plt.plot(daily_portfolio_value.index, (daily_portfolio_value / starting_value) - 1, label='Portfolio')
        plt.legend()
        plt.title('Daily portfolio value and SPY')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.grid(True)
        plt.show()


    return cumulative_return, average_daily_return, stdev_daily_return, sharpe_ratio, end_value 



def main():
    # print(get_data('2016-12-25','2017-01-10',['AAPL','JPM','TSLA']))
    assess_portfolio('2010-01-01', '2010-12-31', ['GOOG', 'AAPL', 'GLD', 'XOM'], [0.2, 0.3, 0.4, 0.1])
    # assess_portfolio('2015-06-30', '2015-12-31', ['MSFT', 'HPQ', 'IBM', 'AMZN'], [0.1, 0.1, 0.4, 0.4])
    # assess_portfolio('2020-01-01', '2020-06-30', ['NFLX', 'AMZN', 'XOM', 'PTON'], [0.0, 0.35, 0.35, 0.3])
    # assess_portfolio('2014-05-01', '2014-05-31', ['IBM'], [1.0])
    # assess_portfolio('2014-01-01', '2014-12-31', ['SPY'], [1.0])
    # assess_portfolio('2014-01-01', '2014-12-31', ['F'], [1.0])


if __name__ == "__main__":
    main()
