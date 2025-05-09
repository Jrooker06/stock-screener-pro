
"""
filters_sidebar_premium_pro.py

Premium PRO VERSION with:
- Smart Tabs
- Collapsible Subgroups
- Under/Over style Filters and Dropdowns
- Save/Load Presets
"""

import streamlit as st
import json
import os

PRESETS_DIR = "filter_presets"
os.makedirs(PRESETS_DIR, exist_ok=True)

def save_preset(preset_name):
    preset_data = {key: st.session_state[key] for key in st.session_state.keys()}
    with open(os.path.join(PRESETS_DIR, f"{preset_name}.json"), "w") as f:
        json.dump(preset_data, f)
    st.success(f"Preset '{preset_name}' saved.")

def load_preset(preset_name):
    file_path = os.path.join(PRESETS_DIR, f"{preset_name}.json")
    if not os.path.exists(file_path):
        st.error("Preset not found.")
        return
    with open(file_path, "r") as f:
        preset_data = json.load(f)
    for key, value in preset_data.items():
        st.session_state[key] = value
    st.success(f"Preset '{preset_name}' loaded.")

def selectbox_with_options(label, options, key):
    return st.selectbox(label, ["Any"] + options, key=key)

def has_columns(df, columns):
    return any(col in df.columns for col in columns)

def show_sidebar_filters(df):
    st.sidebar.header("📌 Filters")

    # Presets
    preset_col1, preset_col2 = st.sidebar.columns(2)
    with preset_col1:
        save_name = st.text_input("Preset Name")
    with preset_col2:
        if st.button("💾 Save"):
            save_preset(save_name)

    presets = [f.replace(".json", "") for f in os.listdir(PRESETS_DIR) if f.endswith(".json")]
    selected_preset = st.sidebar.selectbox("📂 Load Preset", presets)
    if st.sidebar.button("📥 Load"):
        load_preset(selected_preset)

    # Tabs
    categories = ["All", "Descriptive", "Fundamental", "Growth", "Technical", "News", "Volume/Rotation", "Performance", "Other"]
    tab = st.sidebar.radio("Category", categories)

    # Descriptive
    if tab == "Descriptive":
        with st.sidebar.expander("General"):
            if "Exchange" in df.columns:
                selectbox_with_options("Exchange", list(df["Exchange"].unique()), "filter_exchange")
            if "Country" in df.columns:
                selectbox_with_options("Country", list(df["Country"].unique()) + ["China"], "filter_country")

    # Fundamental
    if tab == "Fundamental":
        with st.sidebar.expander("Market Cap & Price"):
            selectbox_with_options("Market Cap", ["Mega", "Large", "Mid", "Small", "Micro", "Nano"], "filter_market_cap")
            st.number_input("Price Low", min_value=0.0, value=0.0, step=0.5, key="filter_price_low")
            st.number_input("Price High", min_value=0.0, value=0.0, step=0.5, key="filter_price_high")

        with st.sidebar.expander("Valuation Ratios"):
            selectbox_with_options("P/E Ratio", ["Under 10", "10-20", "20-30", "Over 30"], "filter_pe_ratio")
            selectbox_with_options("P/B Ratio", ["Under 1", "1-2", "2-3", "Over 3"], "filter_pb_ratio")
            selectbox_with_options("PEG Ratio", ["Under 1", "1-2", "Over 2"], "filter_peg_ratio")

    # Growth
    if tab == "Growth":
        with st.sidebar.expander("Growth Rates"):
            selectbox_with_options("EPS Growth (YoY)", ["Negative", "0-10%", "10-20%", "Over 20%"], "filter_eps_growth")
            selectbox_with_options("Revenue Growth (YoY)", ["Negative", "0-10%", "10-20%", "Over 20%"], "filter_revenue_growth")
            selectbox_with_options("EPS Growth This Year", ["Negative", "0-10%", "10-20%", "Over 20%"], "filter_eps_this_year")
            selectbox_with_options("EPS Growth qtr over qtr", ["Negative", "0-10%", "10-20%", "Over 20%"], "filter_eps_qoq")

    # Technical
    if tab == "Technical":
        with st.sidebar.expander("Moving Averages"):
            selectbox_with_options("SMA20", ["Price Below", "Price Above", "Crossed"], "filter_sma20")
            selectbox_with_options("SMA50", ["Price Below", "Price Above", "Crossed"], "filter_sma50")
            selectbox_with_options("SMA200", ["Price Below", "Price Above", "Crossed"], "filter_sma200")
            selectbox_with_options("EMA 9", ["Above", "Below"], "filter_ema9")

        with st.sidebar.expander("Indicators"):
            selectbox_with_options("RSI (14)", ["Oversold", "Overbought", "Neutral"], "filter_rsi")
            selectbox_with_options("ATR", ["Over 0.25", "Over 0.5", "Over 1", "Under 1"], "filter_atr")

    # News
    if tab == "News":
        with st.sidebar.expander("IPO Date"):
            selectbox_with_options("IPO Date", ["Today", "Last Week", "Last Year", "Over 5 Years"], "filter_ipo_date")

    # Volume and Rotation
    if tab == "Volume/Rotation":
        with st.sidebar.expander("Volume & Float"):
            selectbox_with_options("Float", ["Under 5M", "5M-10M", "Over 50M"], "filter_float")
            selectbox_with_options("Short Float", ["Under 5%", "5-10%", "Over 10%"], "filter_short_float")
            selectbox_with_options("Float Rotation", ["1x-10x", "Over 10x"], "filter_float_rotation")

    # Performance
    if tab == "Performance":
        with st.sidebar.expander("Performance"):
            selectbox_with_options("Performance", ["Today Up", "Today Down", "Week Up", "Week Down", "Month Up", "Month Down"], "filter_performance")
            selectbox_with_options("Performance 2", ["Today Up", "Today Down", "Week Up", "Week Down", "Month Up", "Month Down"], "filter_performance2")
            selectbox_with_options("Gap", ["Up", "Up 1%", "Down", "Down 1%"], "filter_gap")
            selectbox_with_options("Change From Open", ["Up", "Up 1%", "Down", "Down 1%"], "filter_change_open")

    # Other
    with st.sidebar.expander("Other"):
        # Number of Trades moved into Other
        st.slider("Number of Trades", min_value=0, max_value=50000, value=(0, 50000), step=100, key="filter_trades")

    st.sidebar.markdown("---")
    st.sidebar.button("Reset Filters")
