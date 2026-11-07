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
