
import streamlit as st
import pandas as pd
import filters_sidebar_grouped_dynamic as filters_sidebar

# Example dataset for testing
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

st.title("📈 Stock Screener - PREMIUM PRO V2 VERSION")

filters_sidebar.show_sidebar_filters(df)

st.header("Stock Data")
st.dataframe(df)
