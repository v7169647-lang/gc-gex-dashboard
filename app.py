import streamlit as st
import pandas as pd
from gex_engine import calculate_gex
import streamlit as st
import pandas as pd

from gex_engine import calculate_gex

st.set_page_config(
    page_title="GC Gold GEX",
    layout="wide"
)

st.title("🟡 GC Gold GEX Dashboard")

df = pd.read_csv("data/options_chain.csv")

result = calculate_gex(df)

c1, c2, c3 = st.columns(3)

c1.metric("Call Wall", result["call_wall"])
c2.metric("Put Wall", result["put_wall"])
c3.metric("Total GEX", round(result["total_gex"], 2))

st.dataframe(df)
