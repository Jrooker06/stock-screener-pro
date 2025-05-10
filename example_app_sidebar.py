
import streamlit as st
import pandas as pd
import yfinance as yf
import base64
import filters_sidebar_grouped_dynamic as filters_sidebar

# Page config
st.set_page_config(page_title="Wolf Screener", layout="wide")
st.markdown("<style>div[data-testid='column']{padding-top: 0rem;} .small-icon {cursor:pointer;}</style>", unsafe_allow_html=True)

# Funnel toggle
if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = False

# Inline funnel icon
funnel_icon_b64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAB+UlEQVR4nO3cwW3DMBQE0WGQslS++mLOCYzEdkRyPrVTgGDgYcmDLbfeO8nTx+oPkL4XEFkBkRUQWQGRFRBZAZEVEFkBkRUQWQGRFRBZAZEVEFkBkRUQWQGRFRBZAZH1efUDW2u3+5K+996uelYb8SOH1lo/juPy59o6z/NSDMiR9XYjMGAQSO+9nec54tHbN2whO6OMWgcMPrJ2RBmJAblDXmo0BkwA2XElI5uykB1QZqwDJh5ZlVFmYUDukD+biQGTQSqvZFbTF1IJZfY6YNGRVQFlBQbkDnnYKgxYCFJhJStauhAjysp1gODIMqGsxgABiCUDBkhATCtZnQIE1qJY1gEiEFiDYsIAGcjsbBggBLn7faIDgTkoxnWAFATGolgxQAwyKjMGyEHueJ+oQeBaFPs6oAAIXINSAQOKgPy3KhhQCOQu90kZEHgPpdI6oBgIvIZSDQMKgjxbRQwoCrLzfVISBH5HqboOKAwCj1EqY0BxkJ9Vx4ANQHa7T4a8Fj26V96Fr7aYy/84YFbPvAdfcTnlj6zdCoisgMgKiKyAyAqIrIDICoisgMgKiKyAyAqIrIDICoisgMgKiKyAyAqIrIDICoisgMgKiKyAyMoP5WSVBNm5HFmyAiIrILICIisgsgIiKyCyAiIrILICIisgsgIiKyCyvgAjgE34KfdpNgAAAABJRU5ErkJggg=="

def filter_icon():
    return f'<img class="small-icon" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAB+UlEQVR4nO3cwW3DMBQE0WGQslS++mLOCYzEdkRyPrVTgGDgYcmDLbfeO8nTx+oPkL4XEFkBkRUQWQGRFRBZAZEVEFkBkRUQWQGRFRBZAZEVEFkBkRUQWQGRFRBZAZH1efUDW2u3+5K+996uelYb8SOH1lo/juPy59o6z/NSDMiR9XYjMGAQSO+9nec54tHbN2whO6OMWgcMPrJ2RBmJAblDXmo0BkwA2XElI5uykB1QZqwDJh5ZlVFmYUDukD+biQGTQSqvZFbTF1IJZfY6YNGRVQFlBQbkDnnYKgxYCFJhJStauhAjysp1gODIMqGsxgABiCUDBkhATCtZnQIE1qJY1gEiEFiDYsIAGcjsbBggBLn7faIDgTkoxnWAFATGolgxQAwyKjMGyEHueJ+oQeBaFPs6oAAIXINSAQOKgPy3KhhQCOQu90kZEHgPpdI6oBgIvIZSDQMKgjxbRQwoCrLzfVISBH5HqboOKAwCj1EqY0BxkJ9Vx4ANQHa7T4a8Fj26V96Fr7aYy/84YFbPvAdfcTnlj6zdCoisgMgKiKyAyAqIrIDICoisgMgKiKyAyAqIrIDICoisgMgKiKyAyAqIrIDICoisgMgKiKyAyMoP5WSVBNm5HFmyAiIrILICIisgsgIiKyCyAiIrILICIisgsgIiKyCyvgAjgE34KfdpNgAAAABJRU5ErkJggg==" width="25" title="Toggle Column Filters" />'

# Sidebar wolf logo
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=180)

# Header logo
st.markdown(
    """
    <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
        <img src='https://cdn-icons-png.flaticon.com/512/616/616408.png' width='40'/>
        <h2 style='margin: 0; color: #c5a46d;'>🐺 Wolf Screener</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Sample tickers
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

# Sidebar filters
filters_sidebar.show_sidebar_filters(df)

# Column toggle icon
col1, col2 = st.columns([12, 1])
with col1:
    st.markdown("### Stock Overview")
with col2:
    if st.button(filter_icon(), key="funnel_toggle", help="Toggle Column Filters"):
        st.session_state["show_filters"] = not st.session_state["show_filters"]

# Column filter UI
if st.session_state["show_filters"]:
    selected_cols = st.multiselect("Select columns to show", list(df.columns), default=list(df.columns))
else:
    selected_cols = list(df.columns)

# Filtered stock data table
st.dataframe(df[selected_cols], use_container_width=True)
