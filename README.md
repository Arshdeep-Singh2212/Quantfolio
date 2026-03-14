# 📊 QuantFolio: Portfolio Optimization & ML-Enhanced Asset Allocation

> **Markowitz Mean-Variance Optimization + Machine Learning on Real NSE Data**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-orange.svg)](https://scikit-learn.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What This Project Does

Builds optimized stock portfolios using **10 real NSE large-cap stocks**, combining classical finance theory with modern machine learning:

1. **Downloads real stock data** from Yahoo Finance (RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, WIPRO, LT, BAJFINANCE, MARUTI)
2. **Analyzes risk-return profiles** — correlation structure, volatility clustering, sector relationships
3. **Computes the Efficient Frontier** — Markowitz mean-variance optimization with 50,000 Monte Carlo simulations
4. **Trains ML models** — Gradient Boosting predicts next-month returns per stock
5. **ML-Enhanced Allocation** — feeds predicted returns into the optimizer for forward-looking portfolios
6. **Backtests 4 strategies** — Equal Weight, Max Sharpe, Min Variance, ML-Enhanced vs NIFTY50 benchmark

---

## 🚀 Quick Start (Anaconda)

```bash
# 1. Open Anaconda Prompt, navigate to project folder
cd path\to\QuantFolio

# 2. Install one extra package
pip install yfinance

# 3. Launch Jupyter
jupyter notebook

# 4. Open QuantFolio_Analysis.ipynb and run cells with Shift+Enter
```

---

## 📁 Project Structure

```
QuantFolio/
├── QuantFolio_Analysis.ipynb    # Main notebook (100% self-contained)
├── app.py                       # Streamlit dashboard (coming soon)
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore
```

---

## 📊 Key Results

| Strategy | Ann. Return | Volatility | Sharpe Ratio | Max Drawdown |
|----------|-------------|------------|--------------|--------------|
| Max Sharpe (Markowitz) | Varies | Varies | Highest | Moderate |
| Min Variance | Lowest risk | Lowest | Good | Best |
| ML-Enhanced | ML-predicted | Moderate | Competitive | Moderate |
| Equal Weight | Average | Average | Baseline | Average |

*(Actual numbers depend on market data at time of running)*

---

## 🛠️ Tech Stack

- **Data**: Yahoo Finance via `yfinance` (real NSE market data)
- **Optimization**: SciPy `minimize` (SLSQP solver)
- **ML**: scikit-learn Gradient Boosting
- **Visualization**: Matplotlib, Seaborn
- **Theory**: Markowitz Mean-Variance (1952), Modern Portfolio Theory

---

## 📝 License

MIT License — free to use for your own portfolio.

---

*Built as a portfolio project for Quant/Finance roles.*
