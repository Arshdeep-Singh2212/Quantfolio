"""
QuantFolio — Interactive Streamlit Dashboard
=============================================
Self-contained: downloads data, computes everything, displays results.
Run with: streamlit run app.py
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy.optimize import minimize
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ──
st.set_page_config(page_title="QuantFolio | Portfolio Optimizer", page_icon="📊", layout="wide")

# ── Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');
    .stApp { background: linear-gradient(180deg, #0a0e17 0%, #0d1321 100%); }
    section[data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1a2332; }
    h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; color: #e8edf3 !important; }
    [data-testid="stMetric"] { background: linear-gradient(135deg, #111827 0%, #1a2332 100%);
        border: 1px solid #1e2d3d; border-radius: 12px; padding: 16px 20px; }
    [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; color: #38bdf8 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; text-transform: uppercase; font-size: 0.7rem !important; letter-spacing: 0.08em; }
    .stTabs [data-baseweb="tab-list"] { background: #111827; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #64748b; border-radius: 8px; }
    .stTabs [aria-selected="true"] { background: #1e293b !important; color: #38bdf8 !important; }
    .stMarkdown p, .stMarkdown li { color: #94a3b8; font-family: 'DM Sans', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Dark chart style ──
DARK = {"figure.facecolor": "#0a0e17", "axes.facecolor": "#111827", "axes.edgecolor": "#1e2d3d",
        "axes.labelcolor": "#94a3b8", "text.color": "#e8edf3", "xtick.color": "#64748b",
        "ytick.color": "#64748b", "grid.color": "#1e2d3d", "grid.alpha": 0.5}
CLR = {"cyan": "#38bdf8", "green": "#34d399", "red": "#f87171", "orange": "#fb923c",
       "purple": "#a78bfa", "yellow": "#fbbf24"}
COLORS = ['#38bdf8', '#f87171', '#34d399', '#a78bfa', '#fb923c', '#fbbf24', '#818cf8', '#22d3ee', '#f472b6', '#4ade80']

# ══════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════
TICKERS = {'RELIANCE':'RELIANCE.NS','TCS':'TCS.NS','INFY':'INFY.NS','HDFCBANK':'HDFCBANK.NS',
           'ICICIBANK':'ICICIBANK.NS','SBIN':'SBIN.NS','WIPRO':'WIPRO.NS','LT':'LT.NS',
           'BAJFINANCE':'BAJFINANCE.NS','MARUTI':'MARUTI.NS'}

@st.cache_data(show_spinner=False, ttl=3600)
def load_data(start, end):
    import yfinance as yf
    prices = pd.DataFrame()
    for name, ticker in TICKERS.items():
        try:
            data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            prices[name] = data['Close']
        except: pass
    try:
        nifty = yf.download('^NSEI', start=start, end=end, progress=False, auto_adjust=True)
        if isinstance(nifty.columns, pd.MultiIndex):
            nifty.columns = nifty.columns.get_level_values(0)
        prices['NIFTY50'] = nifty['Close']
    except: pass
    prices.dropna(inplace=True)
    return prices

@st.cache_data(show_spinner=False)
def run_optimization(_prices, stock_names, rf_rate):
    returns = _prices[stock_names].pct_change().dropna()
    mean_ret = returns.mean() * 252
    cov = returns.cov() * 252
    n = len(stock_names)

    def perf(w):
        r = np.dot(w, mean_ret); v = np.sqrt(w.T @ cov @ w); return r, v, (r-rf_rate)/v
    def neg_sr(w): return -perf(w)[2]
    def vol(w): return perf(w)[1]
    def ret(w): return perf(w)[0]

    cons = {'type':'eq','fun':lambda w: np.sum(w)-1}
    bnds = tuple((0,1) for _ in range(n))
    w0 = np.array([1/n]*n)

    r_ms = minimize(neg_sr, w0, method='SLSQP', bounds=bnds, constraints=cons)
    r_mv = minimize(vol, w0, method='SLSQP', bounds=bnds, constraints=cons)

    # Monte Carlo
    np.random.seed(42)
    mc_n = 30000
    mc_w = np.array([np.random.dirichlet(np.ones(n)) for _ in range(mc_n)])
    mc_r = np.array([perf(w)[0] for w in mc_w])
    mc_v = np.array([perf(w)[1] for w in mc_w])
    mc_s = np.array([perf(w)[2] for w in mc_w])

    # Efficient frontier
    targets = np.linspace(mean_ret.min(), mean_ret.max(), 60)
    ef_v = []
    for t in targets:
        c2 = [{'type':'eq','fun':lambda w:np.sum(w)-1},{'type':'eq','fun':lambda w,t=t:ret(w)-t}]
        r = minimize(vol, w0, method='SLSQP', bounds=bnds, constraints=c2)
        ef_v.append(vol(r.x) if r.success else np.nan)

    return {
        'returns': returns, 'mean_ret': mean_ret, 'cov': cov,
        'ms_w': r_ms.x, 'ms_perf': perf(r_ms.x),
        'mv_w': r_mv.x, 'mv_perf': perf(r_mv.x),
        'eq_w': w0, 'eq_perf': perf(w0),
        'mc_r': mc_r, 'mc_v': mc_v, 'mc_s': mc_s,
        'ef_targets': targets, 'ef_v': np.array(ef_v),
        'ann_ret': mean_ret, 'ann_vol': returns.std()*np.sqrt(252),
    }

@st.cache_data(show_spinner=False)
def run_ml(_prices, stock_names, rf_rate):
    returns = _prices[stock_names].pct_change().dropna()
    monthly = _prices[stock_names].resample('ME').last().pct_change().dropna()
    cov = returns.cov() * 252
    n = len(stock_names)

    def perf(w, mr):
        r = np.dot(w, mr); v = np.sqrt(w.T @ cov @ w); return r, v, (r-rf_rate)/v if v > 0 else 0

    preds = {}
    for stock in stock_names:
        try:
            df = pd.DataFrame({'Return': monthly[stock]})
            df['Mom1'] = df['Return'].shift(1)
            df['Mom3'] = df['Return'].rolling(3).mean().shift(1)
            df['Mom6'] = df['Return'].rolling(6).mean().shift(1)
            df['Vol3'] = df['Return'].rolling(3).std().shift(1)
            df['Vol6'] = df['Return'].rolling(6).std().shift(1)
            df['Dev'] = df['Return'].shift(1) - df['Return'].rolling(12).mean().shift(1)
            df.dropna(inplace=True)

            if len(df) < 15:  # Need minimum data for meaningful train/test
                preds[stock] = {'dir_acc': 0.5, 'last_pred': monthly[stock].mean()}
                continue

            fc = ['Mom1','Mom3','Mom6','Vol3','Vol6','Dev']
            X, y = df[fc].values, df['Return'].values
            split = max(int(len(X)*0.7), 5)  # At least 5 training samples
            if split >= len(X) - 1:
                split = len(X) - 2

            sc = RobustScaler()
            Xtr = sc.fit_transform(X[:split])
            Xte = sc.transform(X[split:])
            m = GradientBoostingRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
            m.fit(Xtr, y[:split])
            yp = m.predict(Xte)
            preds[stock] = {'dir_acc': np.mean(np.sign(y[split:])==np.sign(yp)), 'last_pred': yp[-1]}
        except Exception:
            preds[stock] = {'dir_acc': 0.5, 'last_pred': monthly[stock].mean() if stock in monthly.columns else 0}

    ml_er = np.array([preds[s]['last_pred']*12 for s in stock_names])
    def neg_sr_ml(w): r=np.dot(w,ml_er); v=np.sqrt(w.T@cov@w); return -(r-rf_rate)/v if v > 0 else 0
    cons = {'type':'eq','fun':lambda w:np.sum(w)-1}
    bnds = tuple((0,1) for _ in range(n))
    r = minimize(neg_sr_ml, np.array([1/n]*n), method='SLSQP', bounds=bnds, constraints=cons)

    return {'ml_w': r.x, 'ml_perf': perf(r.x, ml_er), 'preds': preds,
            'avg_dir_acc': np.mean([p['dir_acc'] for p in preds.values()])}

# ══════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 QuantFolio")
    st.markdown("---")
    start_date = st.date_input("Start Date", pd.Timestamp("2021-01-01"))
    end_date = st.date_input("End Date", pd.Timestamp("2025-03-14"))
    rf_rate = st.slider("Risk-Free Rate (%)", 3.0, 10.0, 6.5, 0.5) / 100
    st.markdown("---")
    st.markdown("**Stack**: Python · scikit-learn · SciPy · Matplotlib")
    st.caption("Portfolio project for Quant/Finance roles")

# ══════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════
st.markdown("# 📊 QuantFolio — Portfolio Optimization Engine")
st.markdown("##### Markowitz Mean-Variance + ML-Enhanced Allocation on Real NSE Data")
st.markdown("---")

with st.spinner("⏳ Downloading NSE data from Yahoo Finance..."):
    prices = load_data(str(start_date), str(end_date))

stock_names = [c for c in prices.columns if c != 'NIFTY50']

with st.spinner("⚡ Running portfolio optimization (30,000 simulations)..."):
    opt = run_optimization(prices, stock_names, rf_rate)

with st.spinner("🧠 Training ML models..."):
    ml = run_ml(prices, stock_names, rf_rate)

# ── Top Metrics ──
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Max Sharpe", f"{opt['ms_perf'][2]:.3f}", "Sharpe Ratio")
c2.metric("Max Sharpe Return", f"{opt['ms_perf'][0]*100:.1f}%")
c3.metric("Min Vol", f"{opt['mv_perf'][1]*100:.1f}%", "Volatility")
c4.metric("ML Direction Acc", f"{ml['avg_dir_acc']:.1%}")
c5.metric("Stocks", f"{len(stock_names)}")

# ── Tabs ──
tab1, tab2, tab3, tab4 = st.tabs(["📈 Efficient Frontier", "⚖️ Allocations", "🤖 ML Models", "📊 Backtest"])

with tab1:
    with plt.rc_context(DARK):
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor("#0a0e17"); ax.set_facecolor("#111827")
        sc = ax.scatter(opt['mc_v']*100, opt['mc_r']*100, c=opt['mc_s'], cmap='viridis', alpha=0.3, s=5)
        plt.colorbar(sc, ax=ax, label='Sharpe Ratio', shrink=0.8)
        v = ~np.isnan(opt['ef_v'])
        ax.plot(opt['ef_v'][v]*100, opt['ef_targets'][v]*100, color=CLR['red'], lw=3, label='Efficient Frontier')
        ax.scatter(opt['ms_perf'][1]*100, opt['ms_perf'][0]*100, color=CLR['red'], s=300, marker='*', zorder=15, edgecolors='white', lw=1.5, label=f'Max Sharpe ({opt["ms_perf"][2]:.3f})')
        ax.scatter(opt['mv_perf'][1]*100, opt['mv_perf'][0]*100, color=CLR['cyan'], s=300, marker='*', zorder=15, edgecolors='white', lw=1.5, label=f'Min Variance')
        for i, s in enumerate(stock_names):
            ax.scatter(opt['ann_vol'][s]*100, opt['ann_ret'][s]*100, s=80, color=COLORS[i], zorder=12, edgecolors='white')
            ax.annotate(s, (opt['ann_vol'][s]*100, opt['ann_ret'][s]*100), textcoords="offset points", xytext=(7,3), fontsize=8, color='#94a3b8')
        ax.set_xlabel('Volatility (%)'); ax.set_ylabel('Return (%)')
        ax.set_title('Efficient Frontier (30,000 Portfolios)', fontsize=16, fontweight='bold', color='#e8edf3')
        ax.legend(fontsize=9, facecolor='#111827', edgecolor='#1e2d3d', labelcolor='#94a3b8')
    st.pyplot(fig); plt.close(fig)

with tab2:
    st.markdown("### Portfolio Weight Allocations")
    allocs = pd.DataFrame({
        'Max Sharpe': opt['ms_w'], 'Min Variance': opt['mv_w'],
        'ML-Enhanced': ml['ml_w'], 'Equal Weight': opt['eq_w']
    }, index=stock_names).round(4) * 100
    st.dataframe(allocs.style.format("{:.1f}%").background_gradient(cmap='Blues', axis=0), use_container_width=True)

    with plt.rc_context(DARK):
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.patch.set_facecolor("#0a0e17")
        for ax, (name, w) in zip(axes, [('Max Sharpe', opt['ms_w']), ('Min Variance', opt['mv_w']), ('ML-Enhanced', ml['ml_w'])]):
            ax.set_facecolor("#111827")
            mask = w > 0.01
            ax.pie(w[mask]*100, labels=np.array(stock_names)[mask], autopct='%1.0f%%',
                   colors=COLORS[:sum(mask)], textprops={'fontsize':8, 'color':'#e8edf3'})
            ax.set_title(name, fontweight='bold', color='#e8edf3')
    st.pyplot(fig); plt.close(fig)

with tab3:
    st.markdown("### ML Model Performance (Gradient Boosting per Stock)")
    ml_df = pd.DataFrame({s: {'Direction Accuracy': f"{ml['preds'][s]['dir_acc']:.1%}",
                               'Predicted Monthly Return': f"{ml['preds'][s]['last_pred']*100:.2f}%"}
                          for s in stock_names}).T
    st.dataframe(ml_df, use_container_width=True)
    r, v, sr = ml['ml_perf']
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("ML Portfolio Return", f"{r*100:.1f}%")
    mc2.metric("ML Portfolio Vol", f"{v*100:.1f}%")
    mc3.metric("ML Sharpe", f"{sr:.3f}")

with tab4:
    st.markdown("### Strategy Backtest")
    returns = opt['returns']
    split_idx = int(len(returns) * 0.7)
    test_ret = returns.iloc[split_idx:]
    strats = {'Equal Weight': opt['eq_w'], 'Max Sharpe': opt['ms_w'],
              'Min Variance': opt['mv_w'], 'ML-Enhanced': ml['ml_w']}
    strat_ret = pd.DataFrame({n: test_ret.dot(w) for n, w in strats.items()})
    if 'NIFTY50' in prices.columns:
        nifty_r = prices['NIFTY50'].pct_change().dropna()
        strat_ret['NIFTY50'] = nifty_r.reindex(strat_ret.index)
    cum = (1 + strat_ret).cumprod()

    with plt.rc_context(DARK):
        fig, ax = plt.subplots(figsize=(14, 7))
        fig.patch.set_facecolor("#0a0e17"); ax.set_facecolor("#111827")
        style = {'Equal Weight': (CLR['orange'],2,'-'), 'Max Sharpe': (CLR['red'],2.5,'-'),
                 'Min Variance': (CLR['cyan'],2,'-'), 'ML-Enhanced': (CLR['green'],2.5,'-'),
                 'NIFTY50': ('#ffffff',2,'--')}
        for col in cum.columns:
            c, w, ls = style.get(col, ('#888',1,'-'))
            ax.plot(cum.index, cum[col], label=col, color=c, lw=w, ls=ls)
        ax.axhline(y=1, color='#333', ls=':', lw=0.5)
        ax.set_title('Strategy Backtest: Cumulative Returns', fontsize=16, fontweight='bold', color='#e8edf3')
        ax.set_ylabel('Growth of ₹1', color='#94a3b8')
        ax.legend(fontsize=10, facecolor='#111827', edgecolor='#1e2d3d', labelcolor='#94a3b8')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    st.pyplot(fig); plt.close(fig)

    # Performance table
    def calc_metrics(r):
        ar = r.mean()*252; av = r.std()*np.sqrt(252); sr = (ar-rf_rate)/av
        c = (1+r).cumprod(); dd = (c/c.cummax()-1).min()
        return {'Return%': round(ar*100,1), 'Vol%': round(av*100,1), 'Sharpe': round(sr,3),
                'MaxDD%': round(dd*100,1), 'Final₹': round(c.iloc[-1],3)}
    perf_df = pd.DataFrame({n: calc_metrics(strat_ret[n]) for n in strat_ret.columns}).T
    perf_df = perf_df.sort_values('Sharpe', ascending=False)
    st.dataframe(perf_df, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#4a5568;font-size:0.8rem'>QuantFolio v1.0 — Portfolio Project for Quant/Finance Roles</div>", unsafe_allow_html=True)
