
import streamlit as st
import pandas as pd
import yfinance as yf
import base64
import filters_sidebar_grouped_dynamic as filters_sidebar

st.set_page_config(page_title="Wolf Screener", layout="wide")
st.markdown("<style>div[data-testid='column']{padding-top: 0rem;} .small-icon {cursor:pointer;}</style>", unsafe_allow_html=True)

# Base64 funnel icon
def load_funnel_icon():
    return "iVBORw0KGgoAAAANSUhEUgAAADIA..."  # placeholder for valid base64

if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = False

def filter_icon():
    return f'<img class="small-icon" src="data:image/png;base64,{load_funnel_icon()}" width="25" title="Toggle Column Filters" />'

wolf_url = "https://cdn-icons-png.flaticon.com/512/616/616408.png"
st.sidebar.image(wolf_url, width=180)

st.markdown(
    f"""
    <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
        <img src='{wolf_url}' width='40'/>
        <h2 style='margin: 0; color: #c5a46d;'>Wolf Screener</h2>
    </div>
    """,
    unsafe_allow_html=True
)

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
                "Market Cap": round(info.get("marketCap", 0) / 1e9, 2),
                "EPS Growth": f"{info.get('earningsQuarterlyGrowth', 0) * 100:.0f}%",
                "Sector": info.get("sector", "N/A")
            })
        except:
            continue
    return pd.DataFrame(rows)

df = load_data()
filters_sidebar.show_sidebar_filters(df)

col1, col2 = st.columns([12, 1])
with col1:
    st.markdown("### Stock Overview")
with col2:
    if st.button("🧩 Toggle Filters"):
        st.session_state["show_filters"] = not st.session_state["show_filters"]

if st.session_state["show_filters"]:
    selected_cols = st.multiselect("Select columns to show", list(df.columns), default=list(df.columns))
else:
    selected_cols = list(df.columns)

st.dataframe(df[selected_cols], use_container_width=True)
