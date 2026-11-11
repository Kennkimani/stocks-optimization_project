"""Reusable portfolio performance and risk metrics."""
import numpy as np
import pandas as pd


def annualized_return(daily_returns: pd.Series, periods: int = 252) -> float:
    return float(daily_returns.mean() * periods)


def annualized_volatility(daily_returns: pd.Series, periods: int = 252) -> float:
    return float(daily_returns.std() * np.sqrt(periods))


def sharpe_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.04,
                 periods: int = 252) -> float:
    vol = annualized_volatility(daily_returns, periods)
    if np.isclose(vol, 0):
        return float("nan")
    return (annualized_return(daily_returns, periods) - risk_free_rate) / vol


def max_drawdown(daily_returns: pd.Series) -> float:
    wealth = (1 + daily_returns.fillna(0)).cumprod()
    drawdown = wealth / wealth.cummax() - 1
    return float(drawdown.min())


def cumulative_growth(daily_returns: pd.Series) -> pd.Series:
    return (1 + daily_returns.fillna(0)).cumprod()
