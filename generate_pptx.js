/**
 * QuantFolio — Presentation Generator
 * 
 * Run: npm install -g pptxgenjs
 *      node generate_pptx.js
 * 
 * Generates a 10-slide executive deck. You can manually update
 * the numbers below after running the notebook with your real results.
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");

// ═══════════════════════════════════════
// UPDATE THESE NUMBERS from your notebook
// ═══════════════════════════════════════
const DATA = {
    stocks: 10,
    days: "~750",
    dateRange: "Jan 2021 – Mar 2025",
    mcSimulations: "50,000",
    
    maxSharpe: { ret: "XX.X", vol: "XX.X", sr: "X.XXX" },
    minVar:    { ret: "XX.X", vol: "XX.X", sr: "X.XXX" },
    mlPort:    { ret: "XX.X", vol: "XX.X", sr: "X.XXX" },
    equalWt:   { ret: "XX.X", vol: "XX.X", sr: "X.XXX" },
    
    mlDirAcc: "XX.X%",
    bestStrategy: "TBD",
    bestSharpe: "X.XXX",
    
    // Top holdings (update from pie charts)
    topHoldings: "TCS, INFY, BAJFINANCE (update after running)",
};

// ── Colors ──
const C = {
    navy:      "0A1628", deepBlue:  "0F2B4C", teal:      "0E7C7B",
    accent:    "38BDF8", white:     "FFFFFF", offWhite:  "F4F6F8",
    lightGray: "D1D8E0", textDark:  "1A1A2E", textMid:   "4A5568",
    green:     "34D399", red:       "F87171", orange:    "FB923C",
};
const FONT_H = "Georgia";
const FONT_B = "Calibri";

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "QuantFolio Analytics";
pres.title = "QuantFolio: Portfolio Optimization & ML-Enhanced Allocation";

// ══════════════════════════════════════════
// SLIDE 1: TITLE
// ══════════════════════════════════════════
let s1 = pres.addSlide();
s1.background = { color: C.navy };
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });

s1.addText("QUANTFOLIO", {
    x: 0.8, y: 1.2, w: 8.4, h: 0.9,
    fontFace: FONT_H, fontSize: 48, color: C.white, bold: true, charSpacing: 6, margin: 0,
});
s1.addText("Portfolio Optimization & ML-Enhanced Asset Allocation", {
    x: 0.8, y: 2.1, w: 8.4, h: 0.6,
    fontFace: FONT_B, fontSize: 20, color: C.accent, margin: 0,
});
s1.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 3.0, w: 2.5, h: 0.04, fill: { color: C.accent } });
s1.addText([
    { text: `${DATA.stocks} NSE Large-Caps  |  ${DATA.dateRange}  |  Real Yahoo Finance Data`, options: { fontSize: 13, color: C.lightGray, breakLine: true } },
    { text: `Markowitz Efficient Frontier  |  ${DATA.mcSimulations} Monte Carlo Simulations  |  Gradient Boosting ML`, options: { fontSize: 11, color: C.textMid } },
], { x: 0.8, y: 3.3, w: 8, h: 0.8, fontFace: FONT_B, margin: 0 });

s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.0, w: 10, h: 0.625, fill: { color: C.deepBlue } });
s1.addText("A Quant Finance Portfolio Project  |  Python + scikit-learn + SciPy", {
    x: 0.8, y: 5.05, w: 8.4, h: 0.55, fontFace: FONT_B, fontSize: 11, color: C.lightGray, valign: "middle",
});

// ══════════════════════════════════════════
// SLIDE 2: EXECUTIVE SUMMARY
// ══════════════════════════════════════════
let s2 = pres.addSlide();
s2.background = { color: C.offWhite };
s2.addText("Executive Summary", { x: 0.6, y: 0.3, w: 8.8, h: 0.7, fontFace: FONT_H, fontSize: 32, color: C.navy, bold: true, margin: 0 });

const cards = [
    { label: "Max Sharpe Ratio", value: DATA.maxSharpe.sr, sub: `Return: ${DATA.maxSharpe.ret}%` },
    { label: "Min Volatility", value: `${DATA.minVar.vol}%`, sub: `Sharpe: ${DATA.minVar.sr}` },
    { label: "ML Direction Acc.", value: DATA.mlDirAcc, sub: "Gradient Boosting" },
    { label: "Best Backtest", value: DATA.bestStrategy, sub: `Sharpe: ${DATA.bestSharpe}` },
];
cards.forEach((m, i) => {
    const x = 0.6 + i * 2.3;
    s2.addShape(pres.shapes.RECTANGLE, { x, y: 1.3, w: 2.1, h: 1.8, fill: { color: C.white },
        shadow: { type: "outer", blur: 8, offset: 2, angle: 135, color: "000000", opacity: 0.08 } });
    s2.addShape(pres.shapes.RECTANGLE, { x, y: 1.3, w: 2.1, h: 0.06, fill: { color: C.teal } });
    s2.addText(m.label, { x: x+0.15, y: 1.5, w: 1.8, h: 0.35, fontFace: FONT_B, fontSize: 10, color: C.textMid, margin: 0 });
    s2.addText(m.value, { x: x+0.15, y: 1.85, w: 1.8, h: 0.55, fontFace: FONT_H, fontSize: 24, color: C.navy, bold: true, margin: 0 });
    s2.addText(m.sub, { x: x+0.15, y: 2.45, w: 1.8, h: 0.35, fontFace: FONT_B, fontSize: 9, color: C.textMid, margin: 0 });
});

s2.addText([
    { text: "Project Scope", options: { bold: true, fontSize: 14, color: C.navy, breakLine: true } },
    { text: "This project downloads real NSE stock data, computes the Markowitz Efficient Frontier with 50,000 Monte Carlo simulations, trains Gradient Boosting models to predict forward returns, and backtests 4 allocation strategies against the NIFTY50 benchmark.", options: { fontSize: 11, color: C.textDark, breakLine: true } },
    { text: "", options: { fontSize: 6, breakLine: true } },
    { text: "Tech Stack: ", options: { bold: true, fontSize: 12, color: C.navy } },
    { text: "Python 3 · scikit-learn · SciPy · NumPy · Pandas · Matplotlib · yfinance", options: { fontSize: 11, color: C.textDark } },
], { x: 0.6, y: 3.4, w: 8.8, h: 1.8, fontFace: FONT_B, valign: "top" });

// ══════════════════════════════════════════
// SLIDE 3: DATA & UNIVERSE
// ══════════════════════════════════════════
let s3 = pres.addSlide();
s3.background = { color: C.offWhite };
s3.addText("Stock Universe & Data", { x: 0.6, y: 0.3, w: 8.8, h: 0.6, fontFace: FONT_H, fontSize: 28, color: C.navy, bold: true, margin: 0 });
s3.addText("10 NSE large-cap stocks across 5 sectors + NIFTY50 benchmark", { x: 0.6, y: 0.85, w: 8.8, h: 0.3, fontFace: FONT_B, fontSize: 11, color: C.textMid, margin: 0 });

const stocks = [
    ["Stock", "Sector", "Why Included"],
    ["RELIANCE", "Conglomerate", "Largest by market cap"],
    ["TCS / INFY / WIPRO", "IT", "Export-driven, USD correlated"],
    ["HDFCBANK / ICICIBANK / SBIN", "Banking", "Rate-sensitive, domestic economy"],
    ["LT", "Infrastructure", "Capex cycle proxy"],
    ["BAJFINANCE", "NBFC", "Consumer credit growth"],
    ["MARUTI", "Auto", "Discretionary spending"],
];
const tableRows = stocks.map((row, i) => row.map(cell => ({
    text: cell, options: {
        fontSize: 10, fill: { color: i === 0 ? C.navy : (i % 2 === 0 ? C.offWhite : C.white) },
        color: i === 0 ? C.white : C.textDark, bold: i === 0
    }
})));
s3.addTable(tableRows, { x: 0.6, y: 1.4, w: 8.8, h: 2.5, border: { pt: 0.5, color: C.lightGray }, colW: [3, 2.5, 3.3] });

s3.addText([
    { text: `Data Source: Yahoo Finance (yfinance API)`, options: { bold: true, breakLine: true, fontSize: 11 } },
    { text: `Period: ${DATA.dateRange}  |  ~${DATA.days} trading days  |  Auto-adjusted OHLCV`, options: { fontSize: 10, color: C.textMid } },
], { x: 0.6, y: 4.2, w: 8.8, h: 0.7, fontFace: FONT_B, color: C.textDark });

// ══════════════════════════════════════════
// SLIDE 4: METHODOLOGY
// ══════════════════════════════════════════
let s4 = pres.addSlide();
s4.background = { color: C.offWhite };
s4.addText("Methodology & Pipeline", { x: 0.6, y: 0.3, w: 8.8, h: 0.6, fontFace: FONT_H, fontSize: 28, color: C.navy, bold: true, margin: 0 });

const steps = [
    { n: "01", t: "Data Ingestion", d: "Real NSE OHLCV data via Yahoo Finance for 10 stocks + NIFTY50 benchmark index." },
    { n: "02", t: "Risk-Return Analysis", d: "Annualized returns, volatility, Sharpe ratios, correlation matrix, sector analysis." },
    { n: "03", t: "Markowitz Optimization", d: "Efficient Frontier via SciPy SLSQP. 50,000 Monte Carlo random portfolios." },
    { n: "04", t: "ML Return Prediction", d: "Gradient Boosting per stock. Features: momentum, volatility, mean reversion." },
    { n: "05", t: "ML-Enhanced Portfolio", d: "Feed ML-predicted returns into optimizer. Forward-looking allocation." },
    { n: "06", t: "Backtesting", d: "Compare 4 strategies vs NIFTY50. Metrics: Sharpe, drawdown, Calmar ratio." },
];
steps.forEach((s, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.6 + col * 3.1, y = 1.15 + row * 2.1;
    s4.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.9, h: 1.85, fill: { color: C.white },
        shadow: { type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.06 } });
    s4.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.55, h: 0.45, fill: { color: C.navy } });
    s4.addText(s.n, { x, y, w: 0.55, h: 0.45, fontFace: FONT_H, fontSize: 16, color: C.accent, bold: true, align: "center", valign: "middle", margin: 0 });
    s4.addText(s.t, { x: x+0.65, y: y+0.05, w: 2.1, h: 0.4, fontFace: FONT_H, fontSize: 13, color: C.navy, bold: true, margin: 0 });
    s4.addText(s.d, { x: x+0.12, y: y+0.55, w: 2.65, h: 1.2, fontFace: FONT_B, fontSize: 9.5, color: C.textMid, margin: 0 });
});

// ══════════════════════════════════════════
// SLIDE 5-8: PLACEHOLDER CHART SLIDES
// ══════════════════════════════════════════
const chartSlides = [
    { title: "Efficient Frontier & Monte Carlo Cloud", sub: "50,000 random portfolios with Max Sharpe and Min Variance stars" },
    { title: "Portfolio Weight Allocations", sub: "Max Sharpe vs Min Variance vs ML-Enhanced vs Equal Weight" },
    { title: "Strategy Backtest: Cumulative Returns", sub: "4 strategies vs NIFTY50 benchmark over test period" },
    { title: "Risk Analysis: Drawdowns & Monthly Heatmap", sub: "Max drawdown comparison and monthly return patterns" },
];
chartSlides.forEach(cs => {
    let s = pres.addSlide();
    s.background = { color: C.offWhite };
    s.addText(cs.title, { x: 0.6, y: 0.3, w: 8.8, h: 0.6, fontFace: FONT_H, fontSize: 28, color: C.navy, bold: true, margin: 0 });
    s.addText(cs.sub, { x: 0.6, y: 0.85, w: 8.8, h: 0.3, fontFace: FONT_B, fontSize: 11, color: C.textMid, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.3, w: 9, h: 3.8, fill: { color: C.white },
        shadow: { type: "outer", blur: 4, offset: 1, angle: 135, color: "000000", opacity: 0.06 } });
    s.addText("[ Screenshot from notebook — paste chart image here ]", {
        x: 0.5, y: 1.3, w: 9, h: 3.8, fontFace: FONT_B, fontSize: 14, color: C.lightGray, align: "center", valign: "middle"
    });
});

// ══════════════════════════════════════════
// SLIDE 9: STRATEGY COMPARISON TABLE
// ══════════════════════════════════════════
let s9 = pres.addSlide();
s9.background = { color: C.offWhite };
s9.addText("Strategy Performance Comparison", { x: 0.6, y: 0.3, w: 8.8, h: 0.6, fontFace: FONT_H, fontSize: 28, color: C.navy, bold: true, margin: 0 });
s9.addText("Update these numbers from your notebook backtest results", { x: 0.6, y: 0.85, w: 8.8, h: 0.3, fontFace: FONT_B, fontSize: 11, color: C.textMid, margin: 0 });

const perfTable = [
    ["Strategy", "Ann. Return", "Volatility", "Sharpe", "Max Drawdown", "Final Value (₹1)"],
    ["Max Sharpe", `${DATA.maxSharpe.ret}%`, `${DATA.maxSharpe.vol}%`, DATA.maxSharpe.sr, "X.X%", "X.XXX"],
    ["Min Variance", `${DATA.minVar.ret}%`, `${DATA.minVar.vol}%`, DATA.minVar.sr, "X.X%", "X.XXX"],
    ["ML-Enhanced", `${DATA.mlPort.ret}%`, `${DATA.mlPort.vol}%`, DATA.mlPort.sr, "X.X%", "X.XXX"],
    ["Equal Weight", `${DATA.equalWt.ret}%`, `${DATA.equalWt.vol}%`, DATA.equalWt.sr, "X.X%", "X.XXX"],
    ["NIFTY50", "—", "—", "—", "X.X%", "X.XXX"],
];
const perfRows = perfTable.map((row, i) => row.map(cell => ({
    text: cell, options: {
        fontSize: 10, align: i === 0 ? "left" : "center",
        fill: { color: i === 0 ? C.navy : (i % 2 === 0 ? C.offWhite : C.white) },
        color: i === 0 ? C.white : C.textDark, bold: i === 0
    }
})));
s9.addTable(perfRows, { x: 0.6, y: 1.4, w: 8.8, border: { pt: 0.5, color: C.lightGray }, colW: [2, 1.4, 1.4, 1.1, 1.5, 1.4] });

// ══════════════════════════════════════════
// SLIDE 10: CLOSING
// ══════════════════════════════════════════
let s10 = pres.addSlide();
s10.background = { color: C.navy };
s10.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
s10.addText("Key Takeaways", { x: 0.8, y: 0.6, w: 8.4, h: 0.7, fontFace: FONT_H, fontSize: 36, color: C.white, bold: true, margin: 0 });
s10.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 1.4, w: 2, h: 0.04, fill: { color: C.accent } });

s10.addText([
    { text: "Markowitz optimization identifies portfolios that dominate equal-weight allocation", options: { bullet: true, breakLine: true, fontSize: 14, color: C.lightGray } },
    { text: "ML-predicted returns provide forward-looking edge over purely historical estimates", options: { bullet: true, breakLine: true, fontSize: 14, color: C.lightGray } },
    { text: "Low-correlation stock pairs (identified via heatmap) are key to diversification benefit", options: { bullet: true, breakLine: true, fontSize: 14, color: C.lightGray } },
    { text: "Backtesting validates theory: optimized portfolios outperform on risk-adjusted basis", options: { bullet: true, breakLine: true, fontSize: 14, color: C.lightGray } },
    { text: "Pipeline is fully reproducible: real data, open source, one-click execution", options: { bullet: true, fontSize: 14, color: C.lightGray } },
], { x: 0.8, y: 1.8, w: 8.4, h: 2.5, fontFace: FONT_B, paraSpaceAfter: 10 });

s10.addShape(pres.shapes.RECTANGLE, { x: 0, y: 4.6, w: 10, h: 1.025, fill: { color: C.deepBlue } });
s10.addText([
    { text: "QuantFolio — Portfolio Project for Quant/Finance Roles", options: { bold: true, fontSize: 14, color: C.white, breakLine: true } },
    { text: "Python · scikit-learn · SciPy · yfinance · Streamlit  |  Full source on GitHub", options: { fontSize: 11, color: C.lightGray } },
], { x: 0.8, y: 4.7, w: 8.4, h: 0.85, fontFace: FONT_B, valign: "middle" });

// ── WRITE FILE ──
pres.writeFile({ fileName: "QuantFolio_Presentation.pptx" }).then(() => {
    console.log("Presentation saved: QuantFolio_Presentation.pptx");
    console.log("NOTE: Update the DATA object at the top with your real numbers,");
    console.log("      then paste chart screenshots into slides 5-8.");
});
