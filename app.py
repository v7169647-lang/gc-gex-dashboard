import streamlit as st
import pandas as pd

from gex_engine import calculate_gex

st.set_page_config(
    page_title="GC Gold GEX",
    page_icon="🟡",
    layout="wide"
)

st.title("🟡 GC Gold GEX Dashboard")
st.caption("Gold Futures Options — GEX Calculator")

# Load options data
df = pd.read_csv("data/options_chain.csv")

# Calculate GEX
result = calculate_gex(df)

# Main levels
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Call Wall",
    result["call_wall"]
)

col2.metric(
    "Put Wall",
    result["put_wall"]
)

col3.metric(
    "Gamma Flip",
    result["gamma_flip"]
)

col4.metric(
    "Max Pain",
    result["max_pain"]
)

st.divider()

# Total GEX
st.metric(
    "Total GEX",
    round(result["total_gex"], 2)
)

st.subheader("📊 Options Chain")

st.dataframe(
    df,
    use_container_width=True
)
