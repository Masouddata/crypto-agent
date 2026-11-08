import os
import time
import threading
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
