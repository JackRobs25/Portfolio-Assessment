# Portfolio-Assessment

This Python script is designed to assess and visualize the performance of an investment portfolio over a specified date range. The tool calculates key metrics such as cumulative return, average daily return, volatility (standard deviation of daily returns), and the Sharpe ratio, which measures risk-adjusted return. It also compares the portfolio’s performance to the SPY (an ETF that tracks the S&P 500 index) and generates a plot of the cumulative returns over time.

Key Features:

	•	Data Retrieval: The get_data function retrieves historical stock price data from CSV files located in the ./data directory. The function allows you to specify the date range, the stocks of interest (by their symbols), and the specific column to be used for analysis (e.g., ‘Adj Close’). The SPY data is always included by default for benchmarking purposes.
	•	Portfolio Assessment: The assess_portfolio function performs the core analysis. It:
	•	Normalizes stock prices to the first day’s value.
	•	Allocates portfolio funds according to specified allocations.
	•	Calculates the daily portfolio value.
	•	Computes key performance metrics, including the Sharpe ratio, average daily return, and cumulative return.
	•	Optionally generates a plot comparing the portfolio’s performance to the SPY.
	•	Visualization: The script plots the cumulative returns of both the portfolio and the SPY to visually compare performance over time.
