"""Long-only mean-variance portfolio optimization using SLSQP."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def optimize_minimum_variance(returns: pd.DataFrame, periods: int = 252,
                              max_weight: float = 1.0) -> dict:
    """Find long-only minimum-variance weights that sum to one."""
    clean = returns.dropna(how="any")
    if clean.empty:
        raise ValueError("Not enough complete return observations to optimize.")
    assets = list(clean.columns)
    n = len(assets)
    cov = clean.cov().to_numpy() * periods
    initial = np.repeat(1 / n, n)
    result = minimize(lambda w: float(w @ cov @ w), initial, method="SLSQP",
                      bounds=tuple((0.0, max_weight) for _ in range(n)),
                      constraints=({"type": "eq", "fun": lambda w: np.sum(w) - 1},))
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    return {"weights": pd.Series(result.x, index=assets),
            "annualized_volatility": float(np.sqrt(result.fun)),
            "success": bool(result.success), "message": str(result.message)}


def optimize_max_sharpe(returns: pd.DataFrame, risk_free_rate: float = 0.04,
                        periods: int = 252, max_weight: float = 1.0) -> dict:
    """Find long-only maximum-Sharpe weights from historical estimates."""
    clean = returns.dropna(how="any")
    if clean.empty:
        raise ValueError("Not enough complete return observations to optimize.")
    assets = list(clean.columns)
    n = len(assets)
    mu = clean.mean().to_numpy() * periods
    cov = clean.cov().to_numpy() * periods
    def objective(w):
        vol = np.sqrt(max(float(w @ cov @ w), 0.0))
        if np.isclose(vol, 0):
            return 1e6
        return -((float(w @ mu) - risk_free_rate) / vol)
    result = minimize(objective, np.repeat(1/n, n), method="SLSQP",
                      bounds=tuple((0.0, max_weight) for _ in range(n)),
                      constraints=({"type": "eq", "fun": lambda w: np.sum(w)-1},))
    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")
    return {"weights": pd.Series(result.x, index=assets),
            "annualized_return": float(result.x @ mu),
            "annualized_volatility": float(np.sqrt(result.x @ cov @ result.x)),
            "sharpe_ratio": float(-result.fun), "success": True}
