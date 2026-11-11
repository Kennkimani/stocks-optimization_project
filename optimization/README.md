# Quantitative Portfolio Optimization & Walk-Forward Backtesting

## Overview

This project explores quantitative portfolio construction using historical financial market data. It implements mean-variance portfolio optimization techniques to construct investment portfolios, evaluate risk-adjusted performance, and investigate how portfolio allocations change over time.

The project compares two optimization strategies:

- **Minimum Variance Optimization:** Constructs a portfolio that minimizes total portfolio variance.
- **Maximum Sharpe Ratio Optimization:** Constructs a portfolio that maximizes expected excess return per unit of risk.

It also implements a walk-forward backtesting framework to evaluate portfolio performance using historical training and testing windows while accounting for portfolio rebalancing and transaction costs.

The project was developed using Python, pandas, NumPy, SciPy and Matplotlib.

## Objectives

- Retrieve and process historical stock price data.
- Calculate asset returns and portfolio risk metrics.
- Implement minimum variance and maximum Sharpe ratio optimization.
- Compare optimized portfolios against an equal-weight benchmark.
- Evaluate portfolio performance through walk-forward backtesting.
- Account for portfolio turnover and transaction costs.
- Visualize portfolio performance, drawdowns and asset allocations.

## Asset Universe

The analysis uses five publicly traded companies:

| Ticker | Company |
|---|---|
| AAPL | Apple Inc. |
| MSFT | Microsoft Corporation |
| JPM | JPMorgan Chase & Co. |
| XOM | Exxon Mobil Corporation |
| KO | The Coca-Cola Company |

## Methodology

### 1. Data Preparation

Historical price observations are loaded into pandas DataFrames and organized by date and asset.

Daily simple returns are calculated as:

\[
R_t = \frac{P_t}{P_{t-1}} - 1
\]

Where:

- \(R_t\) represents the daily return.
- \(P_t\) represents the current adjusted price.
- \(P_{t-1}\) represents the previous adjusted price.

### 2. Portfolio Optimization

The project implements two long-only optimization strategies.

**Minimum Variance Portfolio**

The objective is to minimize portfolio variance:

\[
\min_w \quad w^T\Sigma w
\]

Subject to:

\[
\sum_{i=1}^{n}w_i=1
\]

\[
0\leq w_i\leq 1
\]

Where:

- \(w\) represents portfolio weights.
- \(\Sigma\) represents the covariance matrix of asset returns.

**Maximum Sharpe Ratio Portfolio**

The objective is to maximize the portfolio's Sharpe ratio:

\[
\max_w \quad
\frac{w^T\mu-r_f}{\sqrt{w^T\Sigma w}}
\]

Where:

- \(\mu\) represents annualized expected asset returns.
- \(r_f\) represents the annual risk-free rate.
- \(\Sigma\) represents annualized covariance.

Optimization is performed using SciPy's Sequential Least Squares Programming (SLSQP) algorithm.

### 3. Portfolio Performance Evaluation

The project evaluates portfolio performance using:

| Metric | Purpose |
|---|---|
| Annualized Return | Estimates annual return from average daily returns. |
| Annualized Volatility | Measures annualized portfolio risk. |
| Sharpe Ratio | Measures excess return relative to volatility. |
| Maximum Drawdown | Measures the largest peak-to-trough portfolio decline. |
| Cumulative Growth | Tracks compounded portfolio performance over time. |

The annualization convention uses 252 trading days.

### 4. Walk-Forward Backtesting

A walk-forward framework is implemented to evaluate the optimization strategies over sequential historical periods.

The backtesting configuration includes:

| Parameter | Setting |
|---|---:|
| Initial Capital | KSh 100,000 |
| Risk-Free Rate | 4% |
| Transaction Cost | 0.1% |
| Trading Days per Year | 252 |
| Training Window | 60 trading days |
| Testing Window | 10 trading days |
| Rebalancing Step | 10 trading days |
| Number of Test Windows | 4 |

For each testing window:

1. Historical training data is used to estimate expected returns and covariance.
2. Portfolio weights are optimized using the selected strategy.
3. The optimized portfolio is evaluated over the subsequent testing period.
4. Portfolio turnover is calculated during rebalancing.
5. Transaction costs are deducted from portfolio capital.
6. The process continues through subsequent testing windows.

Portfolio turnover is calculated as:

\[
Turnover = \frac{1}{2}\sum_{i=1}^{n}|w_{i,t}-w_{i,t-1}|
\]

The transaction cost model applies a fixed 0.1% cost to one-way traded notional.

## Visualizations

The project produces visualizations covering:

1. **Equity Curves:** Compares optimized portfolio growth against an equal-weight benchmark.
2. **Drawdown Analysis:** Examines portfolio losses relative to previous equity peaks.
3. **Asset Allocation:** Shows how optimized portfolio weights change across testing windows.
4. **Window Returns:** Compares net portfolio returns across individual testing periods.

## Project Structure

```text
optimization/
│
├── data/
│   └── stocks_data.csv
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── metrics.py
│   └── optimizer.py
│
├── notebooks/
│   └── portfolio_analysis.ipynb
│
├── outputs/
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Technologies Used

- Python
- pandas
- NumPy
- SciPy
- Matplotlib
- scikit-learn
- Jupyter Notebook
- uv

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd optimization
```

### 2. Install Python dependencies

This project uses uv for environment and dependency management.

```bash
uv sync
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Launch Jupyter Notebook

```bash
uv run jupyter notebook
```

Open the notebook located in the `notebooks/` directory.

### 5. Add the dataset

Place the historical price dataset in:

```text
data/stocks_data.csv
```

The dataset should contain a date column and price columns for the five assets.

## Limitations

This project is an educational quantitative finance research exercise and should not be interpreted as investment advice.

Important limitations include:

- Historical returns and covariance estimates may not accurately predict future market behaviour.
- Mean-variance optimization is sensitive to estimation errors.
- The walk-forward evaluation uses a relatively small number of testing windows.
- Transaction costs are simplified and do not fully capture bid-ask spreads, market impact, taxes or liquidity constraints.
- The short backtesting horizon limits conclusions about long-term strategy robustness.
- Annualized performance estimates from short testing periods should be interpreted cautiously.

## Future Improvements

Potential extensions include:

- Expanding the asset universe.
- Introducing covariance shrinkage techniques.
- Incorporating additional portfolio constraints.
- Testing alternative optimization approaches.
- Extending the historical testing period.
- Introducing more realistic transaction cost and slippage models.

## Disclaimer

This project is intended for educational and research purposes. Historical performance does not guarantee future results. Nothing in this repository constitutes financial or investment advice.
```

