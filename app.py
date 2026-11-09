import os
import time
import threading
import re
import html
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.adapters import HTTPAdapter
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
  --bg: #f4f7fb;
  --panel: #ffffff;
  --panel-soft: #eaf1fa;
  --border: #cbd8e8;
  --text: #14243b;
  --muted: #465b75;
  --blue: #1769d2;
  --teal: #087f6b;
}
.stApp { background: #f4f7fb !important; color: #14243b !important; }
[data-testid="stHeader"] { background: rgba(244,247,251,.98) !important; }
[data-testid="stSidebar"] { background: #eaf1fa !important; border-right: 1px solid #cbd8e8; }
[data-testid="stSidebar"] * { color: #14243b !important; }
.block-container { width: 100%; max-width: 1600px; padding: 1.1rem 1.35rem 2.4rem; }
h1,h2,h3,h4 { color: #102846 !important; font-weight: 800 !important; line-height: 1.35 !important; }
h1 { font-size: 1.9rem !important; }
h2 { font-size: 1.48rem !important; }
h3 { font-size: 1.18rem !important; }
h4 { font-size: 1.04rem !important; }
.stMarkdown, [data-testid="stMarkdownContainer"] { color: #14243b !important; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
[data-testid="stWidgetLabel"], label, .stText, .stMarkdown p {
  color: #243a55 !important; font-size: .96rem !important; line-height: 1.65 !important;
}
[data-testid="stCaptionContainer"], .stCaption, [data-testid="stCaptionContainer"] * {
  color: #465b75 !important; font-size: .88rem !important; line-height: 1.6 !important;
}
[data-testid="stMetric"] { background: #fff !important; border: 1px solid #cbd8e8 !important;
  padding: 14px 16px !important; border-radius: 14px !important; box-shadow: 0 3px 12px rgba(25,55,90,.07); }
[data-testid="stMetric"] label { color: #344c68 !important; font-weight: 700 !important; }
[data-testid="stMetricValue"] { color: #102846 !important; font-size: 1.5rem !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-weight: 700 !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] { background: #fff !important; border: 1px solid #cbd8e8 !important; border-radius: 12px !important; overflow: hidden; }
[data-testid="stDataFrame"] * { font-size: 13px !important; }
[data-testid="stExpander"] { background: #fff !important; border: 1px solid #cbd8e8 !important; border-radius: 12px !important; overflow: hidden; }
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span { color: #102846 !important; background: #eaf1fa !important;
  font-size: .98rem !important; font-weight: 800 !important; }
[data-testid="stExpander"] details, [data-testid="stExpander"] > details > div { background: #fff !important; color: #14243b !important; }
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] button {
  min-height: 2.65rem; padding: .55rem 1rem; font-size: .94rem !important; border-radius: 10px;
  border: 1px solid #1769d2; font-weight: 750; background: #1769d2; color: #fff !important; }
.stButton > button:hover, .stDownloadButton > button:hover { background: #0e55b4; border-color: #087f6b; box-shadow: 0 0 0 3px rgba(8,127,107,.13); }
/* Dedicated high-visibility styling for the CryptoMeter fetch action. */
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
  background: linear-gradient(135deg, #087f6b 0%, #06a58b 100%) !important;
  border: 1px solid #087f6b !important; color: #ffffff !important;
  font-weight: 800 !important; box-shadow: 0 3px 10px rgba(8,127,107,.20);
}
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button:hover,
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button:focus-visible {
  background: linear-gradient(135deg, #066957 0%, #078b77 100%) !important;
  border-color: #055b4c !important; color: #ffffff !important;
  box-shadow: 0 0 0 3px rgba(8,127,107,.20);
}
[data-testid="stForm"] [data-testid="stFormSubmitButton"] button:active {
  transform: translateY(1px); filter: brightness(.96);
}
input, textarea, [data-baseweb="select"] > div { background: #fff !important; color: #14243b !important;
  border: 1px solid #b9c9dc !important; border-radius: 10px !important; font-size: .96rem !important; min-height: 2.65rem; }
input::placeholder, textarea::placeholder { color: #60748d !important; opacity: 1 !important; }
[data-testid="stSlider"] [data-testid="stWidgetLabel"] { color: #243a55 !important; font-weight: 750 !important; }
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label { color: #243a55 !important; }
/* Icon navigation: clear selected state and touch-friendly targets. */
div[data-testid="stRadio"] > div[role="radiogroup"] { gap: .45rem; flex-wrap: wrap; }
 div[data-testid="stRadio"] > div[role="radiogroup"] label { background: #fff !important; border: 1px solid #c5d3e3 !important;
  border-radius: 12px !important; padding: .5rem .85rem !important; min-height: 2.8rem; }
div[data-testid="stRadio"] > div[role="radiogroup"] label:has(input:checked) { background: #dceaff !important;
  border: 1.5px solid #1769d2 !important; box-shadow: 0 2px 8px rgba(23,105,210,.12); }
div[data-testid="stRadio"] > div[role="radiogroup"] label p { color: #173653 !important; font-weight: 750 !important; }
[data-testid="stAlert"] { border-radius: 11px !important; font-size: .94rem !important; }
[data-testid="stAlert"] p { color: #18334f !important; }
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #1769d2, #087f6b); }
hr { border-color: #d6e0ec !important; margin: .9rem 0 !important; }
a { color: #075fbd !important; font-weight: 650; }
small, .stMarkdown small { color: #465b75 !important; font-size: .86rem !important; }
[data-testid="stVerticalBlock"] { gap: .8rem; }
[data-testid="stHorizontalBlock"] { gap: .85rem; }
@media (max-width: 768px) {
  /* CryptoMeter touch-submit sizing */
  div[data-testid="stFormSubmitButton"] button { width: 100% !important; min-height: 3.2rem !important; touch-action: manipulation; }

  .block-container { padding: .85rem .65rem 1.8rem; }
  h1 { font-size: 1.45rem !important; }
  h2 { font-size: 1.2rem !important; }
  h3 { font-size: 1.05rem !important; }
  [data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] { font-size: .92rem !important; }
  [data-testid="stMetric"] { padding: 10px 11px !important; border-radius: 11px !important; }
  [data-testid="stMetricValue"] { font-size: 1.18rem !important; }
  .stButton > button, .stDownloadButton > button,
  div[data-testid="stButton"] > button,
  div[data-testid="stFormSubmitButton"] > button {
    width: 100% !important; min-height: 3.15rem !important;
    touch-action: manipulation !important; pointer-events: auto !important;
    position: relative; z-index: 2; cursor: pointer;
  }
  input, textarea, [data-baseweb="select"] > div { min-height: 2.85rem; }
  [data-testid="stDataFrame"] { overflow-x: auto; }
  div[data-testid="stRadio"] > div[role="radiogroup"] { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); }
  div[data-testid="stRadio"] > div[role="radiogroup"] label { justify-content: center; }
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


# Reuse HTTP connections per worker thread. Thread-local sessions avoid sharing
# mutable requests.Session state between concurrent Streamlit fetch workers.
_HTTP_LOCAL = threading.local()
_HTTP_RETRY_STATUSES = {429, 500, 502, 503, 504}


def _http_session():
    session = getattr(_HTTP_LOCAL, "session", None)
    if session is None:
        session = requests.Session()
        adapter = HTTPAdapter(pool_connections=12, pool_maxsize=12, max_retries=0)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"User-Agent": "CryptoIntelligenceScanner/2026.11"})
        _HTTP_LOCAL.session = session
    return session


def _retry_delay(response, attempt):
    retry_after = response.headers.get("Retry-After") if response is not None else None
    if retry_after:
        try:
            return min(8.0, max(0.25, float(retry_after)))
        except (TypeError, ValueError):
            pass
    return min(4.0, 0.35 * (2 ** attempt))


def safe_get(url, *, params=None, headers=None, timeout=20):
    """GET with connection reuse and bounded retry for transient/rate-limit errors."""
    last_error = None
    for attempt in range(3):
        response = None
        try:
            response = _http_session().get(
                url, params=params, headers=headers, timeout=timeout
            )
            if response.status_code in _HTTP_RETRY_STATUSES and attempt < 2:
                time.sleep(_retry_delay(response, attempt))
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
            if attempt >= 2:
                raise
            time.sleep(_retry_delay(response, attempt))
        except ValueError:
            # Invalid JSON is a data/provider error, not a transient transport error.
            raise
    if last_error:
        raise last_error
    raise RuntimeError("HTTP request failed without a response")


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
                "Technical_Signal": "Insufficient history",
                "Volume_24h_vs_7d_Avg": np.nan,
                "Price_Range_7d_Percent": np.nan,
                "Price_Range_Last24h_Percent": np.nan,
                "Range_Compression_Ratio": np.nan,
                "Higher_Low_24h_Percent": np.nan,
                "Accumulation_Price_Score": np.nan}
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
        # CoinGecko total_volumes is a rolling 24h snapshot, not hourly traded volume.
        if len(v) >= 48:
            recent_volume = v.tail(24).median()
            baseline_volume = v.iloc[:-24].median()
            if pd.notna(baseline_volume) and baseline_volume > 0:
                volume_ratio = float(recent_volume / baseline_volume)

    # Accumulation structure proxy: compare the latest ~24 samples with the
    # preceding ~24 samples. It is not wallet-level accumulation evidence.
    range_7d_pct = range_24h_pct = compression_ratio = higher_low_pct = np.nan
    compression_score = higher_low_score = np.nan
    if len(p) >= 48:
        recent = p.tail(24)
        previous = p.iloc[-48:-24]
        median_7d = float(p.median())
        median_recent = float(recent.median())
        if median_7d > 0 and median_recent > 0:
            range_7d_pct = float((p.max() - p.min()) / median_7d * 100)
            range_24h_pct = float((recent.max() - recent.min()) / median_recent * 100)
            if range_7d_pct > 0:
                compression_ratio = range_24h_pct / range_7d_pct
                compression_score = (100 if compression_ratio <= 0.35 else
                                     80 if compression_ratio <= 0.50 else
                                     60 if compression_ratio <= 0.70 else
                                     40 if compression_ratio <= 0.90 else 20)
        previous_low = float(previous.min())
        recent_low = float(recent.min())
        if previous_low > 0:
            higher_low_pct = (recent_low / previous_low - 1) * 100
            higher_low_score = (100 if higher_low_pct >= 1.0 else
                                80 if higher_low_pct >= 0.3 else
                                60 if higher_low_pct >= 0 else
                                30 if higher_low_pct >= -0.5 else 0)

    rsi_structure_score = np.nan
    if pd.notna(latest_rsi):
        rsi_structure_score = (100 if 45 <= latest_rsi <= 60 else
                               80 if 40 <= latest_rsi <= 65 else
                               55 if 35 <= latest_rsi <= 70 else 20)
    price_parts = [(compression_score, 0.45), (higher_low_score, 0.35), (rsi_structure_score, 0.20)]
    price_weight = sum(weight for value, weight in price_parts if pd.notna(value))
    accumulation_price_score = (sum(value * weight for value, weight in price_parts if pd.notna(value)) / price_weight
                                if price_weight > 0 else np.nan)

    return {
        "RSI_14": round(float(latest_rsi), 2) if pd.notna(latest_rsi) else np.nan,
        "MACD": round(float(macd.iloc[-1]), 8),
        "MACD_Signal": round(float(signal.iloc[-1]), 8),
        "Trend_7d_Percent": round(float(trend), 2) if pd.notna(trend) else np.nan,
        "Technical_Score": round(score, 2),
        "Technical_Signal": signal_text,
        "Volume_24h_vs_7d_Avg": round(volume_ratio, 3) if pd.notna(volume_ratio) else np.nan,
        "Price_Range_7d_Percent": round(range_7d_pct, 3) if pd.notna(range_7d_pct) else np.nan,
        "Price_Range_Last24h_Percent": round(range_24h_pct, 3) if pd.notna(range_24h_pct) else np.nan,
        "Range_Compression_Ratio": round(compression_ratio, 3) if pd.notna(compression_ratio) else np.nan,
        "Higher_Low_24h_Percent": round(higher_low_pct, 3) if pd.notna(higher_low_pct) else np.nan,
        "Accumulation_Price_Score": round(accumulation_price_score, 1) if pd.notna(accumulation_price_score) else np.nan,
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
    # A ticker alone is not a unique asset identifier. Mark collisions so a
    # provider's symbol-only flow cannot be assigned to the wrong token.
    symbols = out.get("Symbol", pd.Series("", index=out.index)).astype(str).str.upper().str.strip()
    collision_counts = symbols[symbols.ne("")].value_counts()
    out["Symbol_Ambiguous"] = symbols.map(collision_counts).fillna(0).gt(1)
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
    out = out.merge(flow[["Symbol", "Buy_Volume_USD", "Sell_Volume_USD", "Net_Buy_USD", "Buy_Share_Percent"]],
                    on="Symbol", how="left")
    # Never present symbol-only flow as confirmed for colliding tickers.
    ambiguous = out["Symbol_Ambiguous"].fillna(False)
    flow_columns = ["Buy_Volume_USD", "Sell_Volume_USD", "Net_Buy_USD", "Buy_Share_Percent"]
    out.loc[ambiguous, flow_columns] = np.nan
    return out


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
    """Conservative seven-factor early-activity score; missing evidence is not bullish."""
    out = mark_stablecoins(frame)
    out = attach_actual_buy_sell_flow(out)
    ch24 = numeric(out.get("Change_24h_Percent", pd.Series(np.nan, index=out.index)))
    ch7 = numeric(out.get("Change_7d_Percent", pd.Series(np.nan, index=out.index)))
    volume = numeric(out.get("Volume_24h", pd.Series(np.nan, index=out.index)))
    market_cap = numeric(out.get("Market_Cap", pd.Series(np.nan, index=out.index)))
    turnover = (volume / market_cap.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
    out["Volume_to_Market_Cap"] = turnover
    eligible = ~out["Is_Excluded_Asset"]
    symbol_ambiguous = out.get("Symbol_Ambiguous", pd.Series(False, index=out.index)).fillna(False).astype(bool)
    out["Data_Quality_Status"] = np.where(
        symbol_ambiguous,
        "نماد تکراری است؛ تطبیق قرارداد لازم است",
        "تطبیق نماد بدون برخورد تکراری"
    )

    # 1) REAL reported buy/sell traded volume (30%). Never infer it from trade counts.
    buy_share = numeric(out.get("Buy_Share_Percent", pd.Series(np.nan, index=out.index)))
    net_buy = numeric(out.get("Net_Buy_USD", pd.Series(np.nan, index=out.index)))
    flow_available = buy_share.notna() & net_buy.notna()
    flow_score = ((buy_share - 50) * 4 + 50).clip(0, 100)
    rsi_value = numeric(out.get("RSI_14", pd.Series(np.nan, index=out.index)))
    out["Buy_Flow_Score"] = flow_score.where(flow_available, np.nan)
    out["Buy_Flow_Status"] = np.select(
        [~flow_available, (net_buy > 0) & (buy_share >= 55), (net_buy > 0) & (buy_share > 50), net_buy < 0],
        ["حجم خرید/فروش واقعی دریافت نشده", "غلبه خرید واقعی", "خرید کمی بیشتر از فروش", "غلبه فروش واقعی"],
        default="خرید و فروش تقریباً متعادل"
    )

    # 2) Volume acceleration vs the coin's own 7-day baseline (20%).
    surge = numeric(out.get("Volume_24h_vs_7d_Avg", pd.Series(np.nan, index=out.index)))
    surge_score = pd.Series(np.select(
        [surge >= 3, surge >= 2, surge >= 1.5, surge >= 1.2, surge >= 1.0],
        [100, 85, 75, 60, 45], default=15
    ), index=out.index, dtype=float).where(surge.notna(), np.nan)
    out["Volume_Acceleration_Score"] = surge_score

    # Independent accumulation screen. This is kept separate from PrePump_Score
    # so the existing seven-factor ranking remains comparable across versions.
    price_structure = numeric(out.get("Accumulation_Price_Score", pd.Series(np.nan, index=out.index)))
    flow_accumulation = flow_score.where(flow_available & (net_buy > 0), np.nan)
    volume_accumulation = pd.Series(np.select(
        [surge >= 2.0, surge >= 1.5, surge >= 1.2, surge >= 1.0],
        [100, 85, 70, 50], default=20
    ), index=out.index, dtype=float).where(surge.notna(), np.nan)
    rsi_accumulation = pd.Series(np.select(
        [rsi_value.between(45, 60), rsi_value.between(40, 65), rsi_value.between(35, 70)],
        [100, 80, 55], default=20
    ), index=out.index, dtype=float).where(rsi_value.notna(), np.nan)
    # Weights: price structure 35, real net buying 35, volume expansion 20, RSI 10.
    accumulation_parts = {
        "Accumulation_Price_Score": (price_structure, 35.0),
        "Accumulation_Flow_Score": (flow_accumulation, 35.0),
        "Accumulation_Volume_Score": (volume_accumulation, 20.0),
        "Accumulation_RSI_Score": (rsi_accumulation, 10.0),
    }
    accum_sum = pd.Series(0.0, index=out.index)
    accum_weight = pd.Series(0.0, index=out.index)
    for col, (values, weight) in accumulation_parts.items():
        out[col] = values
        accum_sum += values.fillna(0) * weight
        accum_weight += values.notna().astype(float) * weight
    out["Accumulation_Data_Coverage"] = accum_weight
    out["Accumulation_Score"] = (accum_sum / accum_weight.replace(0, np.nan)).round(1)
    positive_flow_for_accum = flow_available & (net_buy > 0) & (buy_share >= 52)
    compressed_structure = numeric(out.get("Range_Compression_Ratio", pd.Series(np.nan, index=out.index))).le(0.70)
    healthy_rsi = rsi_value.between(40, 65)
    not_hot = (ch24 < 8) & (ch7 < 20)
    out["Accumulation_Status"] = np.select(
        [out["Accumulation_Score"].isna(),
         (out["Accumulation_Score"] >= 75) & positive_flow_for_accum & compressed_structure & healthy_rsi & (surge >= 1.1) & not_hot & (market_cap >= 10_000_000) & (volume >= 300_000),
         (out["Accumulation_Score"] >= 60) & compressed_structure & ~flow_available],
        ["داده کافی برای ارزیابی انباشت نیست",
         "نامزد انباشت: ساختار فشرده + خالص خرید مثبت",
         "تراکم قیمت دیده می‌شود؛ خرید واقعی تأیید نشده"],
        default="شواهد انباشت هنوز کافی نیست"
    )

    # 3) Price momentum (15%): modest positive momentum is preferred over an already vertical move.
    momentum_score = (50 + 3.0 * ch24.clip(-10, 8) + 1.0 * ch7.clip(-20, 15)).clip(0, 100)
    out["Momentum_Factor_Score"] = momentum_score.where(ch24.notna() & ch7.notna(), np.nan)

    # 4) Liquidity / market quality (15%).
    cap_score = pd.Series(np.select(
        [market_cap >= 250_000_000, market_cap >= 75_000_000, market_cap >= 20_000_000, market_cap >= 10_000_000],
        [100, 85, 70, 50], default=15
    ), index=out.index, dtype=float).where(market_cap.notna(), np.nan)
    vol_score = pd.Series(np.select(
        [volume >= 10_000_000, volume >= 2_000_000, volume >= 500_000, volume >= 300_000],
        [100, 85, 65, 45], default=15
    ), index=out.index, dtype=float).where(volume.notna(), np.nan)
    liquidity_score = (0.55 * cap_score + 0.45 * vol_score)
    out["Liquidity_Quality_Score"] = liquidity_score
    out["Volume_Activity_Score"] = (turnover.rank(pct=True) * 100).where(turnover.notna(), np.nan)

    # 5) Technical analysis (10%). RSI/MACD are not fabricated when history is missing.
    tech = numeric(out.get("Technical_Score", pd.Series(np.nan, index=out.index)))
    rsi_value = numeric(out.get("RSI_14", pd.Series(np.nan, index=out.index)))
    macd = numeric(out.get("MACD", pd.Series(np.nan, index=out.index)))
    macd_signal = numeric(out.get("MACD_Signal", pd.Series(np.nan, index=out.index)))
    derived_tech = (100 - (rsi_value - 58).abs() * 2.2).clip(0, 100)
    derived_tech = derived_tech + np.where(macd.notna() & macd_signal.notna(), np.where(macd > macd_signal, 10, -10), 0)
    derived_tech = pd.Series(derived_tech, index=out.index).clip(0, 100)
    tech = tech.where(tech.notna(), derived_tech.where(rsi_value.notna() | (macd.notna() & macd_signal.notna())))
    out["Technical_PrePump_Score"] = tech

    # 6) BTC regime (5%): market-wide risk filter, not an altcoin-specific catalyst.
    btc_adjustment, btc_context = _btc_market_context(out)
    out["BTC_Market_Context"] = btc_context
    btc_score_value = 55.0 + btc_adjustment * 3.0
    out["BTC_Regime_Score"] = btc_score_value

    # 7) News / fundamentals (5%): only use a supplied/API-computed 0-100 score.
    news_score = numeric(out.get("News_Score", pd.Series(np.nan, index=out.index))).clip(0, 100)
    out["News_Factor_Score"] = news_score

    weights = {
        "Buy_Flow_Score": 30.0,
        "Volume_Acceleration_Score": 20.0,
        "Momentum_Factor_Score": 15.0,
        "Liquidity_Quality_Score": 15.0,
        "Technical_PrePump_Score": 10.0,
        "BTC_Regime_Score": 5.0,
        "News_Factor_Score": 5.0,
    }
    weighted_sum = pd.Series(0.0, index=out.index)
    available_weight = pd.Series(0.0, index=out.index)
    for column, weight in weights.items():
        value = numeric(out[column])
        present = value.notna()
        weighted_sum = weighted_sum + value.fillna(0) * weight
        available_weight = available_weight + present.astype(float) * weight
    # Renormalize only over observed evidence; publish coverage so a 90 with 40% coverage
    # cannot be mistaken for a fully researched 90. Missing factors are never treated as positive.
    out["Evidence_Coverage_Percent"] = available_weight.round(1)
    raw_score = (weighted_sum / available_weight.replace(0, np.nan)).clip(0, 100)

    abs24, abs7 = ch24.abs(), ch7.abs()
    quiet24 = pd.Series(np.select([abs24 <= 2, abs24 <= 4, abs24 <= 7], [100, 75, 35], default=0), index=out.index, dtype=float).where(ch24.notna(), np.nan)
    quiet7 = pd.Series(np.select([abs7 <= 5, abs7 <= 12, abs7 <= 20], [100, 75, 35], default=0), index=out.index, dtype=float).where(ch7.notna(), np.nan)
    out["Price_Still_Quiet_Score"] = (0.45 * quiet24 + 0.55 * quiet7)

    overheated = (ch24 >= 8) | (ch7 >= 20) | (ch24 <= -18) | (ch7 <= -35)
    thin = (market_cap.fillna(0) < 10_000_000) | (volume.fillna(0) < 300_000)
    missing_market = market_cap.isna() | volume.isna() | ch24.isna() | ch7.isna()
    no_acceleration = surge.isna() | (surge < 1.2)
    extreme_turnover = turnover > 0.20
    penalty = (np.where(overheated, 22, 0) + np.where(thin, 30, 0) +
               np.where(missing_market, 20, 0) + np.where(extreme_turnover, 20, 0) +
               np.where(no_acceleration, 10, 0))
    out["PrePump_Risk_Penalty"] = penalty
    score = (raw_score - penalty).clip(0, 100).where(eligible, 0)
    out["PrePump_Score"] = score.round(1)
    out["Pump_Potential_Score"] = out["PrePump_Score"]

    positive_flow = flow_available & (net_buy > 0) & (buy_share >= 52)
    strong_coverage = available_weight >= 75
    btc_not_bearish = btc_context not in ("BTC weak — risk-off", "BTC mildly weak")
    valid_setup = (eligible & ~symbol_ambiguous & ~overheated & ~thin & ~missing_market & ~extreme_turnover &
                   ch24.abs().le(5) & ch7.abs().le(12) & surge.ge(1.5) &
                   turnover.between(0.001, 0.15) & score.ge(70) & positive_flow &
                   rsi_value.between(40, 68) & strong_coverage & btc_not_bearish)
    watch_setup = (eligible & ~symbol_ambiguous & ~overheated & ~thin & ~missing_market & ~extreme_turnover &
                   ch24.abs().le(7) & ch7.abs().le(18) & turnover.between(0.001, 0.15) & score.ge(55))
    out["Signal"] = np.select(
        [out["Is_Stablecoin"], out["Is_Tokenized_Equity"], symbol_ambiguous, overheated, valid_setup,
         watch_setup & ~flow_available, watch_setup & flow_available & ~positive_flow,
         watch_setup & ~surge.notna(), watch_setup],
        ["Excluded — stablecoin", "Excluded — tokenized equity", "Hold — ambiguous ticker; verify contract",
         "Already moving / abnormal volatility — caution", "Pre-pump watch — real buying + volume confirmed",
         "Early activity — real buy/sell data missing",
         "Early activity — buy pressure not confirmed",
         "Early activity — volume history missing",
         "Early activity — monitor"], default="Watch — not enough evidence")
    out["Risk_Level"] = np.select(
        [out["Is_Stablecoin"], out["Is_Tokenized_Equity"], symbol_ambiguous, thin, overheated, extreme_turnover, missing_market],
        ["Excluded — stablecoin", "Excluded — tokenized equity", "Unverified ticker / contract", "High / thin market", "High / volatile", "High / abnormal turnover", "Incomplete market data"],
        default="Medium / review")
    return out


# =========================================================
# DATA SOURCES
# =========================================================
def _fetch_market_page(currency, page, api_key):
    return safe_get(
        f"{CG_API}/coins/markets",
        params={
            "vs_currency": currency,
            "order": "market_cap_desc",
            "per_page": 250,
            "page": int(page),
            "sparkline": "false",
            "price_change_percentage": "24h,7d",
        },
        headers=cg_headers(api_key),
        timeout=25,
    )


@st.cache_data(ttl=150, show_spinner=False)
def fetch_market_pages(currency, pages, api_key):
    """Fetch market pages concurrently (max 3 workers); cache the assembled result."""
    page_numbers = list(range(1, int(pages) + 1))
    rows_by_page = {}
    # Three concurrent requests improve multi-page scans without creating a large
    # burst against CoinGecko. Results are reassembled in page/rank order.
    with ThreadPoolExecutor(max_workers=min(3, len(page_numbers) or 1)) as pool:
        futures = {
            page: pool.submit(_fetch_market_page, currency, page, api_key)
            for page in page_numbers
        }
        for page in page_numbers:
            data = futures[page].result()
            rows_by_page[page] = data if isinstance(data, list) else []

    rows = []
    for page in page_numbers:
        data = rows_by_page[page]
        if not data:
            break
        rows.extend(data)
        if len(data) < 250:
            break

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


def green_candle_streak_from_history(history, min_days=5):
    """Aggregate intraday market-chart samples into UTC daily candles and find green runs."""
    if history is None or history.empty or not {"Time", "price"}.issubset(history.columns):
        return None
    frame = history[["Time", "price"]].copy().dropna()
    if len(frame) < min_days:
        return None
    frame["Time"] = pd.to_datetime(frame["Time"], utc=True, errors="coerce")
    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    frame = frame.dropna().sort_values("Time").set_index("Time")
    daily = frame["price"].resample("1D").agg(open="first", close="last").dropna()
    # Ignore today's unfinished candle so it cannot create a false green-day signal.
    today_utc = pd.Timestamp.now(tz="UTC").normalize()
    daily = daily[daily.index < today_utc]
    if len(daily) < min_days:
        return None
    daily["green"] = daily["close"] > daily["open"]
    runs = []
    run_start = None
    for i, is_green in enumerate(daily["green"].tolist()):
        if is_green and run_start is None:
            run_start = i
        if run_start is not None and (not is_green or i == len(daily) - 1):
            run_end = i - 1 if not is_green else i
            run_len = run_end - run_start + 1
            if run_len >= min_days:
                first_open = float(daily.iloc[run_start]["open"])
                last_close = float(daily.iloc[run_end]["close"])
                run_closes = daily.iloc[run_start:run_end + 1]["close"].to_numpy(dtype=float)
                trend_slope = float(np.polyfit(np.arange(len(run_closes)), run_closes, 1)[0]) if len(run_closes) >= 2 else 0.0
                change_pct = (last_close / first_open - 1) * 100 if first_open else 0.0
                if change_pct > 0 and trend_slope > 0:
                    runs.append({
                        "Green_Days": int(run_len),
                        "Streak_Start": daily.index[run_start].strftime("%Y-%m-%d"),
                        "Streak_End": daily.index[run_end].strftime("%Y-%m-%d"),
                        "Streak_Change_Percent": float(change_pct),
                        "Last_Daily_Close": last_close,
                    })
            run_start = None
    return max(runs, key=lambda x: (x["Green_Days"], x["Streak_Change_Percent"])) if runs else None


@st.cache_data(ttl=86400, show_spinner=False)
def translate_news_to_persian(text):
    """Translate short English news text to Persian; try two public services, fail safely."""
    original = str(text or "").strip()
    if not original:
        return ""
    if re.search(r"[\u0600-\u06FF]", original):
        return original

    # First choice: MyMemory free endpoint.
    try:
        response = _http_session().get(
            "https://api.mymemory.translated.net/get",
            params={"q": original[:480], "langpair": "en|fa"},
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json()
        translated = html.unescape(str((payload.get("responseData") or {}).get("translatedText") or "")).strip()
        if re.search(r"[\u0600-\u06FF]", translated):
            return translated
    except Exception:
        pass

    # Fallback: Google Translate's public web endpoint. It is unofficial and may be rate-limited.
    try:
        response = _http_session().get(
            "https://translate.googleapis.com/translate_a/single",
            params={"client": "gtx", "sl": "auto", "tl": "fa", "dt": "t", "q": original[:480]},
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json()
        chunks = payload[0] if isinstance(payload, list) and payload else []
        translated = "".join(str(chunk[0]) for chunk in chunks if isinstance(chunk, list) and chunk and chunk[0])
        translated = html.unescape(translated).strip()
        if re.search(r"[\u0600-\u06FF]", translated):
            return translated
    except Exception:
        pass
    return ""


@st.cache_data(ttl=300, show_spinner=False)
def fetch_news(currency_api_key="", coin_symbol=None):
    """Prefer CryptoPanic when keyed; otherwise use public publisher RSS feeds."""
    rows = []
    if currency_api_key:
        try:
            params = {"auth_token": currency_api_key, "public": "true", "kind": "news"}
            if coin_symbol and str(coin_symbol).upper() != "ALL":
                params["currencies"] = str(coin_symbol).lower()
            payload = safe_get(NEWS_API, params=params, timeout=20)
            for item in payload.get("results", []) if isinstance(payload, dict) else []:
                votes = item.get("votes") or {}
                rows.append({
                    "Published": item.get("published_at"), "Title": item.get("title", ""),
                    "Summary": item.get("description", ""),
                    "Source": (item.get("source") or {}).get("title", "CryptoPanic"),
                    "Currencies": ", ".join(c.get("code", "") for c in (item.get("currencies") or [])),
                    "Positive_Votes": votes.get("positive", 0), "Negative_Votes": votes.get("negative", 0),
                    "URL": item.get("url", ""),
                })
            if rows:
                return pd.DataFrame(rows), "CryptoPanic"
        except Exception as exc:
            keyed_error = str(exc)[:160]
        else:
            keyed_error = "CryptoPanic returned no articles; using public RSS fallback."
    else:
        keyed_error = "No CryptoPanic key; using public RSS sources."

    feeds = [
        ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("Cointelegraph", "https://cointelegraph.com/rss"),
        ("Decrypt", "https://decrypt.co/feed"),
    ]
    feed_errors = []
    wanted = str(coin_symbol or "ALL").strip().upper()
    for source, url in feeds:
        try:
            response = _http_session().get(url, timeout=15, headers={"Accept": "application/rss+xml, application/xml, text/xml"})
            response.raise_for_status()
            root = ET.fromstring(response.content)
            for node in root.iter():
                if node.tag.split("}")[-1].lower() not in ("item", "entry"):
                    continue
                fields = {}
                for child in list(node):
                    key = child.tag.split("}")[-1].lower()
                    value = "".join(child.itertext()).strip()
                    if key == "link" and not value:
                        value = child.attrib.get("href", "")
                    fields[key] = value
                title = fields.get("title", "").strip()
                summary = re.sub(r"<[^>]+>", " ", fields.get("description", fields.get("summary", "")))
                summary = re.sub(r"\s+", " ", summary).strip()
                if not title:
                    continue
                if wanted not in ("", "ALL", "*", "MARKET"):
                    searchable = f" {title} {summary} ".upper()
                    if not re.search(rf"(?<![A-Z0-9]){re.escape(wanted)}(?![A-Z0-9])", searchable):
                        continue
                rows.append({"Published": fields.get("pubdate", fields.get("published", fields.get("updated", ""))),
                             "Title": title, "Summary": summary[:500], "Source": source,
                             "Currencies": wanted if wanted not in ("", "ALL", "*", "MARKET") else "Market",
                             "Positive_Votes": 0, "Negative_Votes": 0, "URL": fields.get("link", "")})
        except Exception as exc:
            feed_errors.append(f"{source}: {str(exc)[:100]}")
    if rows:
        frame = pd.DataFrame(rows).drop_duplicates(subset=["Title"]).sort_values("Published", ascending=False, na_position="last")
        return frame.head(40).reset_index(drop=True), f"Public RSS • {len(rows)} articles • {keyed_error}"
    detail = " | ".join(feed_errors) if feed_errors else "No matching articles in the latest feed items."
    return pd.DataFrame(), f"{keyed_error} RSS unavailable: {detail}"


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
    # Derivatives are a separate positioning/risk overlay; they are not part of the
    # agreed seven-factor score and must not overwrite its fixed weights.
    out["Derivatives_Data_Available"] = has_derivatives
    return out


def _run_parallel_jobs(jobs, worker, max_workers=3):
    """Run independent API jobs concurrently and preserve input key order."""
    if not jobs:
        return {}
    results = {}
    with ThreadPoolExecutor(max_workers=min(max_workers, len(jobs))) as pool:
        futures = {key: pool.submit(worker, *args) for key, args in jobs.items()}
        for key in jobs:
            try:
                results[key] = futures[key].result()
            except Exception as exc:
                results[key] = exc
    return results


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
        response = None
        for attempt in range(3):
            response = _http_session().get(
                f"{CRYPTOMETER_API}/{endpoint.strip('/')}/",
                params=query,
                timeout=25,
            )
            if response.status_code in _HTTP_RETRY_STATUSES and attempt < 2:
                time.sleep(_retry_delay(response, attempt))
                continue
            break
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
st.title("📡 اسکنر هوشمند بازار ارزهای دیجیتال")
st.caption("پایش گسترده بازار • شناسایی فرصت‌های پیش از رشد • رادار انباشت • افزایش حجم • کنترل ریسک")
st.caption("Build 2026-11-08.2 • Parallel fetch + pooled HTTP + smart cache • Analysis engine preserved")
st.caption("سرعت دریافت بهینه شده: صفحات بازار و درخواست‌های مستقل هم‌زمان اجرا می‌شوند؛ پاسخ‌ها کش می‌شوند و خطاهای موقت/محدودیت API با تلاش مجدد کنترل‌شده مدیریت می‌شوند.")
st.warning(
    "امتیازها ابزار غربالگری‌اند، نه احتمال قطعی پامپ یا توصیه مالی. داده‌های ناقص به‌عنوان سیگنال مثبت فرض نمی‌شوند؛ درصد پوشش شواهد را کنار امتیاز ببین."
)
with st.expander("📘 راهنمای سریع استفاده از اسکنر", expanded=False):
    guide_a, guide_b, guide_c = st.columns(3)
    guide_a.markdown("**۱. امتیاز هفت‌عاملی**\n\nخرید واقعی ۳۰٪، شتاب حجم ۲۰٪، مومنتوم ۱۵٪، نقدشوندگی ۱۵٪، تکنیکال ۱۰٪، وضعیت BTC پنج درصد و خبر پنج درصد. عواملِ بدون داده از محاسبه کنار می‌روند و پوشش شواهد نمایش داده می‌شود.")
    guide_b.markdown("**۲. ورود ترکیبی و محافظه‌کارانه**\n\nورود اولیه حداکثر ۲۵٪ حجم موقعیت؛ ۷۵٪ باقی‌مانده فقط پس از شکست مقاومت و تثبیت با حجم مناسب. سیگنال Watch به معنی ورود نیست.")
    guide_c.markdown("**۳. مدیریت ریسک**\n\nریسک پیشنهادی هر معامله حداکثر ۰٫۵٪ سرمایه؛ حداقل نسبت سود به زیان ۲ به ۱. اگر داده کافی یا حدضرر ساختاری نداریم، ورود صادر نمی‌شود.")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("⚙️ تنظیمات اسکنر")
    data_source = st.radio("منبع اطلاعات بازار", ["CoinGecko market", "Upload CSV"], index=0, format_func=lambda x: "بازار زنده CoinGecko" if x == "CoinGecko market" else "بارگذاری فایل CSV")
    currency = st.selectbox("واحد نمایش قیمت", ["usd", "eur", "gbp"], index=0, format_func=lambda x: x.upper())
    if data_source == "CoinGecko market":
        pages = st.selectbox(
            "تعداد ارزهای مورد بررسی",
            options=[1, 2, 4, 8],
            format_func=lambda n: f"Up to {n * 250:,} market coins",
            index=2,
            help="Starts with up to 1,000 market coins. Reduce to 250 or 500 if CoinGecko rate limits occur.",
        )
        refresh_seconds = st.selectbox("فاصله به‌روزرسانی", [60, 120, 300, 600], index=1)
    uploaded = st.file_uploader("انتخاب فایل داده CSV", type=["csv"])
    st.divider()
    st.subheader("🔬 تحلیل تکنیکال")
    use_bybit_derivatives = st.checkbox(
        "دریافت نرخ فاندینگ و سود باز قراردادها",
        value=True,
        help="Uses public USDT perpetual data: Bybit first, then OKX, then Gate.io if blocked. No exchange API key is used."
    )
    technical_limit = st.selectbox(
        "تعداد ارز برای محاسبه شاخص‌های تکنیکال",
        [0, 10, 20, 30, 50],
        index=3,
        help="Fetches 7-day price and volume history for the highest turnover-to-market-cap candidates. 30 is a practical balance; 50 uses more API calls. 0 disables detailed indicators.",
    )
    run_technicals = st.button("محاسبه شاخص‌های تکنیکال", type="primary")
    st.divider()
    st.subheader("📰 اخبار بازار")
    news_key_input = st.text_input(
        "کلید CryptoPanic (اختیاری)",
        value=secret_or_env("CRYPTOPANIC_API_KEY"),
        type="password",
        help="بدون کلید هم خبرها از RSS عمومی CoinDesk، Cointelegraph و Decrypt دریافت می‌شوند.",
    )
    st.divider()
    st.subheader("🧪 جست‌وجوی صرافی‌های غیرمتمرکز")
    dex_query = st.text_input("نام ارز یا جفت معاملاتی", value="bitcoin", help="جفت‌های معاملاتی منطبق با عبارت جست‌وجو را پیدا می‌کند.")
    dex_button = st.button("Search DEX Screener")
    st.divider()
    min_score = st.slider("حداقل امتیاز پیش از رشد", 0, 100, 70)
    min_liquidity = st.number_input("حداقل نقدشوندگی DEX (دلار)", min_value=0, value=50000, step=10000)
    show_all = st.checkbox("نمایش همه ردیف‌های جدول داده", value=True)

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
                         "Volume_24h_vs_7d_Avg": np.nan,
                         "Price_Range_7d_Percent": np.nan,
                         "Price_Range_Last24h_Percent": np.nan,
                         "Range_Compression_Ratio": np.nan,
                         "Higher_Low_24h_Percent": np.nan,
                         "Accumulation_Price_Score": np.nan})
        results.append(item)
        progress.progress(i / max(1, len(candidates)), text=f"Indicators {i}/{len(candidates)}")
    progress.empty()
    tech = pd.DataFrame(results).drop_duplicates("CoinGecko_ID")
    st.session_state["scanner_technical_results"] = {"currency": currency, "data": tech.copy()}
    df = df.drop(columns=[c for c in ["RSI_14", "MACD", "MACD_Signal", "Trend_7d_Percent", "Technical_Score", "Technical_Signal", "Volume_24h_vs_7d_Avg", "Price_Range_7d_Percent", "Price_Range_Last24h_Percent", "Range_Compression_Ratio", "Higher_Low_24h_Percent", "Accumulation_Price_Score"] if c in df.columns])
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
            df = df.drop(columns=[c for c in ["RSI_14", "MACD", "MACD_Signal", "Trend_7d_Percent", "Technical_Score", "Technical_Signal", "Volume_24h_vs_7d_Avg", "Price_Range_7d_Percent", "Price_Range_Last24h_Percent", "Range_Compression_Ratio", "Higher_Low_24h_Percent", "Accumulation_Price_Score"] if c in df.columns])
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
# MARKET SENTIMENT INDICES — Fear & Greed + Altcoin Season
# =========================================================
@st.cache_data(ttl=900, show_spinner=False)
def fetch_fear_greed_history():
    """Alternative.me daily Fear & Greed observations (latest 31 records)."""
    payload = safe_get(
        "https://api.alternative.me/fng/",
        params={"limit": 31, "format": "json"},
        timeout=15,
    )
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    records = []
    for item in rows:
        try:
            value = float(item.get("value"))
            stamp = int(item.get("timestamp"))
            if 0 <= value <= 100 and stamp > 0:
                records.append({
                    "Timestamp": pd.to_datetime(stamp, unit="s", utc=True),
                    "Value": value,
                    "Classification": str(item.get("value_classification", "")),
                })
        except (TypeError, ValueError, OverflowError):
            continue
    if not records:
        raise ValueError("Fear & Greed provider returned no valid observations")
    return pd.DataFrame(records).sort_values("Timestamp").reset_index(drop=True)


@st.cache_data(ttl=900, show_spinner=False)
def fetch_altcoin_season_index():
    """CoinMarketCap public/keyless Altcoin Season Index endpoint."""
    payload = safe_get(
        "https://pro-api.coinmarketcap.com/public-api/v1/altcoin-season-index/latest",
        timeout=15,
    )
    data = payload.get("data", {}) if isinstance(payload, dict) else {}
    value = data.get("altcoin_index")
    if value is None:
        raise ValueError("Altcoin Season Index is not present in provider response")
    value = float(value)
    if not 0 <= value <= 100:
        raise ValueError("Altcoin Season Index is outside the 0–100 range")
    return {
        "value": value,
        "snapshot_time": data.get("snapshot_time"),
        "yearly_high": data.get("yearly_high"),
        "yearly_low": data.get("yearly_low"),
    }


def sentiment_label(value):
    if value < 25:
        return "ترس شدید"
    if value < 45:
        return "ترس"
    if value <= 55:
        return "خنثی"
    if value <= 75:
        return "طمع"
    return "طمع شدید"


def render_semi_gauge(value, title, subtitle, marker_color="#1769d2"):
    """Compact semicircular Plotly gauge with explicit 0–100 scale."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(value),
        number={"font": {"size": 38, "color": "#102846"}, "suffix": " / 100"},
        title={"text": f"<b>{title}</b><br><span style='font-size:13px;color:#52677f'>{subtitle}</span>",
               "font": {"size": 18, "color": "#102846"}},
        gauge={
            "shape": "angular",
            "axis": {"range": [0, 100], "tickmode": "array", "tickvals": [0, 25, 50, 75, 100],
                     "tickfont": {"size": 11, "color": "#465b75"}},
            "bar": {"color": marker_color, "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 25], "color": "#f46b65"},
                {"range": [25, 45], "color": "#ffad72"},
                {"range": [45, 55], "color": "#f6d878"},
                {"range": [55, 75], "color": "#9cdda0"},
                {"range": [75, 100], "color": "#35c878"},
            ],
            "threshold": {"line": {"color": marker_color, "width": 4}, "thickness": 0.85,
                          "value": float(value)},
        },
    ))
    fig.update_layout(height=265, margin={"l": 22, "r": 22, "t": 65, "b": 12},
                      paper_bgcolor="rgba(0,0,0,0)", font={"family": "Arial"})
    return fig


# =========================================================
# منوی اصلی بخش‌های اسکنر
# =========================================================
filtered = df[(numeric(df["PrePump_Score"]).fillna(0) >= min_score) & (~df["Is_Excluded_Asset"])].copy()  # پیش‌فرض برای بخش‌های دیگر
section = st.radio(
    "انتخاب بخش اسکنر",
    ["🏠 نمای کلی", "🧲 رادار انباشت و پیش‌پامپ", "📊 نمودارها و ریزش‌ها", "📰 اخبار و DEX", "🐋 جریان پول و مشتقات", "📁 داده‌ها"],
    horizontal=True,
    label_visibility="collapsed",
    key="scanner_section_navigation",
)
# Keep scheduled refreshes away from the CryptoMeter panel so they cannot
# interrupt a user-initiated mobile/API request.
if section != "🐋 جریان پول و مشتقات" and data_source == "CoinGecko market":
    st_autorefresh(interval=refresh_seconds * 1000, key="scanner_refresh")
st.caption({
    "🏠 نمای کلی": "خلاصه وضعیت بازار و شاخص‌های اصلی اسکنر",
    "🧲 رادار انباشت و پیش‌پامپ": "ارزهایی که نشانه‌های اولیه انباشت یا فعالیت پیش از رشد دارند",
    "📊 نمودارها و ریزش‌ها": "بررسی ساختار قیمت، شاخص‌های تکنیکال و ارزهای با افت شدید",
    "📰 اخبار و DEX": "اخبار، فعالیت صرافی‌های غیرمتمرکز و فشار خرید و فروش",
    "🐋 جریان پول و مشتقات": "جریان پول، خرید و فروش واقعی، فاندینگ و سود باز",
    "📁 داده‌ها": "مشاهده و دریافت داده خام بازار",
}[section])
st.divider()

# =========================================================
if section == "🏠 نمای کلی":
    # MAIN FILTERS / KPIS
    # =========================================================
    st.caption(
        f"Source: {dataset_name} • Rows loaded: {len(df):,} • "
        f"Display refreshed: {pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )
    st.info(
        "وزن‌ها: خرید واقعی ۳۰٪ • شتاب حجم ۲۰٪ • مومنتوم ۱۵٪ • نقدشوندگی ۱۵٪ • تکنیکال ۱۰٪ • رژیم BTC پنج درصد • خبر پنج درصد. "
        "داده ناموجود امتیاز مثبت نمی‌گیرد؛ امتیاز با وزن عواملِ واقعاً موجود نرمال می‌شود و پوشش شواهد جداگانه نشان داده می‌شود. "
        "رادار انباشت جداگانه فشردگی قیمت، کف‌های بالاتر، خرید خالص واقعی، حجم و RSI را می‌سنجد؛ فشردگی قیمت به‌تنهایی اثبات خرید نهنگ نیست. برای سیگنال Pre-Pump معتبر، خرید واقعی مثبت، شتاب حجم، تکنیکال قابل محاسبه و شرایط مناسب بازار لازم است. OI و حجم معاملات به‌تنهایی ورود پول یا خرید نهنگ نیستند."
    )
    if data_source == "CoinGecko market" and use_bybit_derivatives:
        if bybit_status.startswith("matched"):
            st.success(f"Public derivatives feed: {bybit_status} • cached 90 seconds")
        else:
            st.warning(f"Public derivatives feed {bybit_status}. Scanner continues without it.")

    # Live sentiment meters — these are market context indicators, not entry signals.
    st.divider()
    st.subheader("🌡️ دماسنج احساسات بازار")
    st.caption("دو شاخص مستقل برای سنجش جو بازار؛ مقدارها از ارائه‌دهنده دریافت می‌شوند و در صورت قطعی API عدد ساختگی نمایش داده نمی‌شود.")
    fg_col, alt_col = st.columns(2, gap="large")
    fg_value = None
    alt_value = None
    try:
        fg_history = fetch_fear_greed_history()
        fg_latest = fg_history.iloc[-1]
        fg_value = float(fg_latest["Value"])
        fg_label = sentiment_label(fg_value)
        with fg_col:
            st.plotly_chart(
                render_semi_gauge(fg_value, "شاخص ترس و طمع", fg_label, "#1769d2"),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            if len(fg_history) >= 2:
                previous_value = float(fg_history.iloc[-2]["Value"])
                delta = fg_value - previous_value
                st.metric("تغییر نسبت به مشاهده قبلی", f"{delta:+.0f} واحد", delta_color="normal")
            st.caption("منبع: Alternative.me — داده روزانه؛ شاخص احساسات است، نه سیگنال قطعی خرید یا فروش.")
            history_chart = go.Figure()
            history_chart.add_trace(go.Scatter(
                x=fg_history["Timestamp"], y=fg_history["Value"], mode="lines+markers",
                name="Fear & Greed", line={"color": "#1769d2", "width": 3},
                marker={"size": 5},
            ))
            history_chart.add_hrect(y0=0, y1=25, fillcolor="#f46b65", opacity=0.08, line_width=0)
            history_chart.add_hrect(y0=75, y1=100, fillcolor="#35c878", opacity=0.08, line_width=0)
            history_chart.update_layout(
                title="روند ۳۰ روزه ترس و طمع", height=220,
                margin={"l": 12, "r": 12, "t": 42, "b": 12},
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis={"range": [0, 100], "title": "امتیاز", "gridcolor": "#e4ebf4"},
                xaxis={"title": "", "gridcolor": "#f0f3f8"},
                showlegend=False,
            )
            st.plotly_chart(history_chart, use_container_width=True, config={"displayModeBar": False})
    except Exception as exc:
        with fg_col:
            st.warning(f"شاخص ترس و طمع فعلاً دریافت نشد: {str(exc)[:180]}")

    try:
        alt_data = fetch_altcoin_season_index()
        alt_value = alt_data["value"]
        if alt_value < 25:
            alt_label = "فصل بیت‌کوین"
        elif alt_value > 75:
            alt_label = "فصل آلت‌کوین‌ها"
        else:
            alt_label = "فصل خنثی / انتقالی"
        with alt_col:
            st.plotly_chart(
                render_semi_gauge(alt_value, "شاخص فصل آلت‌کوین‌ها", alt_label, "#087f6b"),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.metric("وضعیت بازار آلت‌کوین‌ها", alt_label)
            st.caption("منبع: CoinMarketCap Public API • کمتر از ۲۵: فصل بیت‌کوین؛ بیشتر از ۷۵: فصل آلت‌کوین‌ها.")
            if alt_data.get("snapshot_time"):
                st.caption(f"زمان ثبت داده: {alt_data['snapshot_time']}")
    except Exception as exc:
        with alt_col:
            st.warning(f"شاخص فصل آلت‌کوین‌ها فعلاً دریافت نشد: {str(exc)[:180]}")

    st.divider()

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

    # Persian market intelligence report (uses only fields actually present)
    st.divider()
    with st.container(border=True):
        st.subheader("🧠 گزارش هوشمند بازار و ردپای نهنگ‌ها")
        st.caption("گزارش پویا بر اساس داده‌های همین اجرای اسکنر؛ نبود داده به‌عنوان سیگنال مثبت تفسیر نمی‌شود.")

        report_parts = []
        market_up = int((numeric(df.get("Change_24h_Percent", pd.Series(np.nan, index=df.index))) > 0).sum())
        market_down = int((numeric(df.get("Change_24h_Percent", pd.Series(np.nan, index=df.index))) < 0).sum())
        market_valid = market_up + market_down
        if market_valid:
            up_share = market_up / market_valid * 100
            if up_share >= 60:
                report_parts.append(f"**تصویر کلی بازار:** جو کوتاه‌مدت متمایل به صعود است؛ {up_share:.0f}٪ از ارزهای دارای تغییر ۲۴ساعته مثبت هستند. برای تأیید، رشد حجم و عملکرد بیت‌کوین نیز باید بررسی شود.")
            elif up_share <= 40:
                report_parts.append(f"**تصویر کلی بازار:** فشار نزولی غالب است؛ فقط {up_share:.0f}٪ از ارزهای دارای داده تغییر ۲۴ساعته مثبت‌اند. در چنین شرایطی ورود عجولانه به آلت‌کوین‌ها ریسک بیشتری دارد.")
            else:
                report_parts.append(f"**تصویر کلی بازار:** وضعیت دوطرفه و بدون برتری روشن است؛ {up_share:.0f}٪ از ارزهای دارای داده مثبت‌اند. بهتر است منتظر تأیید جهت بازار بمانیم.")
        else:
            report_parts.append("**تصویر کلی بازار:** داده کافی برای سنجش گستردگی رشد و ریزش بازار وجود ندارد.")

        flow_col = "Net_Buy_USD" if "Net_Buy_USD" in df.columns else None
        buy_share_col = "Buy_Share_Percent" if "Buy_Share_Percent" in df.columns else None
        if flow_col:
            net_flow = numeric(df[flow_col])
            known_flow = net_flow.dropna()
            if not known_flow.empty:
                net_total = float(known_flow.sum())
                if net_total > 0:
                    report_parts.append(f"**جریان خرید ثبت‌شده:** خالص خرید واقعی در ردیف‌های دارای داده حدود {fmt_money(net_total, 'USD')} مثبت است؛ این نشانه به نفع تقاضاست، اما به‌تنهایی تضمین‌کننده رشد قیمت نیست.")
                elif net_total < 0:
                    report_parts.append(f"**جریان فروش ثبت‌شده:** خالص جریان خرید/فروش حدود {fmt_money(abs(net_total), 'USD')} به سمت فروش است؛ فشار عرضه را جدی بگیر.")
                else:
                    report_parts.append("**جریان پول:** خالص خرید و فروش ثبت‌شده تقریباً متعادل است.")
            else:
                report_parts.append("**جریان پول:** داده واقعی خالص خرید برای این بازار در دسترس نیست؛ حجم ۲۴ساعته به‌تنهایی ورود پول را ثابت نمی‌کند.")
        else:
            report_parts.append("**جریان پول:** ستون خالص خرید واقعی در داده فعلی موجود نیست؛ از حجم معاملات به‌عنوان ورود پول قطعی استفاده نمی‌کنیم.")

        if buy_share_col:
            shares = numeric(df[buy_share_col]).dropna()
            if not shares.empty:
                mean_share = float(shares.mean())
                report_parts.append(f"**فشار خرید:** میانگین سهم خرید ثبت‌شده در ارزهای دارای داده {mean_share:.1f}٪ است؛ این عدد فقط برای همان نمونه‌های پوشش‌داده‌شده معتبر است.")

        cm_report = st.session_state.get("cryptometer_results", {})
        whale_payload = cm_report.get("whales", {}).get("payload") if isinstance(cm_report, dict) else None
        if whale_payload:
            report_parts.append("**ردپای نهنگ‌ها:** داده معاملات بزرگ CryptoMeter دریافت شده است. جمع‌بندی جهت خرید و فروش در بخش «جریان پول و مشتقات» و نمودار معاملات نهنگ‌ها نمایش داده می‌شود.")
        else:
            report_parts.append("**ردپای نهنگ‌ها:** در این اجرا داده معاملات نهنگ از CryptoMeter دریافت نشده است؛ بنابراین نمی‌توان با اطمینان از انباشت یا توزیع نهنگ‌ها صحبت کرد.")

        if "Signal" in df.columns:
            pre_count = int(df["Signal"].astype(str).str.startswith("Pre-pump watch").sum())
            avoid_count = int(df["Risk_Level"].astype(str).str.startswith("High").sum()) if "Risk_Level" in df.columns else 0
            report_parts.append(f"**فرصت‌های زیرنظر:** اسکنر {pre_count} مورد در وضعیت رصد پیش‌پامپ و {avoid_count} مورد با ریسک بالا شناسایی کرده است. رصد به معنی نقطه ورود نیست؛ شکست مقاومت و تثبیت همراه حجم لازم است.")

        st.markdown("### 🧭 خلاصه تصمیم‌گیری بازار")
        market_change = numeric(df.get("Change_24h_Percent", pd.Series(np.nan, index=df.index)))
        median_change = market_change.median()
        btc_rows = df[df.get("Symbol", pd.Series("", index=df.index)).astype(str).str.upper().eq("BTC")]
        if not btc_rows.empty:
            btc_row = btc_rows.iloc[0]
            btc_24 = numeric(pd.Series([btc_row.get("Change_24h_Percent")])).iloc[0]
            btc_7 = numeric(pd.Series([btc_row.get("Change_7d_Percent")])).iloc[0]
            btc_text = f"بیت‌کوین: ۲۴ساعته {btc_24:+.2f}٪" if pd.notna(btc_24) else "بیت‌کوین: تغییر ۲۴ساعته ناموجود"
            btc_text += f" و هفتگی {btc_7:+.2f}٪" if pd.notna(btc_7) else "؛ داده هفتگی ناموجود"
        else:
            btc_text = "داده بیت‌کوین در فهرست فعلی موجود نیست."
        if pd.notna(median_change):
            breadth_text = f"میانه تغییر ۲۴ساعته کل فهرست {median_change:+.2f}٪ است؛ "
            breadth_text += "اکثریت بازار تمایل مثبت دارد." if market_valid and market_up / market_valid >= 0.60 else ("اکثریت بازار تمایل منفی دارد." if market_valid and market_up / market_valid <= 0.40 else "بازار جهت یکپارچه‌ای ندارد.")
        else:
            breadth_text = "برای محاسبه میانه تغییرات بازار داده کافی نداریم."
        st.write(f"**وضعیت بیت‌کوین:** {btc_text}")
        st.write(f"**گستردگی بازار:** {breadth_text}")
        candidates = df[~df.get("Is_Excluded_Asset", pd.Series(False, index=df.index)).fillna(False)].copy()
        if "PrePump_Score" in candidates.columns:
            candidates["PrePump_Score"] = numeric(candidates["PrePump_Score"])
            candidates = candidates[candidates["PrePump_Score"].notna()].sort_values("PrePump_Score", ascending=False)
            if not candidates.empty:
                top = candidates.head(3)
                top_text = "، ".join(f"{r.get('Symbol','?')} ({float(r['PrePump_Score']):.0f}/100)" for _, r in top.iterrows())
                st.write(f"**سه گزینه با امتیاز پیش‌پامپ بالاتر:** {top_text}؛ این‌ها فقط برای رصد هستند و بدون تأیید خرید واقعی/حجم، سیگنال ورود محسوب نمی‌شوند.")
            else:
                st.write("**فرصت پیش‌پامپ:** هنوز گزینه‌ای با امتیاز معتبر و داده کافی شناسایی نشده است.")
        else:
            st.write("**فرصت پیش‌پامپ:** امتیاز پیش‌پامپ در داده فعلی محاسبه نشده است.")
        for report_line in report_parts:
            st.markdown(report_line)

        st.caption("این گزارش تحلیلی و غربالگری است، نه پیش‌بینی قطعی. کیفیت نتیجه به پوشش و تازگی داده‌های API وابسته است.")

    st.divider()
if section == "🧲 رادار انباشت و پیش‌پامپ":
    st.subheader("🧲 رادار انباشت قبل از شکست مقاومت")
    st.caption("این بخش جدا از امتیاز هفت‌عاملی است: فشردگی دامنه قیمت، کف‌های بالاتر، خرید خالص واقعی، شتاب حجم و RSI را می‌سنجد. فشردگی قیمت به‌تنهایی اثبات انباشت نهنگ‌ها نیست؛ برای تأیید خرید واقعی، داده خرید/فروش دلاری لازم است.")
    accumulation_view = df[~df["Is_Excluded_Asset"]].copy()
    if "Accumulation_Score" in accumulation_view.columns:
        accumulation_view["Accumulation_Score"] = numeric(accumulation_view["Accumulation_Score"])
        accumulation_view = accumulation_view[
            accumulation_view["Accumulation_Score"].notna() &
            (numeric(accumulation_view["Accumulation_Data_Coverage"]).fillna(0) >= 35)
        ].sort_values(["Accumulation_Score", "Accumulation_Data_Coverage"], ascending=[False, False])
        accumulation_cols = [c for c in [
            "Coin", "Symbol", "Accumulation_Score", "Accumulation_Data_Coverage",
            "Range_Compression_Ratio", "Higher_Low_24h_Percent", "Buy_Share_Percent",
            "Net_Buy_USD", "Volume_24h_vs_7d_Avg", "RSI_14", "Accumulation_Status"
        ] if c in accumulation_view.columns]
        if not accumulation_view.empty and accumulation_cols:
            accumulation_display = accumulation_view[accumulation_cols].head(20).rename(columns={
                "Coin": "ارز", "Symbol": "نماد", "Accumulation_Score": "امتیاز انباشت",
                "Accumulation_Data_Coverage": "پوشش داده انباشت٪", "Range_Compression_Ratio": "نسبت فشردگی دامنه",
                "Higher_Low_24h_Percent": "تغییر کف ۲۴ساعته٪", "Buy_Share_Percent": "سهم خرید واقعی٪",
                "Net_Buy_USD": "خالص خرید دلاری", "Volume_24h_vs_7d_Avg": "حجم ۲۴ساعت / مبنا",
                "RSI_14": "RSI", "Accumulation_Status": "تفسیر وضعیت"
            })
            st.dataframe(accumulation_display, use_container_width=True, hide_index=True)
        else:
            st.info("برای محاسبه رادار انباشت، ابتدا از تنظیمات کناری دکمه «Calculate technical indicators» را اجرا کن.")
    else:
        st.info("ستون‌های لازم برای ارزیابی انباشت هنوز موجود نیستند.")

    st.divider()
    st.subheader("🛰️ فرصت‌های احتمالی پیش از رشد")
    st.caption("استیبل‌کوین‌ها حذف شده‌اند. سیگنال معتبر نیازمند خرید واقعی مثبت، شتاب حجم، تکنیکال قابل محاسبه، نقدشوندگی مناسب و بازار BTC غیرنزولی است. درصد پوشش نشان می‌دهد چه مقدار از هفت عامل واقعاً داده داشته‌اند.")
    if not filtered.empty:
        if "Volume_24h_vs_7d_Avg" not in filtered.columns:
            filtered["Volume_24h_vs_7d_Avg"] = np.nan
        ranked = filtered.sort_values(["PrePump_Score", "Volume_24h_vs_7d_Avg"], ascending=[False, False], na_position="last").copy()
        # Radar view of the leading candidates. Missing factors stay blank, not zero or a fabricated neutral.
        radar_factors = [
            ("Buy_Flow_Score", "خرید واقعی"),
            ("Volume_Acceleration_Score", "شتاب حجم"),
            ("Momentum_Factor_Score", "مومنتوم"),
            ("Liquidity_Quality_Score", "نقدشوندگی"),
            ("Technical_PrePump_Score", "تکنیکال"),
            ("BTC_Regime_Score", "وضعیت BTC"),
            ("News_Factor_Score", "اخبار"),
        ]
        radar_rows = ranked.head(3)
        if not radar_rows.empty:
            radar_fig = go.Figure()
            theta = [label for _, label in radar_factors]
            for _, radar_row in radar_rows.iterrows():
                values = [float(radar_row[col]) if col in radar_row.index and pd.notna(radar_row[col]) else None for col, _ in radar_factors]
                radar_fig.add_trace(go.Scatterpolar(
                    r=values, theta=theta, fill="toself", name=f"{radar_row.get('Symbol', '')}"
                ))
            radar_fig.update_layout(
                title="مقایسه عوامل هفت‌گانه سه گزینه برتر",
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                template="plotly_white", height=420, margin=dict(l=35, r=35, t=55, b=35),
                legend=dict(orientation="h", y=-0.15),
            )
            st.plotly_chart(radar_fig, width="stretch")
            st.caption("هر محور فقط در صورت وجود داده رسم می‌شود؛ خالی بودن محور یعنی داده نداریم، نه اینکه امتیاز آن صفر یا ۵۰ باشد.")
        confirmed = ranked[ranked["Signal"].astype(str).str.startswith("Pre-pump watch — real buying")]
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
                "Accumulation_Score", "Accumulation_Data_Coverage", "Accumulation_Status",
                "Range_Compression_Ratio", "Higher_Low_24h_Percent",
                "Volume_24h_vs_7d_Avg", "Volume_Acceleration_Score", "Market_Cap_Rank", "RSI_14", "Technical_PrePump_Score",
                "Buy_Volume_USD", "Sell_Volume_USD", "Net_Buy_USD", "Buy_Share_Percent", "Buy_Flow_Status",
                "Momentum_Factor_Score", "Liquidity_Quality_Score", "BTC_Market_Context", "BTC_Regime_Score", "News_Factor_Score", "Evidence_Coverage_Percent",
                "Funding_Rate_Percent", "Open_Interest_USD", "Derivatives_Turnover_24h_USD", "Derivatives_Exchange",
                "Derivatives_Context_Score", "PrePump_Score", "Pump_Potential_Score", "Signal", "Risk_Level", "Technical_Signal",
            ]
            cols = [c for c in preferred_cols if c in ranked.columns]
            display_names = {
                "Coin": "Coin", "Symbol": "Ticker", "Price": f"Price ({currency.upper()})",
                "Change_24h_Percent": "24h change (%)", "Change_7d_Percent": "7d change (%)",
                "Volume_24h": f"24h volume ({currency.upper()})", "Market_Cap_Rank": "Market rank",
                "Volume_to_Market_Cap": "Volume / market cap", "Volume_Activity_Score": "Turnover activity",
                "Price_Still_Quiet_Score": "Price still quiet", "Accumulation_Score": "امتیاز انباشت",
                "Accumulation_Data_Coverage": "پوشش داده انباشت (%)", "Accumulation_Status": "وضعیت انباشت",
                "Range_Compression_Ratio": "نسبت فشردگی دامنه", "Higher_Low_24h_Percent": "تغییر کف ۲۴ساعته (%)",
                "Volume_24h_vs_7d_Avg": "24h volume vs 7d baseline",
                "Volume_Acceleration_Score": "Volume acceleration score", "Momentum_Factor_Score": "Momentum score",
                "Liquidity_Quality_Score": "Liquidity score", "BTC_Regime_Score": "BTC regime score",
                "News_Factor_Score": "News score", "Evidence_Coverage_Percent": "Evidence coverage (%)",
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
            st.caption("برای دیدن نمودار یک ارز، روی ردیف آن کلیک کن.")
            table_event = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="candidate_coin_table_select",
            )
            selected_rows = table_event.selection.rows if table_event and table_event.selection else []
            if selected_rows:
                selected_coin_row = ranked.iloc[int(selected_rows[0])]
                selected_coin_name = str(selected_coin_row.get("Coin", "ارز انتخاب‌شده"))
                selected_coin_symbol = str(selected_coin_row.get("Symbol", "")).upper()
                st.divider()
                st.subheader(f"📈 نمودار {selected_coin_name} ({selected_coin_symbol})")
                if data_source == "CoinGecko market" and pd.notna(selected_coin_row.get("CoinGecko_ID")):
                    chart_days = st.selectbox(
                        "بازه نمودار",
                        [1, 7, 30, 90],
                        index=1,
                        format_func=lambda x: {1: "۱ روز", 7: "۷ روز", 30: "۳۰ روز", 90: "۹۰ روز"}[x],
                        key="clicked_coin_chart_days",
                    )
                    try:
                        clicked_hist = fetch_history(str(selected_coin_row["CoinGecko_ID"]), currency, chart_days, cg_key)
                        if clicked_hist is not None and not clicked_hist.empty and "price" in clicked_hist.columns:
                            clicked_hist = clicked_hist.sort_values("Time").copy()
                            clicked_hist["price"] = pd.to_numeric(clicked_hist["price"], errors="coerce")
                            clicked_hist = clicked_hist.dropna(subset=["price"])
                            if not clicked_hist.empty:
                                clicked_fig = go.Figure()
                                clicked_fig.add_trace(go.Scatter(
                                    x=clicked_hist["Time"], y=clicked_hist["price"],
                                    mode="lines", name=selected_coin_symbol,
                                    line=dict(color="#1769d2", width=2.5),
                                    fill="tozeroy", fillcolor="rgba(23,105,210,0.08)",
                                ))
                                clicked_fig.update_layout(
                                    template="plotly_white", height=420,
                                    title=f"{selected_coin_symbol} — نمودار قیمت ({chart_days} روز)",
                                    paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
                                    font=dict(color="#172b4d"),
                                    margin=dict(l=15, r=15, t=55, b=25),
                                    hovermode="x unified",
                                    xaxis=dict(title="زمان", gridcolor="#e5edf6"),
                                    yaxis=dict(title=f"قیمت ({currency.upper()})", gridcolor="#e5edf6"),
                                )
                                st.plotly_chart(clicked_fig, use_container_width=True)
                                latest_clicked_price = clicked_hist["price"].iloc[-1]
                                st.metric("آخرین قیمت داده تاریخی", fmt_money(latest_clicked_price), currency.upper())
                            else:
                                st.warning("داده قیمت تاریخی معتبر برای این ارز دریافت نشد.")
                        else:
                            st.warning("تاریخچه قیمت برای این ارز در دسترس نیست.")
                    except Exception as chart_error:
                        st.warning(f"دریافت نمودار ناموفق بود: {chart_error}")
                else:
                    st.info("برای نمایش نمودار تاریخی، منبع داده باید CoinGecko باشد و شناسه تاریخی ارز موجود باشد.")
            st.caption("RSI از صفر تا ۱۰۰ است: بالای ۷۰ می‌تواند نشانه داغ‌شدن حرکت و زیر ۳۰ نشانه فشار فروش شدید باشد؛ به‌تنهایی سیگنال خرید نیست. MACD بالای خط سیگنال یعنی مومنتوم صعودی‌تر، اما باید با حجم و ساختار قیمت تأیید شود.")
            st.caption("روش ورود: ۲۵٪ اولیه فقط در ناحیه ساختاری مناسب؛ ۷۵٪ پس از شکست و تثبیت مقاومت. حدضرر پشت کف/حمایت ساختاری؛ اگر داده تاریخی برای تعیین آن نداریم، سطح ورود و خروج ساخته نمی‌شود. سقف ریسک هر معامله ۰٫۵٪ سرمایه و حداقل R/R برابر ۲ است.")
    else:
        st.info("No verified early-activity candidates match these filters yet. Calculate historical indicators or lower the minimum score to inspect unconfirmed setups.")

if section == "📊 نمودارها و ریزش‌ها":
    # Separate watchlist for deeply declined assets (not mixed with pre-pump candidates).
    st.subheader("📉 ارزهای با بیشترین ریزش")
    st.caption("این فهرست فقط برای بررسی احتمال برگشت است؛ ریزش زیاد به‌تنهایی دلیل خرید نیست.")
    drop_view = df[~df["Is_Excluded_Asset"]].copy()
    drop_view["_drop_rank"] = numeric(drop_view["Change_7d_Percent"])
    drop_view = drop_view.dropna(subset=["_drop_rank"]).sort_values("_drop_rank").head(15)
    if not drop_view.empty:
        drop_cols = [c for c in ["Coin", "Symbol", "Price", "Change_24h_Percent", "Change_7d_Percent", "Volume_24h", "RSI_14", "PrePump_Score", "Buy_Flow_Status", "Risk_Level"] if c in drop_view.columns]
        st.dataframe(drop_view[drop_cols], width="stretch", hide_index=True)
    else:
        st.info("داده کافی برای رتبه‌بندی ریزش هفتگی موجود نیست.")

    # Alerts for sharp moves
    st.subheader("🔔 هشدار حرکت‌های غیرعادی بازار")
    alerts = df[(numeric(df["Change_24h_Percent"]).abs() >= 5) | (numeric(df["Change_7d_Percent"]).abs() >= 15)].copy()
    if not alerts.empty:
        # Restore the original alert ranking: highest 24h percentage move first.
        alerts = alerts.sort_values(
            "Change_24h_Percent", ascending=False, na_position="last", kind="mergesort"
        )
        alert_columns = ["Coin", "Symbol", "Change_24h_Percent", "Change_7d_Percent", "Volume_24h", "Pump_Potential_Score", "Risk_Level"]
        st.dataframe(alerts[alert_columns].head(30), use_container_width=True, hide_index=True)
    else:
        st.info("No moves crossed the default alert thresholds.")

    # Multi-day consecutive green-candle scan (daily candles built from CoinGecko history).
    st.divider()
    st.subheader("🟢 ارزهای دارای حداقل ۵ روز متوالی کندل سبز")
    st.caption("اسکن حداکثر ۴۰ ارز نقدشونده بر اساس داده تاریخی ۳۰ روزه؛ فقط روزهای کامل UTC شمرده می‌شوند. هر ردیف باید حداقل ۵ کندل روزانه سبزِ پی‌درپی و بازده مثبت در همان بازه داشته باشد.")
    if data_source != "CoinGecko market" or "CoinGecko_ID" not in df.columns:
        st.info("برای اسکن کندل‌های روزانه، منبع داده CoinGecko market را انتخاب کن.")
    else:
        if st.button("🔍 اسکن ارزهای با کندل سبز متوالی", type="primary", key="scan_green_streaks"):
            scan_universe = df.copy()
            if "Is_Excluded_Asset" in scan_universe.columns:
                scan_universe = scan_universe[~scan_universe["Is_Excluded_Asset"].fillna(False)]
            scan_universe["_scan_volume"] = numeric(scan_universe["Volume_24h"]).fillna(0)
            scan_universe = scan_universe[scan_universe["CoinGecko_ID"].notna()].sort_values("_scan_volume", ascending=False).head(40)
            found = []
            errors = 0
            def _scan_one_green(row):
                hist = fetch_history(str(row["CoinGecko_ID"]), currency, 30, cg_key)
                streak = green_candle_streak_from_history(hist, min_days=5)
                if streak:
                    return {
                        "Coin": row.get("Coin", ""), "Symbol": row.get("Symbol", ""),
                        "Green_Days": streak["Green_Days"],
                        "Streak_Change_Percent": streak["Streak_Change_Percent"],
                        "Streak_Start": streak["Streak_Start"], "Streak_End": streak["Streak_End"],
                        "Last_Daily_Close": streak["Last_Daily_Close"],
                        "Volume_24h": row.get("Volume_24h", np.nan),
                    }
                return None
            with st.spinner(f"در حال بررسی کندل‌های روزانه {len(scan_universe)} ارز نقدشونده... ممکن است کمی زمان ببرد."):
                with ThreadPoolExecutor(max_workers=6) as pool:
                    futures = [pool.submit(_scan_one_green, row) for _, row in scan_universe.iterrows()]
                    for future in futures:
                        try:
                            item = future.result()
                            if item:
                                found.append(item)
                        except Exception:
                            errors += 1
            result_df = pd.DataFrame(found)
            if not result_df.empty:
                result_df = result_df.sort_values(["Green_Days", "Streak_Change_Percent"], ascending=[False, False])
            st.session_state["green_streak_scan_results"] = result_df
            st.session_state["green_streak_scan_errors"] = errors
        green_results = st.session_state.get("green_streak_scan_results", pd.DataFrame())
        if isinstance(green_results, pd.DataFrame) and not green_results.empty:
            green_display = green_results.rename(columns={
                "Coin": "ارز", "Symbol": "نماد", "Green_Days": "روز سبز متوالی",
                "Streak_Change_Percent": "تغییر قیمت در دوره (%)",
                "Streak_Start": "شروع دوره", "Streak_End": "پایان دوره",
                "Last_Daily_Close": "آخرین بسته‌شدن روزانه", "Volume_24h": "حجم ۲۴ساعته",
            })
            st.dataframe(green_display, use_container_width=True, hide_index=True,
                         column_config={"تغییر قیمت در دوره (%)": st.column_config.NumberColumn(format="%.2f%%"),
                                        "آخرین بسته‌شدن روزانه": st.column_config.NumberColumn(format="%.8g"),
                                        "حجم ۲۴ساعته": st.column_config.NumberColumn(format="$%.2f")})
            st.success(f"{len(green_results)} ارز با حداقل ۵ کندل سبز متوالی و روند صعودی در همان دوره پیدا شد.")
        elif "green_streak_scan_results" in st.session_state:
            st.info("در ۴۰ ارز نقدشونده بررسی‌شده، موردی با حداقل ۵ کندل سبز متوالی و بازده مثبت پیدا نشد.")
        if st.session_state.get("green_streak_scan_errors", 0):
            st.caption(f"تعداد {st.session_state['green_streak_scan_errors']} درخواست تاریخی با خطا یا محدودیت منبع روبه‌رو شد؛ بنابراین این اسکن پوشش کامل بازار نیست.")

    # Market chart
    chart_source = filtered if not filtered.empty else df.head(50)
    if not chart_source.empty:
        st.subheader("🌌 نقشه مومنتوم بازار")
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

if section == "📰 اخبار و DEX":
    # News panel
    st.divider()
    st.subheader("📰 اخبار و عوامل بنیادی")
    st.caption("خبرها بدون نیاز به کلید API از RSS رسانه‌های عمومی دریافت می‌شوند؛ در صورت واردکردن کلید، CryptoPanic در اولویت است.")
    news_symbol = st.selectbox("محدوده خبر", ["ALL", "BTC", "ETH", "SOL", "XRP", "BNB", "DOGE"], index=0,
                               format_func=lambda x: "کل بازار" if x == "ALL" else x)
    fetch_news_clicked = st.button("🔄 دریافت آخرین اخبار و تحلیل بنیادی", type="primary", key="fetch_market_news")
    if fetch_news_clicked or "news_feed_cache" not in st.session_state or st.session_state.get("news_feed_symbol") != news_symbol:
        with st.spinner("در حال دریافت خبرهای بازار از منابع خبری..."):
            loaded_news, loaded_status = fetch_news(news_key_input, news_symbol)
        st.session_state["news_feed_cache"] = loaded_news
        st.session_state["news_feed_status"] = loaded_status
        st.session_state["news_feed_symbol"] = news_symbol
    news_df = st.session_state.get("news_feed_cache", pd.DataFrame())
    news_status = st.session_state.get("news_feed_status", "هنوز خبری دریافت نشده است.")
    st.caption(f"وضعیت منبع: {news_status}")
    if news_df is None or news_df.empty:
        st.warning("در حال حاضر خبری از منابع انتخاب‌شده دریافت نشد. وضعیت اتصال و پیام منبع بالا را بررسی کن.")
    else:
        # Transparent headline keyword proxy; this is not trained NLP or fact-checking.
        positive_terms = ("approval", "adoption", "partnership", "launch", "upgrade", "inflow", "bullish", "listing", "گسترش", "همکاری", "تایید", "تصویب", "رشد")
        negative_terms = ("hack", "exploit", "lawsuit", "ban", "delist", "outflow", "bearish", "scam", "breach", "هک", "حمله", "شکایت", "ممنوع", "حذف", "کلاهبرداری", "ورشکستگی")
        def headline_score(title):
            t = str(title).lower()
            return sum(w in t for w in positive_terms) - sum(w in t for w in negative_terms)
        news_df = news_df.copy()
        news_df["Sentiment"] = news_df["Title"].apply(headline_score).map(
            lambda x: "مثبتِ کلمه‌محور" if x > 0 else ("منفیِ کلمه‌محور" if x < 0 else "خنثی / نامشخص")
        )
        scores = news_df["Title"].apply(headline_score)
        pos_n, neg_n = int((scores > 0).sum()), int((scores < 0).sum())
        n1, n2, n3 = st.columns(3)
        n1.metric("تعداد خبرهای دریافتی", len(news_df))
        n2.metric("تیترهای دارای واژه مثبت", pos_n)
        n3.metric("تیترهای دارای واژه منفی", neg_n)
        if pos_n > neg_n:
            st.success("جمع‌بندی خبری: در تیترهای دریافت‌شده واژه‌های مثبت بیشتر دیده می‌شود؛ این برداشت اولیه است و باید متن خبر و منبع آن بررسی شود.")
        elif neg_n > pos_n:
            st.warning("جمع‌بندی خبری: تیترهای دارای واژه منفی بیشترند؛ ریسک خبرهای منفی را قبل از تصمیم بررسی کن.")
        else:
            st.info("جمع‌بندی خبری: تیترها از نظر واژه‌های مثبت و منفی برتری روشنی ندارند یا بخش زیادی از آن‌ها خنثی‌اند.")
        # Translate titles and summaries independently; delimiter-based combined translation
        # was unreliable because translation services sometimes modify/remove delimiters.
        news_df = news_df.copy().head(8)
        translated_titles = []
        translated_summaries = []
        with st.spinner("در حال ترجمه تیترها و خلاصه خبرها به فارسی..."):
            for _, article in news_df.iterrows():
                title_en = str(article.get("Title", "") or "")
                summary_en = str(article.get("Summary", "") or "")
                title_fa = translate_news_to_persian(title_en[:350]) if title_en else ""
                summary_fa = translate_news_to_persian(summary_en[:350]) if summary_en else ""
                translated_titles.append(title_fa or title_en)
                translated_summaries.append(summary_fa or summary_en)
        news_df["عنوان فارسی"] = translated_titles
        news_df["خلاصه فارسی"] = translated_summaries
        translated_count = sum(1 for fa, en in zip(translated_titles, news_df["Title"]) if fa and fa != en)
        st.caption(f"ترجمه فارسی: {translated_count} از {len(news_df)} تیتر ترجمه شد؛ MyMemory و در صورت نیاز Google Translate عمومی امتحان می‌شوند. حداکثر ۸ خبر تازه برای کنترل زمان و محدودیت سرویس ترجمه می‌شود؛ در صورت اختلال متن اصلی باقی می‌ماند.")
        display_news = news_df.rename(columns={"Published": "زمان انتشار", "Title": "عنوان اصلی (انگلیسی)", "Summary": "خلاصه اصلی (انگلیسی)", "Source": "منبع", "Currencies": "ارز", "Sentiment": "برداشت اولیه", "URL": "لینک"})
        keep_news = [c for c in ["زمان انتشار", "عنوان فارسی", "خلاصه فارسی", "عنوان اصلی (انگلیسی)", "منبع", "ارز", "برداشت اولیه", "لینک"] if c in display_news.columns]
        st.dataframe(display_news[keep_news], use_container_width=True, hide_index=True, column_config={"لینک": st.column_config.LinkColumn("لینک خبر")})
        st.caption("ترجمه از سرویس‌های عمومی رایگان انجام می‌شود و ممکن است محدود یا نادقیق باشد. برداشت مثبت/منفی فقط بر اساس واژه‌های تیتر است، نه تحلیل هوش مصنوعی یا راستی‌آزمایی خبر؛ اثر خبر بر قیمت قطعی نیست.")

    # DEX panel
    st.divider()
    st.subheader("🧪 جریان معاملات، فشار خرید و فروش و نشانه‌های نهنگ‌ها")
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
if section == "🐋 جریان پول و مشتقات":
    # LIVE FUNDING + OPEN INTEREST PANEL
    # =========================================================
    if data_source == "CoinGecko market" and use_bybit_derivatives:
        st.divider()
        st.subheader("📈 وضعیت بازار مشتقه: فاندینگ و سود باز")
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
    st.subheader("🧭 داده‌های تکمیلی: فعالیت نهنگ‌ها، جریان پول و حرکت‌های سریع")
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

        st.caption("برای دریافت داده‌ها، دکمه زیر را لمس کن؛ هنگام دریافت، پیام انتظار نمایش داده می‌شود. در این بخش به‌روزرسانی خودکار موقتاً متوقف است.")
        # Use Streamlit's form-submit event for a more reliable touch action on
        # mobile browsers; unlike a normal button, the browser submits the form.
        with st.form("cm_fetch_form", clear_on_submit=False):
            cm_fetch_clicked = st.form_submit_button(
                "🔄 Fetch CryptoMeter intelligence",
                type="primary",
                use_container_width=True,
                help="درخواست فیدهای رایگان و فیدهای پولی انتخاب‌شده از CryptoMeter",
            )
        if cm_fetch_clicked:
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
            with st.spinner("Requesting selected CryptoMeter feeds in parallel..."):
                job_results = _run_parallel_jobs(
                    endpoint_jobs,
                    lambda endpoint, params: fetch_cryptometer(endpoint, params, cm_key),
                    max_workers=3,
                )
                for result_key, (endpoint, _params) in endpoint_jobs.items():
                    result = job_results.get(result_key)
                    if isinstance(result, Exception):
                        collected[result_key] = {
                            "payload": None, "error": str(result), "endpoint": endpoint,
                        }
                    else:
                        collected[result_key] = {
                            "payload": result, "error": None, "endpoint": endpoint,
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
                    # Whale-flow visualization uses only provider-reported USD trade values.
                    whale_value_col = "usd_total" if "usd_total" in whale_df.columns else ("total" if "total" in whale_df.columns else None)
                    if whale_value_col and "side" in whale_df.columns:
                        whale_plot = whale_df.copy()
                        whale_plot["_usd"] = pd.to_numeric(whale_plot[whale_value_col], errors="coerce")
                        whale_plot["_side"] = whale_plot["side"].astype(str).str.upper()
                        whale_plot["_symbol"] = whale_plot.get("symbol", whale_plot.get("pair", "Unknown")).astype(str).str.upper()
                        whale_plot = whale_plot[whale_plot["_side"].isin(["BUY", "SELL"]) & whale_plot["_usd"].notna()]
                        if not whale_plot.empty:
                            whale_summary = whale_plot.groupby(["_symbol", "_side"], as_index=False)["_usd"].sum()
                            whale_summary = whale_summary.rename(columns={"_symbol": "ارز", "_side": "جهت معامله", "_usd": "ارزش معاملات نهنگ (USD)"})
                            st.markdown("**نمودار جهت حرکت نهنگ‌ها**")
                            fig_whales = px.bar(whale_summary, x="ارز", y="ارزش معاملات نهنگ (USD)", color="جهت معامله", barmode="group", title="خرید و فروش ثبت‌شده نهنگ‌ها")
                            fig_whales.update_layout(height=360, margin=dict(l=10, r=10, t=55, b=10), legend_title_text="جهت")
                            st.plotly_chart(fig_whales, use_container_width=True)
                            whale_buy = float(whale_plot.loc[whale_plot["_side"] == "BUY", "_usd"].sum())
                            whale_sell = float(whale_plot.loc[whale_plot["_side"] == "SELL", "_usd"].sum())
                            whale_net = whale_buy - whale_sell
                            if whale_net > 0:
                                st.success(f"تحلیل نهنگ‌ها: در داده‌های دریافتی، خرید بزرگ‌ها {fmt_num(whale_net, 0)} دلار بیشتر از فروش بوده است؛ این نشانه به نفع فشار خرید است، اما به‌تنهایی ورود پول به کیف‌پول‌ها یا انباشت قطعی را ثابت نمی‌کند.")
                            elif whale_net < 0:
                                st.warning(f"تحلیل نهنگ‌ها: فروش بزرگ‌ها {fmt_num(abs(whale_net), 0)} دلار بیشتر از خرید بوده است؛ فشار عرضه بالاتر است و بهتر است قبل از ورود، تثبیت قیمت بررسی شود.")
                            else:
                                st.info("تحلیل نهنگ‌ها: ارزش خرید و فروش بزرگ تقریباً برابر است؛ فعلاً جهت غالب مشخصی دیده نمی‌شود.")
                        else:
                            st.info("برای ترسیم نمودار نهنگ‌ها، داده معتبر خرید/فروش دلاری دریافت نشد.")

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
                    with st.spinner("در حال دریافت هم‌زمان حجم خرید و فروش..."):
                        buy_jobs = {
                            symbol: (symbol, buy_exchange, cm_key)
                            for symbol in dict.fromkeys(selected_buy_symbols)
                        }
                        buy_results = _run_parallel_jobs(
                            buy_jobs,
                            lambda symbol, exchange, key: fetch_cryptometer_buy_sell_volume(symbol, exchange, key),
                            max_workers=3,
                        )
                        for symbol in buy_jobs:
                            result = buy_results.get(symbol)
                            if isinstance(result, Exception):
                                actual_rows.append({
                                    "Symbol": symbol, "Pair": f"{symbol}-USDT", "Exchange": buy_exchange,
                                    "Buy volume (USDT)": np.nan, "Sell volume (USDT)": np.nan,
                                    "Net buy (USDT)": np.nan, "Buy share (%)": np.nan,
                                    "Data status": str(result)[:140]
                                })
                            else:
                                actual_rows.append(result)
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
                    st.markdown("**نمودار جریان خرید و فروش واقعی**")
                    chart_actual = valid_actual[["Symbol", "Buy volume (USDT)", "Sell volume (USDT)"]].melt(
                        id_vars="Symbol", var_name="جهت جریان", value_name="حجم (USDT)"
                    )
                    chart_actual["جهت جریان"] = chart_actual["جهت جریان"].map({
                        "Buy volume (USDT)": "خرید", "Sell volume (USDT)": "فروش"
                    })
                    fig_flow = px.bar(
                        chart_actual, x="Symbol", y="حجم (USDT)", color="جهت جریان", barmode="group",
                        title="مقایسه حجم واقعی خرید و فروش در صرافی منتخب"
                    )
                    fig_flow.update_layout(height=370, margin=dict(l=10, r=10, t=55, b=10), legend_title_text="جهت")
                    st.plotly_chart(fig_flow, use_container_width=True)
                    st.markdown("**برداشت فارسی از جریان پول**")
                    for _, flow_row in valid_actual.iterrows():
                        sym = str(flow_row["Symbol"])
                        net = float(flow_row["Net buy (USDT)"])
                        buy_share = float(flow_row["Buy share (%)"])
                        buy_usd = float(flow_row["Buy volume (USDT)"])
                        sell_usd = float(flow_row["Sell volume (USDT)"])
                        if net > 0 and buy_share >= 55:
                            reading = "غلبه روشن خریداران؛ فشار تقاضا مثبت است. اگر قیمت هم کف‌های بالاتر بسازد، می‌تواند نشانه اولیه انباشت باشد."
                        elif net > 0:
                            reading = "خرید کمی بیشتر از فروش است؛ برتری خریداران هنوز قاطع نیست و به تأیید حجم و ساختار قیمت نیاز دارد."
                        elif net < 0 and buy_share <= 45:
                            reading = "غلبه فروشندگان؛ خروج عرضه از خرید بیشتر است و ورود عجولانه ریسک بالاتری دارد."
                        elif net < 0:
                            reading = "فروش اندکی بیشتر است؛ فشار عرضه دیده می‌شود اما برای نتیجه‌گیری قطعی کافی نیست."
                        else:
                            reading = "تعادل نسبی خرید و فروش؛ جهت جریان فعلاً خنثی است."
                        st.write(f"**{sym}:** {reading} (خرید {fmt_num(buy_usd, 0)} دلار، فروش {fmt_num(sell_usd, 0)} دلار، خالص {fmt_num(net, 0)} دلار، سهم خرید {buy_share:.1f}٪).")
                    st.caption("این نمودار حجم معاملات خرید/فروش گزارش‌شده توسط صرافی را نشان می‌دهد، نه انتقال خالص دارایی بین کیف‌پول‌ها. داده فقط مربوط به جفت و صرافی انتخاب‌شده است.")

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


if section == "📁 داده‌ها":
    # Full data export
    st.divider()
    with st.expander("📋 مشاهده پیشرفته و دریافت کل داده‌های بازار", expanded=False):
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
