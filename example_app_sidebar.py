
import streamlit as st
import pandas as pd
import yfinance as yf
import base64
import os

# Page config and style
st.set_page_config(page_title="Wolf Screener", layout="wide")
st.markdown("<style>div[data-testid='column']{padding-top: 0rem;} .small-icon {cursor:pointer;}</style>", unsafe_allow_html=True)

# Load funnel icon
def load_filter_icon():
    with open("filter_icon.png", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f'<img class="small-icon" src="data:image/png;base64,{b64}" width="25" title="Toggle Column Filter" />'

# Toggle for filter
if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = False

# Logo and header
st.sidebar.image("https://i.imgur.com/yOAdO7R.png", width=180)
st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
        <img src='https://i.imgur.com/yOAdO7R.png' width='40'/>
        <h2 style='margin: 0; color: #c5a46d;'>🐺 Wolf Screener</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Load sample tickers
tickers = ["AAPL", "MSFT", "GOOG", "NVDA"]

@st.cache_data(ttl=3600)
def load_data():
    rows = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            rows.append({
                "Symbol": t,
                "Price": info.get("regularMarketPrice", 0),
                "P/E Ratio": info.get("trailingPE", 0),
                "Market Cap": "Large" if info.get("marketCap", 0) > 1e10 else "Small",
                "EPS Growth": f"{info.get('earningsQuarterlyGrowth', 0) * 100:.0f}%",
                "Sector": info.get("sector", "N/A")
            })
        except:
            continue
    return pd.DataFrame(rows)

df = load_data()

# Filter toggle UI
col1, col2 = st.columns([12, 1])
with col1:
    st.markdown("### Stock Overview")
with col2:
    if st.button(load_filter_icon(), key="funnel", help="Toggle Column Filters"):
        st.session_state["show_filters"] = not st.session_state["show_filters"]

# Column filter toggle logic
if st.session_state["show_filters"]:
    selected_cols = st.multiselect("Select columns to show", list(df.columns), default=list(df.columns))
else:
    selected_cols = list(df.columns)

# Show stock data
st.dataframe(df[selected_cols], use_container_width=True)
