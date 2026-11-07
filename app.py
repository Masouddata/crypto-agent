import os
import time
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Crypto Intelligence Scanner Pro",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root {
  --bg: #f7f9fc;
  --panel: #ffffff;
  --panel-soft: #f2f6fc;
  --border: #dce5f0;
  --text: #172b4d;
  --muted: #62748b;
  --blue: #2878ee;
  --teal: #13a98f;
}
.stApp {
  background: linear-gradient(180deg, #ffffff 0%, #f5f8fd 100%);
  color: var(--text);
}
[data-testid="stHeader"] { background: rgba(255,255,255,.96); }
[data-testid="stSidebar"] {
  background: #f1f6fc;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
.block-container {
  width: 100%;
  max-width: 1600px;
  padding: 1.5rem 1.5rem 2.5rem;
}
h1 { color: #14294a !important; font-size: 2rem !important; line-height: 1.25 !important; letter-spacing: -.025em; }
h2 { color: #14294a !important; font-size: 1.5rem !important; }
h3 { color: #18385f !important; font-size: 1.2rem !important; }
h4 { color: #18385f !important; font-size: 1.05rem !important; }
p, label, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] {
  color: var(--text) !important;
  font-size: .96rem !important;
  line-height: 1.55 !important;
}
[data-testid="stCaptionContainer"], .stCaption {
  color: var(--muted) !important;
  font-size: .84rem !important;
}
[data-testid="stMetric"] {
  background: #ffffff;
  border: 1px solid var(--border);
  padding: 15px 16px;
  border-radius: 14px;
  box-shadow: 0 4px 14px rgba(27, 57, 93, .06);
}
[data-testid="stMetric"] label {
  color: #526783 !important;
  font-size: .88rem !important;
  font-weight: 650 !important;
}
[data-testid="stMetricValue"] {
  color: #14294a !important;
  font-size: 1.55rem !important;
  font-weight: 750 !important;
}
[data-testid="stMetricDelta"] { font-size: .82rem !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}
[data-testid="stDataFrame"] * { font-size: 13px !important; }
[data-testid="stExpander"] {
  background: #ffffff !important;
  border: 1px solid #d5e2f1 !important;
  border-radius: 12px !important;
  overflow: hidden;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
  color: #18385f !important;
  background: #f1f6fd !important;
  font-size: .96rem !important;
  font-weight: 700 !important;
}
[data-testid="stExpander"] details,
[data-testid="stExpander"] > details > div {
  background: #ffffff !important;
  color: var(--text) !important;
}
.stButton > button, .stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
  min-height: 2.7rem;
  padding: .55rem 1rem;
  font-size: .94rem !important;
  border-radius: 10px;
  border: 1px solid #2878ee;
  font-weight: 700;
  background: linear-gradient(135deg, #2878ee, #1762cb);
  color: #ffffff !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: #13a98f;
  box-shadow: 0 0 0 3px rgba(19,169,143,.12);
}
input, textarea, [data-baseweb="select"] > div {
  background-color: #ffffff !important;
  color: #172b4d !important;
  border: 1px solid #cbd8e7 !important;
  border-radius: 10px !important;
  font-size: .96rem !important;
  min-height: 2.7rem;
}
input::placeholder, textarea::placeholder { color: #8292a8 !important; }
[data-testid="stSlider"] [data-testid="stWidgetLabel"] {
  color: #18385f !important;
  font-size: .94rem !important;
  font-weight: 650 !important;
}
[data-testid="stTabs"] button {
  color: #526783 !important;
  font-size: .94rem !important;
  font-weight: 650;
}
[data-testid="stTabs"] button[aria-selected="true"] { color: #176bd8 !important; }
[data-testid="stAlert"] {
  background: #f0f8f6;
  border: 1px solid #bfe9dd;
  border-radius: 11px;
  color: #175f51 !important;
  font-size: .94rem;
}
[data-testid="stProgressBar"] > div > div {
  background: linear-gradient(90deg, #2878ee, #13b89a);
}
hr { border-color: #e1e8f1; margin: 1rem 0; }
a { color: #176bd8 !important; }
small, .stMarkdown small { color: var(--muted); font-size: .84rem; }
[data-testid="stVerticalBlock"] { gap: .85rem; }
[data-testid="stHorizontalBlock"] { gap: .9rem; }

/* Mobile layout: readable type, full-width controls, and tighter gutters. */
@media (max-width: 768px) {
  .block-container { padding: 1rem .75rem 2rem; }
  h1 { font-size: 1.5rem !important; }
  h2 { font-size: 1.25rem !important; }
  h3 { font-size: 1.08rem !important; }
  p, label, [data-testid="stMarkdownContainer"] { font-size: .93rem !important; }
  [data-testid="stMetric"] { padding: 11px 12px; border-radius: 12px; }
  [data-testid="stMetricValue"] { font-size: 1.25rem !important; }
  .stButton > button, .stDownloadButton > button { width: 100%; min-height: 2.9rem; }
  input, textarea, [data-baseweb="select"] > div { min-height: 2.9rem; }
  [data-testid="stDataFrame"] { overflow-x: auto; }
}
</style>
""", unsafe_allow_html=True)

CG_API = "https://api.coingecko.com/api/v3"
DEX_API = "https://api.dexscreener.com"
NEWS_API = "https://cryptopanic.com/api/v1/posts/"

# =========================================================
# HELPERS / KEYS
# =========================================================
def secret_or_env(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value).strip()
    except Exception:
        pass
    return os.getenv(name, "").strip()


def cg_headers(api_key: str):
    return {"x-cg-demo-api-key": api_key} if api_key else {}


def safe_get(url, *, params=None, headers=None, timeout=20):
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def numeric(series):
    return pd.to_numeric(series, errors="coerce")


def fmt_num(value, digits=2):
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return "N/A"


def fmt_money(value, currency):
    try:
        if pd.isna(value):
            return "N/A"
        value = float(value)
        return f"{currency.upper()} {value:,.8f}" if abs(value) < 1 else f"{currency.upper()} {value:,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def rsi(series, period=14):
    s = pd.Series(series, dtype="float64")
    delta = s.diff()
    gain = delta.clip(lower=0).rolling(period, min_periods=period).mean()
    loss = (-delta.clip(upper=0)).rolling(period, min_periods=period).mean()
    rs = gain / loss.replace(0, np.nan)
    out = 100 - (100 / (1 + rs))
    out = out.where(~((loss == 0) & (gain > 0)), 100)
    out = out.where(~((gain == 0) & (loss > 0)), 0)
    return out


def technical_summary(prices, volumes=None):
    """Price structure plus rolling 24h-volume expansion; not a trading guarantee."""
    p = pd.Series(prices, dtype="float64").dropna()
    if len(p) < 30:
        return {"RSI_14": np.nan, "MACD": np.nan, "MACD_Signal": np.nan,
                "Trend_7d_Percent": np.nan, "Technical_Score": np.nan,
                "Technical_Signal": "Insufficient history"}
    ema12 = p.ewm(span=12, adjust=False).mean()
    ema26 = p.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    latest_rsi = rsi(p, 14).iloc[-1]
    trend = ((p.iloc[-1] / p.iloc[0]) - 1) * 100 if p.iloc[0] else np.nan
    score = 50.0
    if pd.notna(latest_rsi):
        if 50 <= latest_rsi <= 68:
            score += 20
        elif 40 <= latest_rsi < 50:
            score += 8
        elif latest_rsi > 75:
            score -= 12
        elif latest_rsi < 30:
            score += 5
        elif latest_rsi < 40:
            score -= 5
    if macd.iloc[-1] > signal.iloc[-1]:
        score += 15
    else:
        score -= 8
    if pd.notna(trend):
        score += float(np.clip(trend * 1.2, -20, 20))
    score = float(np.clip(score, 0, 100))
    signal_text = "Bullish momentum" if macd.iloc[-1] > signal.iloc[-1] and 45 <= latest_rsi <= 72 else (
        "Overheated / caution" if latest_rsi > 75 else "Mixed / watch"
    )
    volume_ratio = np.nan
    if volumes is not None:
        v = pd.to_numeric(pd.Series(volumes), errors="coerce").dropna()
        # CoinGecko's total_volumes series is a rolling 24h market-volume snapshot.
        # Compare the latest day of hourly snapshots with the preceding observations.
        if len(v) >= 48:
            recent_volume = v.tail(24).median()
            baseline_volume = v.iloc[:-24].median()
            if pd.notna(baseline_volume) and baseline_volume > 0:
                volume_ratio = float(recent_volume / baseline_volume)
    return {
        "RSI_14": round(float(latest_rsi), 2) if pd.notna(latest_rsi) else np.nan,
        "MACD": round(float(macd.iloc[-1]), 8),
        "MACD_Signal": round(float(signal.iloc[-1]), 8),
        "Trend_7d_Percent": round(float(trend), 2) if pd.notna(trend) else np.nan,
        "Technical_Score": round(score, 2),
        "Technical_Signal": signal_text,
        "Volume_24h_vs_7d_Avg": round(volume_ratio, 3) if pd.notna(volume_ratio) else np.nan,
    }


STABLECOIN_SYMBOLS = {
    "USDT", "USDC", "USDE", "USDS", "DAI", "FDUSD", "TUSD", "USDP",
    "USDD", "PYUSD", "USD1", "USDX", "USDSC", "GUSD", "FRAX",
    "LUSD", "USDB", "USDTB", "EURC", "EURS", "EUROC",
    "USTC", "UST", "SUSD", "USDK", "USDF", "USD0", "EURCV",
}
STABLECOIN_NAME_HINTS = (
    "tether", "usd coin", "usdc", "usdt", "first digital usd",
    "paypal usd", "trueusd", "pax dollar", "dai stablecoin",
    "frax", "liquity usd", "staked usde", "ethena usde", "euro coinvertible", "eur coinvertible",
    "stablecoin", "usd1", "usdd", "gemini dollar",
)

def mark_stablecoins(frame):
    out = frame.copy()
    symbols = out.get("Symbol", pd.Series("", index=out.index)).astype(str).str.upper().str.strip()
    names = out.get("Coin", pd.Series("", index=out.index)).astype(str).str.lower()
    ids = out.get("CoinGecko_ID", pd.Series("", index=out.index)).astype(str).str.lower()
    symbol_match = symbols.isin(STABLECOIN_SYMBOLS)
    name_match = names.apply(lambda value: any(hint in value for hint in STABLECOIN_NAME_HINTS))
    id_match = ids.str.contains(r"tether|usd-coin|first-digital-usd|paypal-usd|true-usd|pax-dollar|dai$|frax|ethena-usde|usd1", regex=True, na=False)
    out["Is_Stablecoin"] = symbol_match | name_match | id_match

    # Tokenized equities are not cryptocurrencies and should not compete in this ranking.
    equity_hints = ("tokenized stock", "tokenised stock", "bstocks", "xstocks", "tracker certificate")
    equity_name_match = names.apply(lambda value: any(hint in value for hint in equity_hints))
    equity_symbol_match = symbols.str.endswith("B", na=False) & names.str.contains("stock|equity|share", na=False)
    out["Is_Tokenized_Equity"] = equity_name_match | equity_symbol_match
    out["Is_Excluded_Asset"] = out["Is_Stablecoin"] | out["Is_Tokenized_Equity"]
    return out



def attach_actual_buy_sell_flow(frame):
    """Attach only provider-reported buy/sell USD volumes; never infer USD flow from txn counts."""
    out = frame.copy()
    out["Buy_Volume_USD"] = np.nan
    out["Sell_Volume_USD"] = np.nan
    out["Net_Buy_USD"] = np.nan
    out["Buy_Share_Percent"] = np.nan
    rows = st.session_state.get("cm_actual_buy_sell_rows", [])
    if not rows:
        return out
    flow = pd.DataFrame(rows)
    required = {"Symbol", "Buy volume (USDT)", "Sell volume (USDT)"}
    if not required.issubset(flow.columns):
        return out
    flow["Symbol"] = flow["Symbol"].astype(str).str.upper().str.strip()
    flow["Buy volume (USDT)"] = numeric(flow["Buy volume (USDT)"])
    flow["Sell volume (USDT)"] = numeric(flow["Sell volume (USDT)"])
    flow = flow.dropna(subset=["Buy volume (USDT)", "Sell volume (USDT)"])
    if flow.empty:
        return out
    flow = flow.groupby("Symbol", as_index=False).agg({
        "Buy volume (USDT)": "sum", "Sell volume (USDT)": "sum"
    })
    flow["Net_Buy_USD"] = flow["Buy volume (USDT)"] - flow["Sell volume (USDT)"]
    total = flow["Buy volume (USDT)"] + flow["Sell volume (USDT)"]
    flow["Buy_Share_Percent"] = np.where(total > 0, flow["Buy volume (USDT)"] / total * 100, np.nan)
    flow = flow.rename(columns={
        "Buy volume (USDT)": "Buy_Volume_USD",
        "Sell volume (USDT)": "Sell_Volume_USD",
    })
    out = out.drop(columns=["Buy_Volume_USD", "Sell_Volume_USD", "Net_Buy_USD", "Buy_Share_Percent"], errors="ignore")
    return out.merge(flow[["Symbol", "Buy_Volume_USD", "Sell_Volume_USD", "Net_Buy_USD", "Buy_Share_Percent"]],
                     on="Symbol", how="left")


def _btc_market_context(frame):
    """A small market-regime adjustment derived from the loaded BTC market row."""
    btc = frame[frame["Symbol"].astype(str).str.upper().eq("BTC")]
    if btc.empty:
        return 0.0, "BTC context unavailable"
    row = btc.iloc[0]
    d24 = pd.to_numeric(pd.Series([row.get("Change_24h_Percent")]), errors="coerce").iloc[0]
    d7 = pd.to_numeric(pd.Series([row.get("Change_7d_Percent")]), errors="coerce").iloc[0]
    if pd.isna(d24) or pd.isna(d7):
        return 0.0, "BTC context incomplete"
    if d24 >= 1 and d7 >= 2:
        return 5.0, "BTC supportive"
    if d24 <= -2 and d7 <= -4:
        return -10.0, "BTC weak — risk-off"
    if d24 < 0 and d7 < 0:
        return -5.0, "BTC mildly weak"
    return 0.0, "BTC neutral / mixed"

def calculate_pre_pump_score(frame):
    """Strict early-activity screen. A confirmed watch requires historical volume expansion."""
    out = mark_stablecoins(frame)
    out = attach_actual_buy_sell_flow(out)
    ch24 = numeric(out.get("Change_24h_Percent", pd.Series(np.nan, index=out.index)))
    ch7 = numeric(out.get("Change_7d_Percent", pd.Series(np.nan, index=out.index)))
    volume = numeric(out.get("Volume_24h", pd.Series(np.nan, index=out.index)))
    market_cap = numeric(out.get("Market_Cap", pd.Series(np.nan, index=out.index)))
    turnover = (volume / market_cap.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
    out["Volume_to_Market_Cap"] = turnover

    eligible = ~out["Is_Excluded_Asset"]
    activity = turnover.where(eligible).rank(pct=True) * 100
    out["Volume_Activity_Score"] = activity.fillna(0).clip(0, 100)

    # Price must still be relatively quiet; missing price changes are not treated as proof.
    abs24, abs7 = ch24.abs(), ch7.abs()
    quiet24 = pd.Series(np.select([abs24 <= 2, abs24 <= 4, abs24 <= 7], [100, 75, 35], default=0), index=out.index, dtype=float)
    quiet7 = pd.Series(np.select([abs7 <= 5, abs7 <= 12, abs7 <= 20], [100, 75, 35], default=0), index=out.index, dtype=float)
    quiet24 = quiet24.where(ch24.notna(), 0)
    quiet7 = quiet7.where(ch7.notna(), 0)
    out["Price_Still_Quiet_Score"] = (0.45 * quiet24 + 0.55 * quiet7).clip(0, 100)

    cap_score = pd.Series(np.select([market_cap >= 250_000_000, market_cap >= 75_000_000,
                                     market_cap >= 20_000_000, market_cap >= 10_000_000],
                                    [100, 85, 70, 50], default=0), index=out.index, dtype=float)
    vol_score = pd.Series(np.select([volume >= 10_000_000, volume >= 2_000_000,
                                     volume >= 500_000, volume >= 300_000],
                                    [100, 85, 65, 45], default=0), index=out.index, dtype=float)
    out["Liquidity_Quality_Score"] = (0.55 * cap_score + 0.45 * vol_score).clip(0, 100)

    rsi_value = numeric(out.get("RSI_14", pd.Series(np.nan, index=out.index)))
    macd = numeric(out.get("MACD", pd.Series(np.nan, index=out.index)))
    macd_signal = numeric(out.get("MACD_Signal", pd.Series(np.nan, index=out.index)))
    tech = (100 - (rsi_value - 55).abs() * 2.0).clip(0, 100)
    tech = pd.Series(tech, index=out.index).fillna(45)
    tech += np.where(macd.notna() & macd_signal.notna(), np.where(macd > macd_signal, 10, -10), 0)
    tech = tech.clip(0, 100)
    surge = numeric(out.get("Volume_24h_vs_7d_Avg", pd.Series(np.nan, index=out.index)))
    surge_score = pd.Series(np.select([surge >= 3, surge >= 2, surge >= 1.5, surge >= 1.2],
                                      [100, 85, 70, 50], default=0), index=out.index, dtype=float)
    # Missing volume history gets a neutral-low score, never a positive confirmation.
    surge_score = surge_score.where(surge.notna(), 25)
    out["Technical_PrePump_Score"] = (0.65 * tech + 0.35 * surge_score).clip(0, 100)

    turnover_score = pd.Series(np.select([turnover >= 0.005, turnover >= 0.0025,
                                          turnover >= 0.001], [90, 75, 55], default=10),
                               index=out.index, dtype=float)
    out["Turnover_Quality_Score"] = turnover_score
    # Base screen is provisional until genuine buy/sell USD data is available.
    base_raw = (0.25 * out["Volume_Activity_Score"] + 0.25 * out["Price_Still_Quiet_Score"] +
                0.25 * out["Liquidity_Quality_Score"] + 0.25 * out["Technical_PrePump_Score"])
    buy_share = numeric(out.get("Buy_Share_Percent", pd.Series(np.nan, index=out.index)))
    net_buy = numeric(out.get("Net_Buy_USD", pd.Series(np.nan, index=out.index)))
    flow_available = buy_share.notna() & net_buy.notna()
    # Buy-side dominance score: 50 is balanced, >50 is net buying, <50 is net selling.
    flow_score = ((buy_share - 50) * 4 + 50).clip(0, 100)
    out["Buy_Flow_Score"] = flow_score.where(flow_available, np.nan)
    out["Buy_Flow_Status"] = np.select(
        [~flow_available, (net_buy > 0) & (buy_share >= 55), (net_buy > 0) & (buy_share > 50), net_buy < 0],
        ["حجم خرید/فروش واقعی دریافت نشده", "غلبه خرید واقعی", "خرید کمی بیشتر از فروش", "غلبه فروش واقعی"],
        default="خرید و فروش تقریباً متعادل"
    )
    # When flow is present it receives 35% of the score; otherwise show a provisional
    # score from the other evidence, but never call it a confirmed pre-pump setup.
    raw = base_raw.where(~flow_available, 0.65 * base_raw + 0.35 * flow_score)
    btc_adjustment, btc_context = _btc_market_context(out)
    out["BTC_Market_Context"] = btc_context
    raw = (raw + btc_adjustment).clip(0, 100)

    overheated = (ch24 >= 8) | (ch7 >= 20) | (ch24 <= -18) | (ch7 <= -35)
    thin = (market_cap.fillna(0) < 10_000_000) | (volume.fillna(0) < 300_000)
    missing_market = market_cap.isna() | volume.isna() | ch24.isna() | ch7.isna()
    no_activity = surge.isna() | (surge < 1.2)
    extreme_turnover = turnover > 0.20
    penalty = (np.where(overheated, 22, 0) + np.where(thin, 30, 0) +
               np.where(missing_market, 20, 0) + np.where(extreme_turnover, 20, 0) +
               np.where(no_activity, 10, 0))
    out["PrePump_Risk_Penalty"] = penalty
    score = (raw - penalty).clip(0, 100).where(eligible, 0)
    out["PrePump_Score"] = score.round(1)
    out["Pump_Potential_Score"] = out["PrePump_Score"]

    positive_flow = flow_available & (net_buy > 0) & (buy_share >= 52)
    valid_setup = (eligible & ~overheated & ~thin & ~missing_market & ~extreme_turnover &
                   ch24.abs().le(5) & ch7.abs().le(12) & surge.ge(1.5) &
                   turnover.between(0.001, 0.15) & score.ge(70) & positive_flow)
    watch_setup = (eligible & ~overheated & ~thin & ~missing_market & ~extreme_turnover &
                   ch24.abs().le(7) & ch7.abs().le(18) & turnover.between(0.001, 0.15) & score.ge(60))
    out["Signal"] = np.select(
        [out["Is_Stablecoin"], out["Is_Tokenized_Equity"], overheated, valid_setup,
         watch_setup & ~flow_available, watch_setup & flow_available & ~positive_flow, watch_setup],
        ["Excluded — stablecoin", "Excluded — tokenized equity", "Already moving / abnormal volatility — caution",
         "Pre-pump watch — real buying + volume confirmed",
         "Early activity — real buy/sell data missing",
         "Early activity — buy pressure not confirmed",
         "Early activity — monitor"], default="Watch — not enough evidence")
    out["Risk_Level"] = np.select(
        [out["Is_Stablecoin"], out["Is_Tokenized_Equity"], thin, overheated, extreme_turnover, missing_market],
        ["Excluded — stablecoin", "Excluded — tokenized equity", "High / thin market", "High / volatile", "High / abnormal turnover", "Incomplete market data"],
        default="Medium / review")
    return out


# =========================================================
# DATA SOURCES
# =========================================================
@st.cache_data(ttl=120, show_spinner=False)
def fetch_market_pages(currency, pages, api_key):
    """Fetches up to pages*250 CoinGecko market rows, subject to API access/rate limits."""
    rows = []
    for page in range(1, int(pages) + 1):
        data = safe_get(
            f"{CG_API}/coins/markets",
            params={
                "vs_currency": currency,
                "order": "market_cap_desc",
                "per_page": 250,
                "page": page,
                "sparkline": "false",
                "price_change_percentage": "24h,7d",
            },
            headers=cg_headers(api_key),
            timeout=25,
        )
        if not isinstance(data, list) or not data:
            break
        rows.extend(data)
        if len(data) < 250:
            break
        # Gentle pause between pages to reduce request bursts.
        if page < int(pages):
            time.sleep(0.25)

    if not rows:
        raise ValueError("CoinGecko returned no market rows.")
    raw = pd.DataFrame(rows)
    def col(name):
        return raw[name] if name in raw.columns else pd.Series(np.nan, index=raw.index)
    df = pd.DataFrame({
        "Coin": col("name"),
        "CoinGecko_ID": col("id"),
        "Symbol": col("symbol").astype("string").str.upper(),
        "Price": col("current_price"),
        "Change_24h_Percent": col("price_change_percentage_24h"),
        "Change_7d_Percent": col("price_change_percentage_7d_in_currency"),
        "Volume_24h": col("total_volume"),
        "Market_Cap": col("market_cap"),
        "Market_Cap_Rank": col("market_cap_rank"),
        "Circulating_Supply": col("circulating_supply"),
        "Total_Supply": col("total_supply"),
        "ATH_Change_Percent": col("ath_change_percentage"),
        "Last_Updated": col("last_updated"),
    })
    for c in ["Price", "Change_24h_Percent", "Change_7d_Percent", "Volume_24h",
              "Market_Cap", "Market_Cap_Rank", "Circulating_Supply", "Total_Supply",
              "ATH_Change_Percent"]:
        df[c] = numeric(df[c])
    # Market-only preliminary score. It is explicitly not a calibrated probability.
    ch24 = df["Change_24h_Percent"].fillna(0)
    ch7 = df["Change_7d_Percent"].fillna(0)
    df["Market_Momentum_Score"] = (50 + 1.4 * ch24 + 0.8 * ch7).clip(0, 100).round(2)
    df["Technical_Score"] = np.nan
    df["RSI_14"] = np.nan
    df["MACD"] = np.nan
    df["MACD_Signal"] = np.nan
    df["Trend_7d_Percent"] = np.nan
    df["Technical_Signal"] = "Not calculated"
    df["News_Score"] = np.nan
    df["News_Summary"] = "News API not configured"
    df["Pump_Potential_Score"] = df["Market_Momentum_Score"]
    df["Risk_Level"] = "Unassessed"
    df["Signal"] = "Watch"
    return df


@st.cache_data(ttl=300, show_spinner=False)
def fetch_history(coin_id, currency, days, api_key):
    payload = safe_get(
        f"{CG_API}/coins/{coin_id}/market_chart",
        params={"vs_currency": currency, "days": int(days)},
        headers=cg_headers(api_key),
        timeout=25,
    )
    prices = pd.DataFrame(payload.get("prices", []), columns=["timestamp_ms", "price"])
    if prices.empty:
        return prices
    volumes = pd.DataFrame(payload.get("total_volumes", []), columns=["timestamp_ms", "volume_24h"])
    if not volumes.empty:
        prices = prices.merge(volumes, on="timestamp_ms", how="left")
    else:
        prices["volume_24h"] = np.nan
    prices["Time"] = pd.to_datetime(prices["timestamp_ms"], unit="ms", utc=True)
    prices["price"] = numeric(prices["price"])
    prices["volume_24h"] = numeric(prices["volume_24h"])
    return prices.dropna(subset=["price"])


@st.cache_data(ttl=180, show_spinner=False)
def fetch_news(currency_api_key, coin_symbol=None):
    if not currency_api_key:
        return pd.DataFrame(), "No CryptoPanic API key configured"
    params = {"auth_token": currency_api_key, "public": "true", "kind": "news"}
    if coin_symbol:
        params["currencies"] = str(coin_symbol).lower()
    try:
        payload = safe_get(NEWS_API, params=params, timeout=20)
        results = payload.get("results", [])
        rows = []
        for item in results:
            votes = item.get("votes") or {}
            title = item.get("title", "")
            rows.append({
                "Published": item.get("published_at"),
                "Title": title,
                "Source": (item.get("source") or {}).get("title", ""),
                "Currencies": ", ".join(
                    (c.get("code", "") for c in (item.get("currencies") or []))
                ),
                "Positive_Votes": votes.get("positive", 0),
                "Negative_Votes": votes.get("negative", 0),
                "URL": item.get("url", ""),
            })
        return pd.DataFrame(rows), "ok"
    except Exception as exc:
        return pd.DataFrame(), str(exc)


@st.cache_data(ttl=90, show_spinner=False)
def fetch_dex_search(query):
    """Searches DEX Screener by query; it does not enumerate every token on every chain."""
    payload = safe_get(f"{DEX_API}/latest/dex/search", params={"q": query}, timeout=20)
    pairs = payload.get("pairs") or []
    rows = []
    for p in pairs:
        base = p.get("baseToken") or {}
        quote = p.get("quoteToken") or {}
        txns = p.get("txns") or {}
        h24 = txns.get("h24") or {}
        vol = p.get("volume") or {}
        liq = p.get("liquidity") or {}
        price_change = p.get("priceChange") or {}
        rows.append({
            "Chain": p.get("chainId", ""),
            "DEX": p.get("dexId", ""),
            "Pair": p.get("pairAddress", ""),
            "Token": base.get("name", ""),
            "Symbol": str(base.get("symbol", "")).upper(),
            "Price_USD": p.get("priceUsd"),
            "Change_5m_Percent": price_change.get("m5"),
            "Change_1h_Percent": price_change.get("h1"),
            "Change_6h_Percent": price_change.get("h6"),
            "Change_24h_Percent": price_change.get("h24"),
            "Volume_24h_USD": vol.get("h24"),
            "Liquidity_USD": liq.get("usd"),
            "Buys_24h": h24.get("buys"),
            "Sells_24h": h24.get("sells"),
            "Pair_URL": p.get("url", ""),
            "Created_At": p.get("pairCreatedAt"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        for c in ["Price_USD", "Change_5m_Percent", "Change_1h_Percent", "Change_6h_Percent",
                  "Change_24h_Percent", "Volume_24h_USD", "Liquidity_USD", "Buys_24h", "Sells_24h"]:
            df[c] = numeric(df[c])
        # Simple DEX screening score, deliberately penalizes low liquidity.
        ch = df["Change_24h_Percent"].fillna(0).clip(-50, 100)
        vol = np.log10(df["Volume_24h_USD"].fillna(0).clip(lower=0) + 1)
        liq = df["Liquidity_USD"].fillna(0)
        buy = df["Buys_24h"].fillna(0)
        sell = df["Sells_24h"].fillna(0)
        buy_ratio = buy / (buy + sell).replace(0, np.nan)
        total_txns = buy + sell
        buy_ratio = buy_ratio.fillna(0.5).clip(0, 1)
        df["Transactions_24h"] = total_txns
        df["Buy_Count_Share_Percent"] = (buy_ratio * 100).round(1)
        df["Buy_Sell_Count_Ratio"] = (buy / sell.replace(0, np.nan)).round(2)
        # Approximate split of reported volume using transaction-count share only.
        # This is NOT actual buy/sell USD flow because average trade sizes may differ.
        df["Estimated_Buy_Volume_Proxy_USD"] = (df["Volume_24h_USD"].fillna(0) * buy_ratio).round(2)
        df["Estimated_Sell_Volume_Proxy_USD"] = (df["Volume_24h_USD"].fillna(0) * (1 - buy_ratio)).round(2)
        df["Volume_to_Liquidity_Ratio"] = (
            df["Volume_24h_USD"] / liq.replace(0, np.nan)
        ).round(2)
        df["Activity_Flag"] = np.where(
            (df["Volume_to_Liquidity_Ratio"] >= 3) & (total_txns >= 1000),
            "Unusually high trading activity — investigate",
            np.where(total_txns >= 500, "Active trading", "Limited activity / verify data")
        )
        df["DEX_Screen_Score"] = (
            45 + ch * 0.7 + vol * 3 + (buy_ratio - 0.5) * 20
        ).clip(0, 100).round(2)
        df["Risk_Flag"] = np.where(liq < 50000, "High: low liquidity",
                           np.where(liq < 200000, "Medium: check liquidity", "Review contract / market"))
        df = df.sort_values(["DEX_Screen_Score", "Liquidity_USD"], ascending=False, na_position="last")
    return df


# =========================================================
# BYBIT PUBLIC DERIVATIVES SNAPSHOT (NO API KEY REQUIRED)
# =========================================================
BYBIT_API = "https://api.bybit.com"


@st.cache_data(ttl=90, show_spinner=False)
def fetch_bybit_derivatives():
    """Try Bybit, then OKX public SWAP data, then Gate.io public USDT futures."""
    errors = []
    # 1) Bybit
    try:
        payload = safe_get(f"{BYBIT_API}/v5/market/tickers", params={"category": "linear"}, timeout=15)
        if not isinstance(payload, dict) or payload.get("retCode") != 0:
            raise RuntimeError((payload or {}).get("retMsg", "unexpected Bybit response"))
        records = []
        for item in (payload.get("result") or {}).get("list") or []:
            pair = str(item.get("symbol", "")).upper()
            if not pair.endswith("USDT"):
                continue
            def fnum(key, scale=1.0):
                try: return float(item.get(key)) * scale
                except (TypeError, ValueError): return np.nan
            records.append({"Symbol": pair[:-4], "Derivatives_Exchange": "Bybit",
                "Derivatives_Pair": pair, "Funding_Rate_Percent": fnum("fundingRate", 100),
                "Open_Interest_USD": fnum("openInterestValue"),
                "Derivatives_Turnover_24h_USD": fnum("turnover24h"),
                "Derivatives_Change_24h_Percent": fnum("price24hPcnt", 100),
                "Next_Funding_Time": item.get("nextFundingTime")})
        frame = pd.DataFrame(records)
        if not frame.empty:
            return frame.sort_values("Derivatives_Turnover_24h_USD", ascending=False).drop_duplicates("Symbol")
        errors.append("Bybit returned no USDT perpetual tickers")
    except Exception as exc:
        errors.append(f"Bybit: {str(exc)[:100]}")

    # 2) OKX public market endpoints. Tickers + open interest are bulk requests;
    # funding is requested only for the 60 most active USDT perpetuals to respect rate limits.
    try:
        base = "https://www.okx.com"
        tick_payload = safe_get(f"{base}/api/v5/market/tickers", params={"instType": "SWAP"}, timeout=18)
        if str(tick_payload.get("code")) != "0":
            raise RuntimeError(tick_payload.get("msg", "OKX ticker error"))
        tickers = [x for x in tick_payload.get("data", []) if str(x.get("instId", "")).endswith("-USDT-SWAP")]
        if not tickers:
            raise RuntimeError("OKX returned no USDT perpetual tickers")
        oi_payload = safe_get(f"{base}/api/v5/public/open-interest", params={"instType": "SWAP"}, timeout=18)
        if str(oi_payload.get("code")) != "0":
            raise RuntimeError(oi_payload.get("msg", "OKX open-interest error"))
        oi_map = {x.get("instId"): x for x in oi_payload.get("data", [])}
        tickers.sort(key=lambda x: float(x.get("volCcy24h") or 0) * float(x.get("last") or 0), reverse=True)
        records = []
        for item in tickers[:60]:
            inst_id = item.get("instId", "")
            symbol = inst_id.replace("-USDT-SWAP", "")
            oi_item = oi_map.get(inst_id, {})
            try: oi_usd = float(oi_item.get("oiUsd"))
            except (TypeError, ValueError): oi_usd = np.nan
            try: turnover = float(item.get("volCcy24h")) * float(item.get("last"))
            except (TypeError, ValueError): turnover = np.nan
            try: change = (float(item.get("last")) / float(item.get("open24h")) - 1) * 100
            except (TypeError, ValueError, ZeroDivisionError): change = np.nan
            funding = np.nan
            try:
                fp = safe_get(f"{base}/api/v5/public/funding-rate", params={"instId": inst_id}, timeout=12)
                if str(fp.get("code")) == "0" and fp.get("data"):
                    funding = float(fp["data"][0].get("fundingRate")) * 100
            except Exception:
                pass
            records.append({"Symbol": symbol, "Derivatives_Exchange": "OKX",
                "Derivatives_Pair": inst_id, "Funding_Rate_Percent": funding,
                "Open_Interest_USD": oi_usd, "Derivatives_Turnover_24h_USD": turnover,
                "Derivatives_Change_24h_Percent": change, "Next_Funding_Time": None})
            time.sleep(0.10)
        frame = pd.DataFrame(records)
        if not frame.empty:
            return frame.drop_duplicates("Symbol")
        errors.append("OKX returned no usable USDT perpetuals")
    except Exception as exc:
        errors.append(f"OKX: {str(exc)[:100]}")

    # 3) Gate.io public fallback
    try:
        gate_rows = safe_get("https://api.gateio.ws/api/v4/futures/usdt/tickers", timeout=18)
        if not isinstance(gate_rows, list):
            raise RuntimeError("Gate.io returned an unexpected ticker response")
        records = []
        for item in gate_rows:
            pair = str(item.get("contract", "")).upper()
            if not pair.endswith("_USDT"):
                continue
            try: funding = float(item.get("funding_rate")) * 100
            except (TypeError, ValueError): funding = np.nan
            try: oi_value = float(item.get("open_interest_usd"))
            except (TypeError, ValueError): oi_value = np.nan
            try: turnover = float(item.get("volume_24h_usd"))
            except (TypeError, ValueError):
                try: turnover = float(item.get("volume_24h_quote"))
                except (TypeError, ValueError): turnover = np.nan
            try: change_24h = float(item.get("change_percentage"))
            except (TypeError, ValueError): change_24h = np.nan
            records.append({"Symbol": pair[:-5], "Derivatives_Exchange": "Gate.io",
                "Derivatives_Pair": pair, "Funding_Rate_Percent": funding,
                "Open_Interest_USD": oi_value, "Derivatives_Turnover_24h_USD": turnover,
                "Derivatives_Change_24h_Percent": change_24h, "Next_Funding_Time": None})
        frame = pd.DataFrame(records)
        if frame.empty:
            raise RuntimeError("Gate.io returned no USDT perpetual tickers")
        return frame.sort_values("Derivatives_Turnover_24h_USD", ascending=False).drop_duplicates("Symbol")
    except Exception as exc:
        errors.append(f"Gate.io: {str(exc)[:100]}")
        raise RuntimeError("All public derivatives feeds failed. " + " | ".join(errors))



def add_derivatives_score(frame):
    """Add a small positioning context weight; never treat OI as cash inflow."""
    out = frame.copy()
    funding = numeric(out.get("Funding_Rate_Percent", pd.Series(np.nan, index=out.index)))
    oi = numeric(out.get("Open_Interest_USD", pd.Series(np.nan, index=out.index)))
    oi_score = (oi.rank(pct=True) * 100).where(oi.notna(), 50).fillna(50)
    funding_score = pd.Series(np.select(
        [funding <= -0.10, funding <= -0.02, funding <= 0.01, funding <= 0.05, funding <= 0.10],
        [45, 82, 75, 55, 30], default=15
    ), index=out.index, dtype=float).where(funding.notna(), 50)
    out["OI_Relative_Score"] = oi_score.round(1)
    out["Funding_Positioning_Score"] = funding_score.round(1)
    has_derivatives = funding.notna() | oi.notna()
    out["Derivatives_Context_Score"] = (0.55 * oi_score + 0.45 * funding_score).round(1)
    base = numeric(out.get("PrePump_Score", pd.Series(np.nan, index=out.index)))
    if base.notna().any():
        combined = 0.92 * base + 0.08 * out["Derivatives_Context_Score"]
        out["PrePump_Score"] = combined.where(has_derivatives, base).clip(0, 100).round(1)
        out["Pump_Potential_Score"] = out["PrePump_Score"]
    return out


# =========================================================
# CRYPTOMETER API
# =========================================================
CRYPTOMETER_API = "https://api.cryptometer.io"


@st.cache_data(ttl=300, show_spinner=False)
def fetch_cryptometer(endpoint: str, params: dict, api_key: str):
    """Fetch one CryptoMeter endpoint. The API key is never included in UI errors."""
    query = dict(params or {})
    query["api_key"] = api_key
    try:
        response = requests.get(
            f"{CRYPTOMETER_API}/{endpoint.strip('/')}/",
            params=query,
            timeout=25,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"Network error while calling CryptoMeter: {exc.__class__.__name__}") from None

    if response.status_code in (401, 403):
        raise RuntimeError("CryptoMeter rejected the key or this endpoint is not enabled for your plan (HTTP 401/403).")
    if response.status_code == 429:
        raise RuntimeError("CryptoMeter rate limit or monthly quota reached (HTTP 429).")
    if response.status_code >= 500:
        raise RuntimeError(f"CryptoMeter server error (HTTP {response.status_code}). Try again later.")
    if not response.ok:
        raise RuntimeError(f"CryptoMeter request failed (HTTP {response.status_code}). Check endpoint access and parameters.")

    try:
        payload = response.json()
    except ValueError:
        raise RuntimeError("CryptoMeter returned a response that was not valid JSON.") from None

    if isinstance(payload, dict):
        success = payload.get("success")
        error_flag = payload.get("error")
        if str(success).strip().lower() == "false" or str(error_flag).strip().lower() == "true":
            message = payload.get("message") or payload.get("msg") or payload.get("error_message")
            raise RuntimeError(str(message or "CryptoMeter reported an API error.")[:240])
    return payload


@st.cache_data(ttl=60, show_spinner=False)
def fetch_cryptometer_buy_sell_volume(symbol: str, exchange: str, api_key: str):
    """Fetch provider-reported 24h buy/sell traded volume for one exchange pair.

    The endpoint reports buy/sell volume for a specified market pair; this is
    not wallet-level whale flow and is not inferred from transaction counts.
    """
    clean_symbol = str(symbol or "").strip().upper()
    if not clean_symbol:
        raise ValueError("A coin symbol is required")
    pair = f"{clean_symbol}-USDT"
    payload = fetch_cryptometer("24h-trade-volume-v2", {"pair": pair, "e": exchange}, api_key)
    data = cryptometer_data(payload)
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not data:
        return {"Symbol": clean_symbol, "Pair": pair, "Exchange": exchange,
                "Buy volume (USDT)": np.nan, "Sell volume (USDT)": np.nan,
                "Net buy (USDT)": np.nan, "Buy share (%)": np.nan,
                "Data status": "No trade-volume rows returned"}
    row = data[0] if isinstance(data[0], dict) else {}
    buy = pd.to_numeric(pd.Series([row.get("buy")]), errors="coerce").iloc[0]
    sell = pd.to_numeric(pd.Series([row.get("sell")]), errors="coerce").iloc[0]
    if pd.isna(buy) or pd.isna(sell):
        return {"Symbol": clean_symbol, "Pair": pair, "Exchange": exchange,
                "Buy volume (USDT)": np.nan, "Sell volume (USDT)": np.nan,
                "Net buy (USDT)": np.nan, "Buy share (%)": np.nan,
                "Data status": "Response lacks buy/sell values"}
    total = float(buy) + float(sell)
    return {"Symbol": clean_symbol, "Pair": pair, "Exchange": exchange,
            "Buy volume (USDT)": float(buy), "Sell volume (USDT)": float(sell),
            "Net buy (USDT)": float(buy) - float(sell),
            "Buy share (%)": (float(buy) / total * 100) if total > 0 else np.nan,
            "Data status": "Provider buy/sell volume"}


def cryptometer_data(payload):
    """Return the endpoint's `data` value without assuming a single response shape."""
    if isinstance(payload, dict):
        return payload.get("data", payload)
    return payload


def cryptometer_frame(payload):
    data = cryptometer_data(payload)
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        # Some endpoints return a single record rather than a list of records.
        return pd.DataFrame([data])
    return pd.DataFrame()


def _cm_number(value):
    try:
        value = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
        return float(value) if pd.notna(value) else 0.0
    except Exception:
        return 0.0


def cryptometer_watchlist(results):
    """Build a transparent evidence score only from symbol-level returned evidence."""
    evidence = {}

    def slot(symbol):
        symbol = str(symbol or "").strip().upper()
        if not symbol:
            return None
        return evidence.setdefault(symbol, {
            "Symbol": symbol, "Rapid bias": 0, "Rapid events": 0,
            "Whale buys USD": 0.0, "Whale sells USD": 0.0,
            "Netflow USD": np.nan,
        })

    rapid_result = results.get("rapid") or {}
    if rapid_result.get("payload"):
        rapid = cryptometer_frame(rapid_result["payload"])
        for _, row in rapid.iterrows():
            symbol = row.get("symbol")
            if not symbol:
                symbol = str(row.get("pair", "")).split("-")[0]
            item = slot(symbol)
            if item is None:
                continue
            side = str(row.get("side", row.get("direction", ""))).upper()
            if side in ("PUMP", "BUY", "UP"):
                item["Rapid bias"] += 1
            elif side in ("DUMP", "SELL", "DOWN"):
                item["Rapid bias"] -= 1
            item["Rapid events"] += 1

    whale_result = results.get("whales") or {}
    if whale_result.get("payload"):
        whales = cryptometer_frame(whale_result["payload"])
        for _, row in whales.iterrows():
            symbol = row.get("symbol") or str(row.get("pair", "")).split("-")[0]
            item = slot(symbol)
            if item is None:
                continue
            usd = _cm_number(row.get("usd_total", row.get("total", 0)))
            side = str(row.get("side", "")).upper()
            if side == "BUY":
                item["Whale buys USD"] += usd
            elif side == "SELL":
                item["Whale sells USD"] += usd

    flow_result = results.get("liquidity") or {}
    if flow_result.get("payload"):
        flow_data = cryptometer_data(flow_result["payload"])
        if isinstance(flow_data, dict):
            for symbol, values in flow_data.items():
                if isinstance(values, dict) and "netflow" in values:
                    item = slot(symbol)
                    if item is not None:
                        item["Netflow USD"] = _cm_number(values.get("netflow"))

    rows = []
    for item in evidence.values():
        score = 50.0
        sources = 0
        rapid_bias = item["Rapid bias"]
        if item["Rapid events"]:
            score += 10 if rapid_bias > 0 else (-10 if rapid_bias < 0 else 0)
            sources += 1
        whale_total = item["Whale buys USD"] + item["Whale sells USD"]
        if whale_total > 0:
            score += 18 if item["Whale buys USD"] > item["Whale sells USD"] else -18
            sources += 1
        if pd.notna(item["Netflow USD"]):
            score += 15 if item["Netflow USD"] > 0 else (-15 if item["Netflow USD"] < 0 else 0)
            sources += 1
        # Do not label a single-source observation bullish or bearish.
        score = float(np.clip(score, 0, 100))
        if sources < 2:
            reading = "Insufficient independent evidence"
        elif score >= 70:
            reading = "Bullish watch — verify chart"
        elif score <= 30:
            reading = "Bearish / risk elevated"
        else:
            reading = "Mixed — monitor"
        rows.append({
            **item,
            "Evidence sources": sources,
            "Activity score": round(score, 1),
            "Reading": reading,
        })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(["Activity score", "Evidence sources"], ascending=False)


# =========================================================
# HEADER
# =========================================================
st.title("📡 Crypto Intelligence Scanner Pro")
st.caption("Broad market scan • Strict early-activity ranking • Volume expansion • Derivatives context • Risk flags")
st.caption("Build 2026-11-07.5 • Real buy-flow integrated into Pre-Pump ranking • Stablecoins excluded")
st.warning(
    "Scores are screening heuristics, not calibrated probabilities or financial advice. "
    "A high score does not guarantee a pump; low-liquidity tokens can be manipulated."
)
with st.expander("📘 Quick guide — how to read the scanner", expanded=True):
    guide_a, guide_b, guide_c = st.columns(3)
    guide_a.markdown("**1. Pre-Pump Score (0–100)**\n\nA strict evidence score combining quiet price action, turnover, market quality and optional historical volume expansion. It is **not** a pump probability.")
    guide_b.markdown("**2. Signal**\n\n`Pre-pump watch — volume confirmed` requires historical volume expansion while price remains relatively quiet. `Early activity — needs confirmation` is not yet a verified setup.")
    guide_c.markdown("**3. Risk**\n\nCheck liquidity, volume, volatility, and the project itself before drawing conclusions. Missing technical data means it has not been calculated.")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("⚙️ Scanner settings")
    data_source = st.radio("Market source", ["CoinGecko market", "Upload CSV"], index=0)
    currency = st.selectbox("Quote currency", ["usd", "eur", "gbp"], index=0)
    if data_source == "CoinGecko market":
        pages = st.selectbox(
            "Market coverage",
            options=[1, 2, 4, 8],
            format_func=lambda n: f"Up to {n * 250:,} market coins",
            index=2,
            help="Starts with up to 1,000 market coins. Reduce to 250 or 500 if CoinGecko rate limits occur.",
        )
        refresh_seconds = st.selectbox("Refresh interval", [60, 120, 300, 600], index=1)
        st_autorefresh(interval=refresh_seconds * 1000, key="scanner_refresh")
    uploaded = st.file_uploader("Upload CSV dataset", type=["csv"])
    st.divider()
    st.subheader("🔬 Technical analysis")
    use_bybit_derivatives = st.checkbox(
        "Add live funding rate + open interest (Bybit → OKX → Gate.io fallback)",
        value=True,
        help="Uses public USDT perpetual data: Bybit first, then OKX, then Gate.io if blocked. No exchange API key is used."
    )
    technical_limit = st.selectbox(
        "Coins for detailed technical indicators",
        [0, 10, 20, 30, 50],
        index=3,
        help="Fetches 7-day price and volume history for the highest turnover-to-market-cap candidates. 30 is a practical balance; 50 uses more API calls. 0 disables detailed indicators.",
    )
    run_technicals = st.button("Calculate technical indicators", type="primary")
    st.divider()
    st.subheader("📰 News")
    news_key_input = st.text_input(
        "CryptoPanic API token (optional)",
        value=secret_or_env("CRYPTOPANIC_API_KEY"),
        type="password",
        help="Set CRYPTOPANIC_API_KEY in Streamlit secrets or enter it here for this session.",
    )
    st.divider()
    st.subheader("🧪 DEX discovery")
    dex_query = st.text_input("DEX search term", value="bitcoin", help="Searches pairs matching this term; not a complete list of all DEX tokens.")
    dex_button = st.button("Search DEX Screener")
    st.divider()
    min_score = st.slider("Minimum Pre-Pump Score", 0, 100, 70)
    min_liquidity = st.number_input("Minimum DEX liquidity (USD)", min_value=0, value=50000, step=10000)
    show_all = st.checkbox("Show all rows in main table", value=True)

cg_key = secret_or_env("COINGECKO_API_KEY")
# =========================================================
# LOAD MARKET
# =========================================================
df = pd.DataFrame()
dataset_name = ""

if data_source == "CoinGecko market":
    try:
        with st.spinner("Fetching CoinGecko market pages..."):
            df = fetch_market_pages(currency, pages, cg_key)
        dataset_name = "CoinGecko market API"
    except Exception as exc:
        st.error(f"Could not fetch CoinGecko market data: {exc}")
        st.info("Check internet/API limits. You can reduce market coverage or upload a CSV instead.")
        st.stop()
else:
    if uploaded is None:
        st.info("Upload a CSV file to continue, or choose CoinGecko market in the sidebar.")
        st.stop()
    try:
        df = pd.read_csv(uploaded)
        dataset_name = uploaded.name
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        st.stop()

if df.empty:
    st.warning("No records returned.")
    st.stop()

# Normalize uploaded CSV common columns and preserve any original values.
rename_candidates = {
    "name": "Coin", "coin": "Coin",
    "symbol": "Symbol",
    "current_price": "Price", "Price_USD": "Price",
    "price_change_percentage_24h": "Change_24h_Percent",
    "change_24h_percent": "Change_24h_Percent",
    "price_change_percentage_7d_in_currency": "Change_7d_Percent",
    "change_7d_percent": "Change_7d_Percent",
    "total_volume": "Volume_24h", "Volume_24h_USD": "Volume_24h",
    "market_cap": "Market_Cap", "Market_Cap_USD": "Market_Cap",
    "id": "CoinGecko_ID",
}
rename = {}
for col in df.columns:
    key = str(col).strip()
    if key in rename_candidates and rename_candidates[key] not in df.columns:
        rename[key] = rename_candidates[key]
df = df.rename(columns=rename)

for col in ["Change_24h_Percent", "Change_7d_Percent", "Price", "Volume_24h", "Market_Cap"]:
    if col in df.columns:
        df[col] = numeric(df[col])
if "Symbol" in df.columns:
    df["Symbol"] = df["Symbol"].astype("string").str.upper()
if "Coin" not in df.columns:
    df["Coin"] = df.get("Symbol", pd.Series(["Unknown"] * len(df), index=df.index))
if "Symbol" not in df.columns:
    df["Symbol"] = df["Coin"].astype(str).str.upper()

if "Change_24h_Percent" not in df.columns:
    df["Change_24h_Percent"] = np.nan
if "Change_7d_Percent" not in df.columns:
    df["Change_7d_Percent"] = np.nan
if "Volume_24h" not in df.columns:
    df["Volume_24h"] = np.nan
if "Market_Cap" not in df.columns:
    df["Market_Cap"] = np.nan
if "Price" not in df.columns:
    df["Price"] = np.nan
if "CoinGecko_ID" not in df.columns:
    df["CoinGecko_ID"] = np.nan

if "Market_Momentum_Score" not in df.columns:
    df["Market_Momentum_Score"] = (
        50 + 1.4 * df["Change_24h_Percent"].fillna(0) +
        0.8 * df["Change_7d_Percent"].fillna(0)
    ).clip(0, 100).round(2)
if "Technical_Score" not in df.columns:
    df["Technical_Score"] = np.nan
if "News_Score" not in df.columns:
    df["News_Score"] = np.nan
if "Pump_Potential_Score" not in df.columns:
    df["Pump_Potential_Score"] = df["Market_Momentum_Score"]

# Live derivatives context: one public exchange request, cached for 90 seconds.
bybit_status = "not requested"
if data_source == "CoinGecko market" and use_bybit_derivatives:
    try:
        with st.spinner("Loading public funding-rate and open-interest snapshot..."):
            bybit_df = fetch_bybit_derivatives()
        df["Symbol"] = df["Symbol"].astype(str).str.upper()
        df = df.merge(bybit_df, on="Symbol", how="left")
        bybit_status = f"{bybit_df['Derivatives_Exchange'].dropna().iloc[0] if bybit_df['Derivatives_Exchange'].notna().any() else 'public exchange'} matched {int(df['Funding_Rate_Percent'].notna().sum())} market coins"
    except Exception as exc:
        bybit_status = f"unavailable: {str(exc)[:180]}"
        for col in ["Funding_Rate_Percent", "Open_Interest_USD", "Derivatives_Turnover_24h_USD", "Derivatives_Exchange", "Derivatives_Change_24h_Percent", "Derivatives_Pair"]:
            df[col] = np.nan

# =========================================================
# TECHNICAL INDICATORS FOR TOP-VOLUME CANDIDATES
# =========================================================
if data_source == "CoinGecko market" and technical_limit > 0 and run_technicals:
    candidates = df.copy()
    candidates["_turnover_sort"] = (
        numeric(candidates["Volume_24h"]) /
        numeric(candidates["Market_Cap"]).replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(0)
    candidates = candidates.sort_values("_turnover_sort", ascending=False).head(technical_limit)
    results = []
    progress = st.progress(0, text="Calculating indicators...")
    for i, (_, row) in enumerate(candidates.iterrows(), start=1):
        coin_id = row.get("CoinGecko_ID")
        item = {"CoinGecko_ID": coin_id}
        try:
            hist = fetch_history(str(coin_id), currency, 7, cg_key)
            item.update(technical_summary(hist["price"], hist.get("volume_24h")) if not hist.empty else technical_summary([]))
        except Exception as exc:
            item.update({"RSI_14": np.nan, "MACD": np.nan, "MACD_Signal": np.nan,
                         "Trend_7d_Percent": np.nan, "Technical_Score": np.nan,
                         "Technical_Signal": f"API unavailable: {str(exc)[:80]}",
                         "Volume_24h_vs_7d_Avg": np.nan})
        results.append(item)
        progress.progress(i / max(1, len(candidates)), text=f"Indicators {i}/{len(candidates)}")
    progress.empty()
    tech = pd.DataFrame(results).drop_duplicates("CoinGecko_ID")
    st.session_state["scanner_technical_results"] = {"currency": currency, "data": tech.copy()}
    df = df.drop(columns=[c for c in ["RSI_14", "MACD", "MACD_Signal", "Trend_7d_Percent", "Technical_Score", "Technical_Signal", "Volume_24h_vs_7d_Avg"] if c in df.columns])
    df = df.merge(tech, on="CoinGecko_ID", how="left")
    # Legacy momentum blend retained for export compatibility; final ranking is recalculated below.
    market = numeric(df["Market_Momentum_Score"])
    tech_score = numeric(df["Technical_Score"])
    df["Pump_Potential_Score"] = np.where(
        tech_score.notna(),
        0.60 * market + 0.40 * tech_score,
        market
    ).clip(0, 100).round(2)
    st.success(f"Technical indicators calculated for {tech['CoinGecko_ID'].nunique()} selected coins.")
elif (data_source == "CoinGecko market" and technical_limit > 0
      and "scanner_technical_results" in st.session_state):
    saved_tech = st.session_state["scanner_technical_results"]
    if saved_tech.get("currency") == currency:
        tech = saved_tech.get("data", pd.DataFrame())
        if not tech.empty:
            df = df.drop(columns=[c for c in ["RSI_14", "MACD", "MACD_Signal", "Trend_7d_Percent", "Technical_Score", "Technical_Signal", "Volume_24h_vs_7d_Avg"] if c in df.columns])
            df = df.merge(tech, on="CoinGecko_ID", how="left")
            market = numeric(df["Market_Momentum_Score"])
            tech_score = numeric(df["Technical_Score"])
            df["Pump_Potential_Score"] = np.where(
                tech_score.notna(), 0.60 * market + 0.40 * tech_score, market
            ).clip(0, 100).round(2)

# The primary ranking is now Pre-Pump: unusual turnover + quiet price + liquidity + optional history.
df = calculate_pre_pump_score(df)
if data_source == "CoinGecko market" and use_bybit_derivatives:
    df = add_derivatives_score(df)

# Always create this optional history column. It is absent when technical
# history has not been fetched (or when the API returns no history).
if "Volume_24h_vs_7d_Avg" not in df.columns:
    df["Volume_24h_vs_7d_Avg"] = np.nan
else:
    df["Volume_24h_vs_7d_Avg"] = numeric(df["Volume_24h_vs_7d_Avg"])

# =========================================================
# MAIN FILTERS / KPIS
# =========================================================
st.caption(
    f"Source: {dataset_name} • Rows loaded: {len(df):,} • "
    f"Display refreshed: {pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S UTC')}"
)
st.info(
    "امتیاز اولیه از فعالیت حجم، آرام بودن قیمت، نقدشوندگی و شاخص‌های تکنیکال ساخته می‌شود. "
    "اگر داده واقعی خرید/فروش CryptoMeter قبلاً دریافت شده باشد، ۳۵٪ امتیاز به غلبه خرید واقعی اختصاص می‌یابد. "
    "بدون این داده، سیگنال تأییدشده صادر نمی‌شود. حجم معاملات و Open Interest به‌تنهایی ورود پول خالص یا خرید نهنگ را ثابت نمی‌کنند."
)
if data_source == "CoinGecko market" and use_bybit_derivatives:
    if bybit_status.startswith("matched"):
        st.success(f"Public derivatives feed: {bybit_status} • cached 90 seconds")
    else:
        st.warning(f"Public derivatives feed {bybit_status}. Scanner continues without it.")
search = st.text_input("🔎 Search coin name or symbol", value="")
filtered = df.copy()
if search.strip():
    q = search.strip().lower()
    filtered = filtered[
        filtered["Coin"].astype(str).str.lower().str.contains(q, na=False) |
        filtered["Symbol"].astype(str).str.lower().str.contains(q, na=False)
    ]
if "Market_Cap_Rank" in filtered.columns:
    rank_max = st.slider("Maximum market-cap rank", 10, max(10, int(pd.to_numeric(df.get("Market_Cap_Rank", pd.Series([250])), errors="coerce").max() or 250)), value=min(250, max(10, int(pd.to_numeric(df.get("Market_Cap_Rank", pd.Series([250])), errors="coerce").max() or 250))))
    filtered = filtered[pd.to_numeric(filtered["Market_Cap_Rank"], errors="coerce").fillna(rank_max + 1) <= rank_max]
filtered = filtered[(numeric(filtered["PrePump_Score"]).fillna(0) >= min_score) & (~filtered["Is_Excluded_Asset"])]

if filtered.empty:
    st.info("No coins match these filters. Lower the minimum score or broaden your search.")
    # Do not stop: DEX and news panels may still be useful.

a, b, c, d = st.columns(4)
a.metric("🪙 Coins loaded", f"{len(df):,}")
b.metric("🔎 Matching signals", f"{len(filtered):,}")
c.metric("🟢 Positive 24h", int((numeric(df["Change_24h_Percent"]) > 0).sum()))
d.metric("📊 Median score", fmt_num(numeric(df["Pump_Potential_Score"]).median()))

e, f, g = st.columns(3)
e.metric("💰 Total 24h volume", fmt_money(numeric(df["Volume_24h"]).sum(), currency))
f.metric("🛰️ Pre-pump watch", int(df["Signal"].astype(str).str.startswith("Pre-pump watch").sum()))
g.metric("⚠️ High-risk / overheated", int(df["Risk_Level"].astype(str).str.startswith("High").sum()))

st.divider()
st.subheader("🛰️ Pre-pump candidates — before the big move")
st.caption("استیبل‌کوین‌ها حذف شده‌اند. سیگنال تأییدشده علاوه بر آرام بودن قیمت و رشد حجم تاریخی، به غلبه حجم خرید واقعی بر فروش نیاز دارد. اگر داده خرید/فروش موجود نباشد، نتیجه فقط یک سرنخ اولیه است.")
if not filtered.empty:
    if "Volume_24h_vs_7d_Avg" not in filtered.columns:
        filtered["Volume_24h_vs_7d_Avg"] = np.nan
    ranked = filtered.sort_values(["PrePump_Score", "Volume_24h_vs_7d_Avg"], ascending=[False, False], na_position="last").copy()
    confirmed = ranked[ranked["Signal"].astype(str).str.startswith("Pre-pump watch — volume confirmed")]
    early = ranked[ranked["Signal"].astype(str).str.startswith("Early activity")]
    if not confirmed.empty:
        st.markdown("**Confirmed volume-expansion setups (historical data available)**")
        top_three = confirmed.head(3)
        card_cols = st.columns(3)
        for i, (_, coin_row) in enumerate(top_three.iterrows()):
            with card_cols[i]:
                st.markdown(f"### {str(coin_row.get('Coin', 'Unknown'))} ({str(coin_row.get('Symbol', '')).upper()})")
                st.metric("Pre-Pump score", f"{fmt_num(coin_row.get('PrePump_Score'), 0)} / 100")
                change = numeric(pd.Series([coin_row.get('Change_24h_Percent')])).iloc[0]
                st.metric("24h change", f"{fmt_num(change)}%" if pd.notna(change) else "N/A")
                st.caption(f"Signal: {coin_row.get('Signal')}\n\nRisk: {coin_row.get('Risk_Level')}")
    else:
        st.info("No confirmed pre-pump setup yet. The scanner will not promote a coin without historical volume expansion.")
    if not early.empty:
        with st.expander(f"Early activity — needs confirmation ({len(early)})", expanded=True):
            early_cols = [c for c in ["Coin", "Symbol", "PrePump_Score", "Change_24h_Percent", "Change_7d_Percent", "Volume_to_Market_Cap", "Volume_24h_vs_7d_Avg", "Risk_Level"] if c in early.columns]
            st.dataframe(early[early_cols].head(20), use_container_width=True, hide_index=True)
    with st.expander("📊 Detailed candidate table", expanded=True):
        preferred_cols = [
            "Coin", "Symbol", "Price", "Change_24h_Percent", "Change_7d_Percent",
            "Volume_24h", "Volume_to_Market_Cap", "Volume_Activity_Score", "Price_Still_Quiet_Score",
            "Volume_24h_vs_7d_Avg", "Market_Cap_Rank", "RSI_14", "Technical_PrePump_Score",
            "Buy_Volume_USD", "Sell_Volume_USD", "Net_Buy_USD", "Buy_Share_Percent", "Buy_Flow_Status",
            "BTC_Market_Context", "Funding_Rate_Percent", "Open_Interest_USD", "Derivatives_Turnover_24h_USD", "Derivatives_Exchange",
            "Derivatives_Context_Score", "PrePump_Score", "Pump_Potential_Score", "Signal", "Risk_Level", "Technical_Signal",
        ]
        cols = [c for c in preferred_cols if c in ranked.columns]
        display_names = {
            "Coin": "Coin", "Symbol": "Ticker", "Price": f"Price ({currency.upper()})",
            "Change_24h_Percent": "24h change (%)", "Change_7d_Percent": "7d change (%)",
            "Volume_24h": f"24h volume ({currency.upper()})", "Market_Cap_Rank": "Market rank",
            "Volume_to_Market_Cap": "Volume / market cap", "Volume_Activity_Score": "Turnover activity",
            "Price_Still_Quiet_Score": "Price still quiet", "Volume_24h_vs_7d_Avg": "24h volume vs 7d baseline",
            "RSI_14": "RSI (14)", "Technical_PrePump_Score": "Technical pre-pump",
             "Buy_Volume_USD": "حجم خرید واقعی (USDT)", "Sell_Volume_USD": "حجم فروش واقعی (USDT)",
            "Net_Buy_USD": "خالص خرید (USDT)", "Buy_Share_Percent": "سهم خرید (%)",
            "Buy_Flow_Status": "وضعیت جریان خرید", "BTC_Market_Context": "وضعیت بازار BTC",
            "Funding_Rate_Percent": "Funding (%)", "Open_Interest_USD": "Open interest (USD)",
            "Derivatives_Turnover_24h_USD": "Perp turnover (USD)", "Derivatives_Exchange": "Derivatives source", "Derivatives_Context_Score": "Derivatives context",
            "PrePump_Score": "Pre-Pump score", "Pump_Potential_Score": "Legacy score (same value)",
            "Signal": "Signal / interpretation", "Risk_Level": "Risk flag", "Technical_Signal": "Technical reading",
        }
        display_df = ranked[cols].rename(columns=display_names)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.caption("RSI is typically interpreted from 0–100: readings above 70 can indicate an overheated move; below 30 can indicate a heavily sold market. Context matters.")
else:
    st.info("No verified early-activity candidates match these filters yet. Calculate historical indicators or lower the minimum score to inspect unconfirmed setups.")

# Alerts for sharp moves
st.subheader("🔔 Unusual market moves")
alerts = df[(numeric(df["Change_24h_Percent"]).abs() >= 5) | (numeric(df["Change_7d_Percent"]).abs() >= 15)].copy()
if not alerts.empty:
    alerts = alerts.sort_values("Change_24h_Percent", ascending=False)
    st.dataframe(alerts[["Coin", "Symbol", "Change_24h_Percent", "Change_7d_Percent", "Volume_24h", "Pump_Potential_Score", "Risk_Level"]].head(30), use_container_width=True, hide_index=True)
else:
    st.info("No moves crossed the default alert thresholds.")

# Market chart
chart_source = filtered if not filtered.empty else df.head(50)
if not chart_source.empty:
    st.subheader("🌌 Market momentum map")
    chart_source = chart_source.copy()
    chart_source["_volume_size"] = np.log10(numeric(chart_source["Volume_24h"]).fillna(0).clip(lower=0) + 1)
    fig = px.scatter(
        chart_source,
        x="Change_24h_Percent", y="Change_7d_Percent",
        size="_volume_size", color="Pump_Potential_Score",
        hover_name="Symbol", hover_data=["Coin", "Volume_24h", "Risk_Level"],
        color_continuous_scale="Turbo", template="plotly_white",
        labels={"Change_24h_Percent": "24h change (%)", "Change_7d_Percent": "7d change (%)", "Pump_Potential_Score": "Pre-Pump Score"},
    )
    fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font_color="#172b4d", height=520, xaxis=dict(gridcolor="#e5edf6"), yaxis=dict(gridcolor="#e5edf6"))
    st.plotly_chart(fig, use_container_width=True)

# Historical chart + Persian technical indicators
st.divider()
st.subheader("📈 نمودار قیمت و تحلیل تکنیکال به زبان فارسی")
st.caption("نمودارها از داده‌های تاریخی بازار ساخته می‌شوند. تفسیرها آموزشی‌اند و به‌تنهایی سیگنال قطعی خرید یا فروش نیستند.")
if data_source == "CoinGecko market" and "CoinGecko_ID" in df.columns:
    hist_candidates = df.dropna(subset=["CoinGecko_ID"]).copy()
    if not hist_candidates.empty:
        hist_candidates["_opt"] = hist_candidates["Symbol"].astype(str) + " — " + hist_candidates["Coin"].astype(str)
        choice = st.selectbox("ارز موردنظر برای تحلیل نمودار", hist_candidates["_opt"].tolist(), key="fa_chart_coin")
        selected = hist_candidates[hist_candidates["_opt"] == choice].iloc[0]
        hist_days = st.selectbox("بازه زمانی نمودار", [1, 7, 30, 90], index=1,
                                 format_func=lambda x: {1: "۱ روز اخیر", 7: "۷ روز اخیر", 30: "۳۰ روز اخیر", 90: "۹۰ روز اخیر"}[x],
                                 key="fa_chart_days")
        if st.button("نمایش نمودار و تحلیل", type="primary", key="load_fa_technical_chart"):
            try:
                hist = fetch_history(str(selected["CoinGecko_ID"]), currency, hist_days, cg_key)
                if hist.empty or len(hist) < 20:
                    st.warning("داده تاریخی کافی برای رسم همه شاخص‌ها دریافت نشد. بازه زمانی دیگری را امتحان کن.")
                else:
                    hist = hist.copy().sort_values("Time")
                    close = pd.to_numeric(hist["price"], errors="coerce")
                    delta = close.diff()
                    gain = delta.clip(lower=0).rolling(14, min_periods=14).mean()
                    loss = (-delta.clip(upper=0)).rolling(14, min_periods=14).mean()
                    rs = gain / loss.replace(0, np.nan)
                    hist["RSI"] = 100 - (100 / (1 + rs))
                    hist.loc[(loss == 0) & (gain > 0), "RSI"] = 100
                    hist.loc[(gain == 0) & (loss > 0), "RSI"] = 0
                    ema12 = close.ewm(span=12, adjust=False).mean()
                    ema26 = close.ewm(span=26, adjust=False).mean()
                    hist["MACD"] = ema12 - ema26
                    hist["MACD_Signal"] = hist["MACD"].ewm(span=9, adjust=False).mean()
                    hist["MACD_Hist"] = hist["MACD"] - hist["MACD_Signal"]
                    hist["Volume"] = pd.to_numeric(hist.get("volume_24h", pd.Series(index=hist.index, dtype=float)), errors="coerce")

                    last_price = close.iloc[-1]
                    last_rsi = hist["RSI"].iloc[-1]
                    last_macd = hist["MACD"].iloc[-1]
                    last_signal = hist["MACD_Signal"].iloc[-1]
                    if pd.isna(last_rsi):
                        rsi_text = "داده کافی برای تفسیر شاخص قدرت خرید و فروش وجود ندارد."
                        rsi_status = "داده ناکافی"
                    elif last_rsi < 30:
                        rsi_text = "فشار فروش زیاد بوده و بازار در محدوده اشباع فروش است؛ این وضعیت فقط احتمال برگشت را مطرح می‌کند و تأیید خرید نیست."
                        rsi_status = "اشباع فروش؛ منتظر تأیید برگشت"
                    elif last_rsi > 70:
                        rsi_text = "قدرت خرید بالا و بازار در محدوده اشباع خرید است؛ احتمال اصلاح یا کندشدن رشد را در نظر بگیر."
                        rsi_status = "اشباع خرید؛ احتیاط"
                    elif last_rsi >= 50:
                        rsi_text = "قدرت خریداران کمی بیشتر است و شاخص در محدوده نسبتاً مثبت قرار دارد. پایداری روند را با حجم و MACD بررسی کن."
                        rsi_status = "تمایل نسبی به خریداران"
                    else:
                        rsi_text = "قدرت فروشندگان هنوز بیشتر است؛ برای بررسی خرید بهتر است نشانه برگشت و عبور شاخص از محدوده میانی دیده شود."
                        rsi_status = "فشار فروش بیشتر"

                    if pd.isna(last_macd) or pd.isna(last_signal):
                        macd_text = "داده کافی برای تفسیر مکدی وجود ندارد."
                        macd_status = "داده ناکافی"
                    elif last_macd > last_signal:
                        macd_text = "خط مکدی بالاتر از خط سیگنال است؛ مومنتوم کوتاه‌مدت مثبت‌تر شده، اما بهتر است حجم و روند قیمت هم آن را تأیید کنند."
                        macd_status = "تقاطع/وضعیت صعودی"
                    else:
                        macd_text = "خط مکدی پایین‌تر از خط سیگنال است؛ مومنتوم هنوز ضعیف یا نزولی است و ورود عجولانه ریسک دارد."
                        macd_status = "وضعیت نزولی"

                    st.markdown(f"**{choice} — قیمت آخرین داده:** `{fmt_money(last_price)}` {currency.upper()}")
                    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.055,
                                        row_heights=[0.38, 0.16, 0.21, 0.25],
                                        subplot_titles=("قیمت", "حجم معاملات", "شاخص قدرت خرید و فروش (RSI)", "مکدی؛ قدرت و جهت حرکت (MACD)"))
                    fig.add_trace(go.Scatter(x=hist["Time"], y=close, mode="lines", name="قیمت", line=dict(color="#2878ee", width=2)), row=1, col=1)
                    if hist["Volume"].notna().any():
                        fig.add_trace(go.Bar(x=hist["Time"], y=hist["Volume"], name="حجم معاملات ۲۴ ساعته", marker_color="#9bb8df", opacity=0.72), row=2, col=1)
                    fig.add_trace(go.Scatter(x=hist["Time"], y=hist["RSI"], mode="lines", name="RSI", line=dict(color="#805ad5", width=2)), row=3, col=1)
                    fig.add_hrect(y0=70, y1=100, fillcolor="#f56565", opacity=0.09, line_width=0, row=3, col=1)
                    fig.add_hrect(y0=0, y1=30, fillcolor="#13a98f", opacity=0.10, line_width=0, row=3, col=1)
                    fig.add_hline(y=70, line_dash="dash", line_color="#d9534f", row=3, col=1)
                    fig.add_hline(y=50, line_dash="dot", line_color="#9aa9bc", row=3, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color="#13a98f", row=3, col=1)
                    hist_colors = np.where(hist["MACD_Hist"].fillna(0) >= 0, "#13a98f", "#e06b75")
                    fig.add_trace(go.Bar(x=hist["Time"], y=hist["MACD_Hist"], name="قدرت میله‌ها", marker_color=hist_colors), row=4, col=1)
                    fig.add_trace(go.Scatter(x=hist["Time"], y=hist["MACD"], mode="lines", name="خط مکدی", line=dict(color="#2878ee", width=2)), row=4, col=1)
                    fig.add_trace(go.Scatter(x=hist["Time"], y=hist["MACD_Signal"], mode="lines", name="خط سیگنال", line=dict(color="#f0a33a", width=2)), row=4, col=1)
                    fig.update_yaxes(title_text=f"قیمت ({currency.upper()})", row=1, col=1, gridcolor="#e5edf6")
                    fig.update_yaxes(title_text="حجم", row=2, col=1, gridcolor="#e5edf6")
                    fig.update_yaxes(title_text="RSI", range=[0, 100], row=3, col=1, gridcolor="#e5edf6")
                    fig.update_yaxes(title_text="مکدی", row=4, col=1, gridcolor="#e5edf6")
                    fig.update_xaxes(title_text="زمان", gridcolor="#e5edf6", row=4, col=1)
                    fig.update_layout(height=980, template="plotly_white", paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                                      font=dict(family="Arial", color="#172b4d", size=12), legend=dict(orientation="h", y=1.02, x=0),
                                      margin=dict(l=20, r=20, t=90, b=30), hovermode="x unified",
                                      title=dict(text="نقشه تکنیکال قیمت، حجم، RSI و MACD", x=0.5))
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("#### 🧭 تفسیر ساده نمودار")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**RSI — {rsi_status}**")
                        st.write(rsi_text)
                        if pd.notna(last_rsi):
                            st.metric("مقدار RSI", f"{last_rsi:.1f} از ۱۰۰")
                    with c2:
                        st.markdown(f"**MACD — {macd_status}**")
                        st.write(macd_text)
                        if pd.notna(last_macd) and pd.notna(last_signal):
                            st.metric("فاصله مکدی از خط سیگنال", f"{(last_macd-last_signal):.6g}")
                    st.info("حجم نشان می‌دهد چه مقدار معامله انجام شده، نه اینکه دقیقاً چه مقدار پول خالص وارد ارز شده است. برای تشخیص ورود پول واقعی یا فعالیت نهنگ‌ها به داده جریان سفارش یا داده آن‌چین نیاز داریم.")
                    st.caption("نکته: در بازه‌های ۱، ۷، ۳۰ و ۹۰ روزه، فاصله زمانی نقاط داده ممکن است متفاوت باشد. این نمودار بر اساس داده تاریخی دریافتی از CoinGecko رسم می‌شود و معادل کندل زنده صرافی بیت‌پین نیست.")
            except Exception as exc:
                st.error(f"خطا در دریافت یا رسم نمودار: {exc}")
else:
    st.info("برای نمایش نمودارهای تکنیکال، منبع داده CoinGecko را انتخاب کن.")

# News panel
st.divider()
st.subheader("📰 Fundamental news")
news_symbol = st.text_input("News currency code (e.g. BTC, ETH, SOL)", value="BTC").strip().upper()
if st.button("Fetch latest news"):
    with st.spinner("Fetching news..."):
        news_df, news_status = fetch_news(news_key_input, news_symbol or None)
    if news_df.empty:
        st.info(f"No news returned. {news_status}")
    else:
        # Lightweight headline sentiment proxy; never represented as a trained sentiment model.
        pos_words = ("approval", "adoption", "partnership", "launch", "upgrade", "inflow", "bullish", "listing")
        neg_words = ("hack", "exploit", "lawsuit", "ban", "delist", "outflow", "bearish", "scam", "breach")
        def headline_score(title):
            t = str(title).lower()
            return sum(w in t for w in pos_words) - sum(w in t for w in neg_words)
        news_df["Headline_Sentiment_Proxy"] = news_df["Title"].apply(headline_score).map(
            lambda x: "Positive keyword" if x > 0 else ("Negative keyword" if x < 0 else "Neutral / unclassified")
        )
        st.dataframe(news_df, use_container_width=True, hide_index=True)
        st.caption("Headline sentiment is a simple keyword proxy, not a trained NLP model or a fact-check.")

# DEX panel
st.divider()
st.subheader("🧪 DEX flows, buy/sell pressure & whale-watch clues")
st.caption("Searches DEX Screener pairs matching your query. This is a market-activity screen, not complete on-chain whale tracking.")
st.info(
    "What these numbers mean: DEX volume is traded value, not net money entering a token. "
    "Buy/sell counts are transaction counts. Estimated buy/sell volume below is only a rough proxy "
    "that splits total volume by transaction-count share; it is NOT actual USD flow. "
    "Real whale detection needs wallet-level/on-chain trade data from a suitable provider."
)
if dex_button:
    if not dex_query.strip():
        st.warning("Enter a search term.")
    else:
        try:
            with st.spinner(f"Searching DEX pairs for {dex_query}..."):
                dex_df = fetch_dex_search(dex_query.strip())
            if dex_df.empty:
                st.info("No DEX pairs found for that search term.")
            else:
                dex_df = dex_df[numeric(dex_df["Liquidity_USD"]).fillna(0) >= min_liquidity]
                if dex_df.empty:
                    st.warning("No pairs passed the minimum liquidity filter. Lower the liquidity filter and search again.")
                else:
                    top = dex_df.iloc[0]
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("DEX pairs found", f"{len(dex_df):,}")
                    k2.metric("Top pair 24h volume", f"${fmt_num(top.get('Volume_24h_USD'), 0)}")
                    k3.metric("Top pair liquidity", f"${fmt_num(top.get('Liquidity_USD'), 0)}")
                    k4.metric("Top pair buy-count share", f"{fmt_num(top.get('Buy_Count_Share_Percent'), 1)}%")
                    st.caption("Buy-count share = buys ÷ (buys + sells). It counts transactions, not their dollar size.")
                    display_cols = [
                        "Token", "Symbol", "Chain", "DEX", "Price_USD", "Change_1h_Percent",
                        "Change_24h_Percent", "Volume_24h_USD", "Liquidity_USD", "Transactions_24h",
                        "Buys_24h", "Sells_24h", "Buy_Count_Share_Percent",
                        "Estimated_Buy_Volume_Proxy_USD", "Estimated_Sell_Volume_Proxy_USD",
                        "Volume_to_Liquidity_Ratio", "Activity_Flag", "DEX_Screen_Score", "Risk_Flag", "Pair_URL"
                    ]
                    display_cols = [c for c in display_cols if c in dex_df.columns]
                    st.dataframe(dex_df[display_cols].head(100), use_container_width=True, hide_index=True)
                    st.caption(
                        "Whale-watch clue only: unusually high volume relative to liquidity plus many transactions can merit review, "
                        "but does not prove that whales traded or that net inflows occurred. Check wallet-level data separately."
                    )
                st.download_button(
                    "⬇️ Download DEX search CSV",
                    data=dex_df.to_csv(index=False).encode("utf-8"),
                    file_name="dex_screener_search.csv",
                    mime="text/csv",
                )
        except Exception as exc:
            st.error(f"DEX Screener error: {exc}")

# =========================================================
# LIVE FUNDING + OPEN INTEREST PANEL
# =========================================================
if data_source == "CoinGecko market" and use_bybit_derivatives:
    st.divider()
    st.subheader("📈 Derivatives positioning — Funding Rate & Open Interest")
    st.caption(
        "Public USDT perpetual snapshot (Bybit, with Gate.io fallback). Funding is the current periodic rate, not an annual yield. "
        "Open interest is the notional value of outstanding contracts; it is not net money entering spot markets."
    )
    deriv = df[df.get("Funding_Rate_Percent", pd.Series(np.nan, index=df.index)).notna()].copy()
    if deriv.empty:
        st.info("No matching Bybit perpetual symbols were returned for the loaded market list.")
    else:
        d1, d2, d3 = st.columns(3)
        d1.metric("Matched perpetuals", f"{len(deriv):,}")
        d2.metric("Positive funding", int((numeric(deriv["Funding_Rate_Percent"]) > 0).sum()))
        d3.metric("Negative funding", int((numeric(deriv["Funding_Rate_Percent"]) < 0).sum()))
        deriv_view = deriv.sort_values("Derivatives_Context_Score", ascending=False)
        deriv_cols = [c for c in ["Coin", "Symbol", "Funding_Rate_Percent", "Open_Interest_USD", "Derivatives_Turnover_24h_USD", "Derivatives_Exchange", "Derivatives_Change_24h_Percent", "Derivatives_Context_Score", "PrePump_Score", "Signal"] if c in deriv_view.columns]
        st.dataframe(deriv_view[deriv_cols].head(60), use_container_width=True, hide_index=True)
        st.caption("Interpretation: very positive funding can indicate crowded longs; negative funding can indicate crowded shorts. Combine with price, volume and OI changes—one snapshot alone cannot confirm a squeeze or a pump.")


# =========================================================
# CRYPTOMETER INTELLIGENCE PANEL
# =========================================================
st.divider()
st.subheader("🧭 CryptoMeter intelligence — whale activity, flows & rapid moves")
st.caption(
    "CryptoMeter feeds add market evidence to the CoinGecko scanner. A signal is a research watchlist, "
    "not a guaranteed pump prediction or an instruction to buy."
)
cm_key = secret_or_env("CRYPTOMETER_API_KEY")
if not cm_key:
    st.warning("CryptoMeter API key not found. Add CRYPTOMETER_API_KEY in Render → Environment, then save and redeploy.")
else:
    cm_a, cm_b, cm_c = st.columns(3)
    with cm_a:
        cm_symbol_filter = st.text_input(
            "Whale / funding symbol filter (optional)", value="", key="cm_symbol_filter",
            help="Leave blank to request the latest market-wide records where the endpoint supports it."
        ).strip().lower()
    with cm_b:
        cm_timeframe = st.selectbox("Flow timeframe", ["15m", "1h", "4h", "d"], index=2, key="cm_flow_timeframe")
    with cm_c:
        cm_mover_timeframe = st.selectbox("Gainers/losers timeframe", ["5m", "15m", "1h", "1d", "1w"], index=2, key="cm_mover_timeframe")

    st.markdown("**Free feeds** — account status, market trend pressure and the Rapid Movements feed.")
    st.caption("The Rapid Movements endpoint is the original 4-hour movement feed. The richer Rapid Movements V2 feed is a paid endpoint.")

    paid_options = {
        "Whale trades (xtrades) — paid": "whales",
        "Volume flow — paid": "volume_flow",
        "Liquidity Lens / netflow — paid": "liquidity",
        "Funding rates — paid": "funding",
        "Gainers & losers — paid": "movers",
    }
    paid_selected_labels = st.multiselect(
        "Optional paid feeds (select only endpoints included in your CryptoMeter plan)",
        options=list(paid_options.keys()),
        default=[],
        help="Do not select these unless you have enabled/purchased the corresponding endpoint in CryptoMeter Manage API."
    )
    st.info(
        "Whale trades, Volume Flow, Liquidity Lens, Funding Rates and Gainers/Losers are marked Paid in CryptoMeter's API documentation. "
        "If your plan does not include an endpoint, leave it unselected."
    )

    if st.button("🔄 Fetch CryptoMeter intelligence", type="primary", key="cm_fetch_button"):
        endpoint_jobs = {
            "account": ("info", {}),
            "trend": ("trend-indicator-v3", {}),
            "rapid": ("rapid-movements", {}),
        }
        for label in paid_selected_labels:
            result_key = paid_options[label]
            if result_key == "whales":
                params = {"symbol": cm_symbol_filter} if cm_symbol_filter else {}
                endpoint_jobs[result_key] = ("xtrades", params)
            elif result_key == "volume_flow":
                endpoint_jobs[result_key] = ("volume-flow", {"timeframe": cm_timeframe})
            elif result_key == "liquidity":
                endpoint_jobs[result_key] = ("liquidity-lens", {"timeframe": cm_timeframe})
            elif result_key == "funding":
                params = {"symbol": cm_symbol_filter} if cm_symbol_filter else {}
                endpoint_jobs[result_key] = ("funding-rates", params)
            elif result_key == "movers":
                endpoint_jobs[result_key] = ("gainers-losers", {"timeframe": cm_mover_timeframe})

        collected = {}
        with st.spinner("Requesting selected CryptoMeter feeds..."):
            for result_key, (endpoint, params) in endpoint_jobs.items():
                try:
                    collected[result_key] = {
                        "payload": fetch_cryptometer(endpoint, params, cm_key),
                        "error": None,
                        "endpoint": endpoint,
                    }
                except Exception as exc:
                    collected[result_key] = {
                        "payload": None,
                        "error": str(exc),
                        "endpoint": endpoint,
                    }
        st.session_state["cryptometer_results"] = collected
        st.session_state["cryptometer_last_fetch"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M:%S UTC")

    cm_results = st.session_state.get("cryptometer_results", {})
    if cm_results:
        st.caption(f"Last requested: {st.session_state.get('cryptometer_last_fetch', 'unknown')} • Responses are cached for 5 minutes.")
        errors = [(key, value) for key, value in cm_results.items() if value.get("error")]
        if errors:
            with st.expander("⚠️ Feed access / API errors", expanded=True):
                for key, value in errors:
                    st.warning(f"{value.get('endpoint', key)}: {value['error']}")

        account_result = cm_results.get("account", {})
        if account_result.get("payload"):
            account_df = cryptometer_frame(account_result["payload"])
            if not account_df.empty:
                account = account_df.iloc[0]
                q1, q2, q3, q4 = st.columns(4)
                q1.metric("CryptoMeter plan", str(account.get("plan", "N/A")))
                q2.metric("API status", str(account.get("status", "N/A")))
                q3.metric("Monthly quota", fmt_num(account.get("quota"), 0))
                q4.metric("Requests used", fmt_num(account.get("total_requests"), 0))
                extras = account.get("extra_endpoints")
                if isinstance(extras, list) and extras:
                    st.caption("Additional enabled endpoints reported by account: " + ", ".join(map(str, extras)))

        trend_result = cm_results.get("trend", {})
        if trend_result.get("payload"):
            trend_df = cryptometer_frame(trend_result["payload"])
            if not trend_df.empty:
                trend = trend_df.iloc[-1]
                st.markdown("**Market-wide trend pressure**")
                t1, t2, t3 = st.columns(3)
                t1.metric("Trend score", fmt_num(trend.get("trend_score")))
                t2.metric("Buy pressure", f"{fmt_num(trend.get('buy_pressure'))}%")
                t3.metric("Sell pressure", f"{fmt_num(trend.get('sell_pressure'))}%")
                if trend.get("timestamp"):
                    st.caption(f"Provider timestamp: {trend.get('timestamp')}. Treat this as broad market context, not a coin-specific signal.")

        rapid_result = cm_results.get("rapid", {})
        if rapid_result.get("payload"):
            rapid_df = cryptometer_frame(rapid_result["payload"])
            st.markdown("**Rapid Movements — last four hours**")
            if rapid_df.empty:
                st.info("No rapid-movement records were returned.")
            else:
                show_cols = [c for c in ["pair", "exchange", "change_detected", "side", "timestamp"] if c in rapid_df.columns]
                st.dataframe(rapid_df[show_cols] if show_cols else rapid_df, use_container_width=True, hide_index=True)

        whale_result = cm_results.get("whales", {})
        if whale_result.get("payload"):
            whale_df = cryptometer_frame(whale_result["payload"])
            st.markdown("**Whale trades**")
            if whale_df.empty:
                st.info("No whale-trade rows were returned.")
            else:
                if "usd_total" not in whale_df.columns and "total" in whale_df.columns:
                    whale_df["usd_total"] = whale_df["total"]
                whale_cols = [c for c in ["timestamp", "symbol", "pair", "exchange", "side", "price", "size", "usd_total"] if c in whale_df.columns]
                st.dataframe(whale_df[whale_cols] if whale_cols else whale_df, use_container_width=True, hide_index=True)

        volume_result = cm_results.get("volume_flow", {})
        if volume_result.get("payload"):
            flow_data = cryptometer_data(volume_result["payload"])
            st.markdown("**Volume Flow**")
            if isinstance(flow_data, dict):
                flow_tabs = st.tabs(["Inflow", "Outflow", "Netflow"])
                for tab, flow_name in zip(flow_tabs, ["inflow", "outflow", "netflow"]):
                    with tab:
                        flow_rows = flow_data.get(flow_name, [])
                        flow_frame = pd.DataFrame(flow_rows if isinstance(flow_rows, list) else [])
                        if flow_frame.empty:
                            st.info(f"No {flow_name} rows returned.")
                        else:
                            st.dataframe(flow_frame, use_container_width=True, hide_index=True)
            else:
                st.json(flow_data)

        # ---------------------------------------------------------
        # ACTUAL PROVIDER BUY/SELL TRADED VOLUME (NOT TXN-COUNT PROXY)
        # ---------------------------------------------------------
        st.markdown("**خرید و فروش واقعی ثبت‌شده در صرافی (۲۴ ساعت)**")
        st.caption(
            "این بخش از endpoint اختصاصی 24h-trade-volume-v2 استفاده می‌کند؛ "
            "حجم خرید و فروش را از داده صرافی می‌گیرد، نه از نسبت تعداد معاملات. "
            "این داده فقط برای جفت و صرافی انتخاب‌شده است و به‌تنهایی ورود نهنگ یا خرید کیف‌پول خاص را ثابت نمی‌کند."
        )
        cm_symbols = []
        if "Symbol" in df.columns:
            cm_symbols = [str(x).upper() for x in df["Symbol"].dropna().unique() if str(x).strip()]
        if not cm_symbols:
            cm_symbols = ["BTC", "ETH", "SOL"]
        ranked_symbols = []
        if "PrePump_Score" in df.columns and "Symbol" in df.columns:
            ranked_symbols = (
                df.assign(_cm_rank=numeric(df["PrePump_Score"]))
                  .sort_values("_cm_rank", ascending=False)["Symbol"]
                  .dropna().astype(str).str.upper().drop_duplicates().head(5).tolist()
            )
        default_symbols = [x for x in ranked_symbols if x in cm_symbols][:5] or cm_symbols[:5]
        buy_col1, buy_col2 = st.columns([2, 1])
        with buy_col1:
            selected_buy_symbols = st.multiselect(
                "ارزها برای بررسی حجم خرید/فروش", options=cm_symbols, default=default_symbols,
                max_selections=10, key="cm_actual_buy_symbols"
            )
        with buy_col2:
            buy_exchange = st.selectbox(
                "صرافی مرجع", ["binance", "bybit_spot", "okx", "kucoin", "coinbase_pro", "kraken"],
                index=0, key="cm_actual_buy_exchange"
            )
        if st.button("محاسبه حجم واقعی خرید و فروش", key="cm_actual_buy_fetch", type="primary"):
            if not selected_buy_symbols:
                st.warning("حداقل یک ارز انتخاب کن.")
            else:
                actual_rows = []
                with st.spinner("در حال دریافت حجم خرید و فروش از صرافی..."):
                    for symbol in selected_buy_symbols:
                        try:
                            actual_rows.append(fetch_cryptometer_buy_sell_volume(symbol, buy_exchange, cm_key))
                        except Exception as exc:
                            actual_rows.append({
                                "Symbol": symbol, "Pair": f"{symbol}-USDT", "Exchange": buy_exchange,
                                "Buy volume (USDT)": np.nan, "Sell volume (USDT)": np.nan,
                                "Net buy (USDT)": np.nan, "Buy share (%)": np.nan,
                                "Data status": str(exc)[:140]
                            })
                        time.sleep(0.16)
                st.session_state["cm_actual_buy_sell_rows"] = actual_rows
                st.session_state["cm_actual_buy_sell_time"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M:%S UTC")
        actual_rows = st.session_state.get("cm_actual_buy_sell_rows", [])
        if actual_rows:
            actual_df = pd.DataFrame(actual_rows)
            st.caption("آخرین دریافت: " + str(st.session_state.get("cm_actual_buy_sell_time", "نامشخص")))
            valid_actual = actual_df.dropna(subset=["Buy volume (USDT)", "Sell volume (USDT)"])
            if valid_actual.empty:
                st.warning("برای ارزهای انتخاب‌شده داده خرید/فروش برنگشت. ممکن است جفت USDT در صرافی یا دسترسی این endpoint در پلن شما موجود نباشد؛ عدد صفر فرض نمی‌شود.")
            else:
                show_actual = actual_df.copy()
                for col in ["Buy volume (USDT)", "Sell volume (USDT)", "Net buy (USDT)"]:
                    show_actual[col] = show_actual[col].map(lambda v: fmt_num(v, 0) if pd.notna(v) else "—")
                show_actual["Buy share (%)"] = show_actual["Buy share (%)"].map(lambda v: f"{v:.1f}%" if pd.notna(v) else "—")
                show_actual = show_actual.rename(columns={
                    "Symbol": "ارز", "Pair": "جفت", "Exchange": "صرافی",
                    "Buy volume (USDT)": "حجم خرید (USDT)",
                    "Sell volume (USDT)": "حجم فروش (USDT)",
                    "Net buy (USDT)": "خالص خرید (USDT)",
                    "Buy share (%)": "سهم خرید", "Data status": "وضعیت داده"
                })
                st.dataframe(show_actual, width="stretch", hide_index=True)
                st.caption("خالص خرید مثبت یعنی حجم خرید ثبت‌شده از فروش بیشتر بوده است. برای تأیید سیگنال، روند قیمت، نقدشوندگی و چند بازه زمانی را هم بررسی کن.")

        liquidity_result = cm_results.get("liquidity", {})
        if liquidity_result.get("payload"):
            liquidity_data = cryptometer_data(liquidity_result["payload"])
            st.markdown("**Liquidity Lens — coin-level netflow**")
            if isinstance(liquidity_data, dict):
                liquidity_df = pd.DataFrame([
                    {"Symbol": symbol, **values}
                    for symbol, values in liquidity_data.items() if isinstance(values, dict)
                ])
            elif isinstance(liquidity_data, list):
                liquidity_df = pd.DataFrame(liquidity_data)
            else:
                liquidity_df = pd.DataFrame()
            if liquidity_df.empty:
                st.info("No liquidity-lens rows were returned.")
            else:
                if "netflow" in liquidity_df.columns:
                    liquidity_df = liquidity_df.sort_values("netflow", ascending=False)
                st.dataframe(liquidity_df, use_container_width=True, hide_index=True)

        funding_result = cm_results.get("funding", {})
        if funding_result.get("payload"):
            funding_df = cryptometer_frame(funding_result["payload"])
            st.markdown("**Funding rates**")
            if funding_df.empty:
                st.info("No funding-rate rows were returned.")
            else:
                funding_cols = [c for c in ["symbol", "pair", "exchange", "rate_percent", "annualized_percent", "interval_hours", "next_funding_at"] if c in funding_df.columns]
                st.dataframe(funding_df[funding_cols] if funding_cols else funding_df, use_container_width=True, hide_index=True)

        movers_result = cm_results.get("movers", {})
        if movers_result.get("payload"):
            movers_data = cryptometer_data(movers_result["payload"])
            st.markdown("**Gainers & losers**")
            if isinstance(movers_data, dict):
                mover_tabs = st.tabs(["Gainers", "Losers"])
                for tab, side_name in zip(mover_tabs, ["gainers", "losers"]):
                    with tab:
                        side_df = pd.DataFrame(movers_data.get(side_name, []))
                        if side_df.empty:
                            st.info(f"No {side_name} rows returned.")
                        else:
                            st.dataframe(side_df, use_container_width=True, hide_index=True)
            else:
                st.json(movers_data)

        watchlist_df = cryptometer_watchlist(cm_results)
        if not watchlist_df.empty:
            st.markdown("**Cross-signal activity watchlist**")
            st.caption(
                "Transparent evidence score: Rapid Moves (+/−10), whale buy/sell USD dominance (+/−18), "
                "and coin-level netflow (+/−15). A bullish/bearish label requires at least two independent evidence sources. "
                "This score is not a calibrated probability and is not a buy recommendation."
            )
            st.dataframe(watchlist_df, use_container_width=True, hide_index=True)
            st.download_button(
                "⬇️ Download CryptoMeter watchlist CSV",
                data=watchlist_df.to_csv(index=False).encode("utf-8"),
                file_name="cryptometer_activity_watchlist.csv",
                mime="text/csv",
                key="cm_watchlist_download",
            )
    else:
        st.info("Click 'Fetch CryptoMeter intelligence' to request the free feeds. Paid feeds remain off until you select them above.")


# Full data export
st.divider()
with st.expander("📋 Advanced view — full market dataset", expanded=False):
    st.caption("This table contains the raw columns used by the scanner. Most users can work from the candidate table above.")
    if show_all:
        st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download full market CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="crypto_intelligence_scanner_export.csv",
        mime="text/csv",
    )

st.caption(
    "Data coverage depends on the connected APIs and their limits. "
    "CoinGecko market pages cover listed market assets; DEX search is query-based. "
    "CryptoMeter paid feeds require endpoint access in your plan. This tool is informational only, not financial advice."
)
