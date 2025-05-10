
import streamlit as st
import pandas as pd
import filters_sidebar_grouped_dynamic as filters_sidebar
import os
import json

PRESETS_DIR = "filter_presets"
os.makedirs(PRESETS_DIR, exist_ok=True)

# Sample data
data = {
    "Exchange": ["NYSE", "NASDAQ"],
    "Country": ["USA", "China"],
    "Market Cap": ["Large", "Small"],
    "Price": [100, 20],
    "P/E Ratio": ["15", "30"],
    "P/B Ratio": ["2", "5"],
    "PEG Ratio": ["1.5", "3"],
    "EPS Growth (YoY)": ["10%", "-5%"],
    "Revenue Growth (YoY)": ["20%", "5%"],
    "EPS Growth This Year": ["-10%", "15%"],
    "EPS Growth qtr over qtr": ["0%", "25%"],
    "Short Float": ["Low", "High"],
    "Float": ["Under 10M", "Over 50M"],
    "Float Rotation": ["1x-10x", "Over 10x"],
    "Gap": ["Up", "Down"],
    "Change From Open": ["Up", "Down"],
    "Performance": ["Today Up", "Month Down"],
    "Performance 2": ["Week Up", "Week Down"],
    "SMA20": ["Price below", "Price above"],
    "SMA50": ["Price above", "Price below"],
    "SMA200": ["Crossed", "Price below"],
    "EMA 9": ["Above", "Below"],
    "RSI (14)": ["Overbought", "Oversold"],
    "ATR": ["Over 0.25", "Under 0.5"],
    "IPO Date": ["Today", "Last year"],
    "Number of Trades": [5000, 30000]
}

df = pd.DataFrame(data)

st.set_page_config(layout="wide")
st.title("📈 Stock Screener - PREMIUM PRO V2")

# Show filters
filters_sidebar.show_sidebar_filters(df)

# Column selector
st.sidebar.subheader("🧩 Column Filter")
all_columns = list(df.columns)
default_cols = st.session_state.get("selected_columns", all_columns[:10])
selected_cols = st.multiselect("Select columns to display", all_columns, default=default_cols, key="selected_columns")

# Apply filters
filtered_df = df.copy()

# List of simple equality-based filters
simple_filters = [
    "Exchange", "Country", "Market Cap", "Short Float", "Float",
    "Float Rotation", "Gap", "Change From Open", "Performance",
    "Performance 2", "SMA20", "SMA50", "SMA200", "EMA 9",
    "RSI (14)", "ATR", "IPO Date"
]

for key in simple_filters:
    user_input = st.session_state.get(f"filter_{key.lower().replace(' ', '_')}")
    if user_input and user_input != "Any":
        filtered_df = filtered_df[filtered_df[key] == user_input]


# Numeric filters (Price and Number of Trades)
price_low = st.session_state.get("filter_price_low", 0)
price_high = st.session_state.get("filter_price_high", 0)
if price_low and price_high:
    filtered_df = filtered_df[
        (filtered_df["Price"].astype(float) >= float(price_low)) &
        (filtered_df["Price"].astype(float) <= float(price_high))
    ]

trades_range = st.session_state.get("filter_trades", (0, 50000))
if trades_range:
    filtered_df = filtered_df[
        (filtered_df["Number of Trades"].astype(int) >= trades_range[0]) &
        (filtered_df["Number of Trades"].astype(int) <= trades_range[1])
    ]

# Show filtered data

st.header("Stock Data")
st.dataframe(filtered_df[selected_cols], use_container_width=True)
