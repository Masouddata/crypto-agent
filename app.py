import os
import time
import requests
import pandas as pd
import numpy as np
import plotly.express as px
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


def technical_summary(prices):
    """Indicators are computed from returned market snapshots; not a trading guarantee."""
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
    return {
        "RSI_14": round(float(latest_rsi), 2) if pd.notna(latest_rsi) else np.nan,
        "MACD": round(float(macd.iloc[-1]), 8),
        "MACD_Signal": round(float(signal.iloc[-1]), 8),
        "Trend_7d_Percent": round(float(trend), 2) if pd.notna(trend) else np.nan,
        "Technical_Score": round(score, 2),
        "Technical_Signal": signal_text,
    }


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
    prices["Time"] = pd.to_datetime(prices["timestamp_ms"], unit="ms", utc=True)
    prices["price"] = numeric(prices["price"])
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
# HEADER
# =========================================================
st.title("📡 Crypto Intelligence Scanner Pro")
st.caption("Broad market scan • Technical indicators • News context • DEX discovery • Risk flags")
st.warning(
    "Scores are screening heuristics, not calibrated probabilities or financial advice. "
    "A high score does not guarantee a pump; low-liquidity tokens can be manipulated."
)
with st.expander("📘 Quick guide — how to read the scanner", expanded=True):
    guide_a, guide_b, guide_c = st.columns(3)
    guide_a.markdown("**1. Score (0–100)**\n\nA sorting aid based on recent market movement. It is **not** the chance that a coin will pump.")
    guide_b.markdown("**2. Signal**\n\n`Early momentum candidate` means momentum looks worth checking. `Already moving — chase risk` means the price has already jumped.")
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
            index=0,
            help="More pages cover more listed coins but use more API requests and may hit rate limits.",
        )
        refresh_seconds = st.selectbox("Refresh interval", [60, 120, 300, 600], index=1)
        st_autorefresh(interval=refresh_seconds * 1000, key="scanner_refresh")
    uploaded = st.file_uploader("Upload CSV dataset", type=["csv"])
    st.divider()
    st.subheader("🔬 Technical analysis")
    technical_limit = st.selectbox(
        "Coins for detailed technical indicators",
        [0, 10, 20, 30],
        index=1,
        help="Each coin requires a historical API request. Start with 10 to reduce rate-limit risk. 0 disables detailed indicators.",
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
    min_score = st.slider("Minimum Pump Potential Score", 0, 100, 60)
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

# =========================================================
# TECHNICAL INDICATORS FOR TOP-VOLUME CANDIDATES
# =========================================================
if data_source == "CoinGecko market" and technical_limit > 0 and run_technicals:
    candidates = df.copy()
    candidates["_vol_sort"] = numeric(candidates["Volume_24h"]).fillna(0)
    candidates = candidates.sort_values("_vol_sort", ascending=False).head(technical_limit)
    results = []
    progress = st.progress(0, text="Calculating indicators...")
    for i, (_, row) in enumerate(candidates.iterrows(), start=1):
        coin_id = row.get("CoinGecko_ID")
        item = {"CoinGecko_ID": coin_id}
        try:
            hist = fetch_history(str(coin_id), currency, 7, cg_key)
            item.update(technical_summary(hist["price"]) if not hist.empty else technical_summary([]))
        except Exception as exc:
            item.update({"RSI_14": np.nan, "MACD": np.nan, "MACD_Signal": np.nan,
                         "Trend_7d_Percent": np.nan, "Technical_Score": np.nan,
                         "Technical_Signal": f"API unavailable: {str(exc)[:80]}"})
        results.append(item)
        progress.progress(i / max(1, len(candidates)), text=f"Indicators {i}/{len(candidates)}")
    progress.empty()
    tech = pd.DataFrame(results).drop_duplicates("CoinGecko_ID")
    st.session_state["scanner_technical_results"] = {"currency": currency, "data": tech.copy()}
    df = df.drop(columns=[c for c in ["RSI_14", "MACD", "MACD_Signal", "Trend_7d_Percent", "Technical_Score", "Technical_Signal"] if c in df.columns])
    df = df.merge(tech, on="CoinGecko_ID", how="left")
    # Weighted score only uses available components; missing news/technical are not fabricated.
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
            df = df.drop(columns=[c for c in ["RSI_14", "MACD", "MACD_Signal", "Trend_7d_Percent", "Technical_Score", "Technical_Signal"] if c in df.columns])
            df = df.merge(tech, on="CoinGecko_ID", how="left")
            market = numeric(df["Market_Momentum_Score"])
            tech_score = numeric(df["Technical_Score"])
            df["Pump_Potential_Score"] = np.where(
                tech_score.notna(), 0.60 * market + 0.40 * tech_score, market
            ).clip(0, 100).round(2)

# Derive risk/signal labels from market conditions; this is screening, not prediction.
ch24 = numeric(df["Change_24h_Percent"]).fillna(0)
ch7 = numeric(df["Change_7d_Percent"]).fillna(0)
vol = numeric(df["Volume_24h"]).fillna(0)
mcap = numeric(df["Market_Cap"])
df["Risk_Level"] = np.where(
    (mcap.fillna(0) < 5_000_000) | (vol < 100_000),
    "High / thin market",
    np.where((ch24 > 25) | (ch7 > 80), "High / overheated", "Medium / review")
)
df["Signal"] = np.where(
    (df["Pump_Potential_Score"] >= 75) & (ch24 < 20),
    "Early momentum candidate",
    np.where((df["Pump_Potential_Score"] >= min_score) & (ch24 >= 20),
             "Already moving — chase risk", "Watch")
)

# =========================================================
# MAIN FILTERS / KPIS
# =========================================================
st.caption(
    f"Source: {dataset_name} • Rows loaded: {len(df):,} • "
    f"Display refreshed: {pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%d %H:%M:%S UTC')}"
)
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
filtered = filtered[numeric(filtered["Pump_Potential_Score"]).fillna(0) >= min_score]

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
f.metric("🚀 Early momentum candidates", int((df["Signal"] == "Early momentum candidate").sum()))
g.metric("⚠️ High-risk / overheated", int(df["Risk_Level"].astype(str).str.startswith("High").sum()))

st.divider()
st.subheader("🚀 Candidates worth reviewing")
st.caption("Start with the short list, then inspect the supporting numbers. These are screening results, not buy/sell instructions.")
if not filtered.empty:
    ranked = filtered.sort_values("Pump_Potential_Score", ascending=False).copy()
    top_three = ranked.head(3)
    card_cols = st.columns(3)
    for i, (_, coin_row) in enumerate(top_three.iterrows()):
        with card_cols[i]:
            st.markdown(f"### {str(coin_row.get('Coin', 'Unknown'))} ({str(coin_row.get('Symbol', '')).upper()})")
            st.metric("Screening score", f"{fmt_num(coin_row.get('Pump_Potential_Score'), 0)} / 100")
            change = numeric(pd.Series([coin_row.get('Change_24h_Percent')])).iloc[0]
            st.metric("Change in 24 hours", f"{fmt_num(change)}%" if pd.notna(change) else "N/A")
            st.caption(f"Signal: {coin_row.get('Signal', 'Watch')}\n\nRisk: {coin_row.get('Risk_Level', 'Unassessed')}")
    with st.expander("📊 Detailed candidate table", expanded=True):
        preferred_cols = [
            "Coin", "Symbol", "Price", "Change_24h_Percent", "Change_7d_Percent",
            "Volume_24h", "Market_Cap_Rank", "Market_Momentum_Score", "RSI_14",
            "Technical_Score", "Pump_Potential_Score", "Signal", "Risk_Level", "Technical_Signal",
        ]
        cols = [c for c in preferred_cols if c in ranked.columns]
        display_names = {
            "Coin": "Coin", "Symbol": "Ticker", "Price": f"Price ({currency.upper()})",
            "Change_24h_Percent": "24h change (%)", "Change_7d_Percent": "7d change (%)",
            "Volume_24h": f"24h volume ({currency.upper()})", "Market_Cap_Rank": "Market rank",
            "Market_Momentum_Score": "Market score", "RSI_14": "RSI (14)",
            "Technical_Score": "Technical score", "Pump_Potential_Score": "Screening score",
            "Signal": "Signal / interpretation", "Risk_Level": "Risk flag", "Technical_Signal": "Technical reading",
        }
        display_df = ranked[cols].rename(columns=display_names)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.caption("RSI is typically interpreted from 0–100: readings above 70 can indicate an overheated move; below 30 can indicate a heavily sold market. Context matters.")
else:
    st.info("No candidates match the current filters. Lower the minimum score or broaden the market coverage.")

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
        color_continuous_scale="Turbo", template="plotly_dark",
        labels={"Change_24h_Percent": "24h change (%)", "Change_7d_Percent": "7d change (%)", "Pump_Potential_Score": "Pump Potential Score"},
    )
    fig.update_layout(paper_bgcolor="#0b1020", plot_bgcolor="#0b1020", height=520)
    st.plotly_chart(fig, use_container_width=True)

# Historical chart
st.divider()
st.subheader("📈 Price history")
if data_source == "CoinGecko market" and "CoinGecko_ID" in df.columns:
    hist_candidates = df.dropna(subset=["CoinGecko_ID"]).copy()
    if not hist_candidates.empty:
        hist_candidates["_opt"] = hist_candidates["Symbol"].astype(str) + " — " + hist_candidates["Coin"].astype(str)
        choice = st.selectbox("Select coin for price history", hist_candidates["_opt"].tolist())
        selected = hist_candidates[hist_candidates["_opt"] == choice].iloc[0]
        hist_days = st.selectbox("History range", [1, 7, 30, 90], index=1)
        if st.button("Load price chart"):
            try:
                hist = fetch_history(str(selected["CoinGecko_ID"]), currency, hist_days, cg_key)
                if hist.empty:
                    st.info("No price history returned.")
                else:
                    fig_hist = px.line(hist, x="Time", y="price", title=f"{choice} — {hist_days} day price history", template="plotly_dark")
                    fig_hist.update_layout(paper_bgcolor="#0b1020", plot_bgcolor="#0b1020", yaxis_title=f"Price ({currency.upper()})")
                    st.plotly_chart(fig_hist, use_container_width=True)
            except Exception as exc:
                st.error(f"History API error: {exc}")

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
    "News requires an optional CryptoPanic token. This tool is informational only."
)


