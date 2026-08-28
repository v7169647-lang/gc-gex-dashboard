import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from gex_engine import calculate_gex

st.set_page_config(
    page_title="GC Gold GEX",
    page_icon="🟡",
    layout="wide"
)

st.title("🟡 GC Gold GEX Dashboard")
st.caption("COMEX Gold Futures Options — GEX Analysis")

# Load data

uploaded_file = st.file_uploader(
    "Upload Options Chain File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

else:
    st.info("Please upload a CSV or Excel file.")
    st.stop()

# Calculate GEX
result = calculate_gex(df)
