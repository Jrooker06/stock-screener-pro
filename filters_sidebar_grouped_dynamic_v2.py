
import streamlit as st

def show_sidebar_filters(df):
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=180)

    st.sidebar.markdown("### 📌 Filters")

    preset_name = st.sidebar.text_input("Preset Name")
    if st.sidebar.button("💾 Save"):
        st.session_state["saved_preset"] = preset_name

    if "saved_preset" in st.session_state:
        st.sidebar.selectbox("📂 Load Preset", [st.session_state["saved_preset"]])
        st.sidebar.button("📥 Load")

    st.sidebar.markdown("### Category")
    category = st.sidebar.radio(
        "Select filter category",
        ("All", "Descriptive", "Fundamental", "Growth", "Technical", "News", "Volume/Rotation", "Performance", "Other")
    )

    if category == "Other":
        st.sidebar.markdown("#### Other")
        st.sidebar.slider("Number of Trades", 0, 50000, (0, 50000))
