import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from gex_engine import calculate_gex, generate_sigma_levels


st.set_page_config(
    page_title="GC Gold GEX",
    page_icon="🟡",
    layout="wide"
)


st.title("🟡 GC Gold GEX Dashboard")
st.caption("COMEX Gold Futures Options — GEX Analysis")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("data/options_chain.csv")

result = calculate_gex(df)


# --------------------------------------------------
# MAIN LEVELS
# --------------------------------------------------

st.subheader("🎯 Key GEX Levels")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🔴 Call Wall",
    result["call_wall"]
)

col2.metric(
    "🟢 Put Wall",
    result["put_wall"]
)

col3.metric(
    "🟡 Gamma Flip",
    result["gamma_flip"]
)

col4.metric(
    "🔵 Max Pain",
    result["max_pain"]
)


st.divider()


# --------------------------------------------------
# SIGMA LEVELS
# --------------------------------------------------

st.subheader("📐 Sigma Levels")

sigma_size = st.number_input(
    "Sigma Distance",
    min_value=0.1,
    value=20.7,
    step=0.1
)

sigma_levels = generate_sigma_levels(
    result["gamma_flip"],
    sigma_size
)


sigma_data = []

for level in sigma_levels:

    sigma = level["sigma"]
    price = level["price"]

    if sigma > 0:
        label = f"+{sigma}σ"
    else:
        label = f"{sigma}σ"

    sigma_data.append({
        "Price": price,
        "Level": label
    })


sigma_df = pd.DataFrame(sigma_data)

st.dataframe(
    sigma_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# --------------------------------------------------
# GEX CHART
# --------------------------------------------------

st.subheader("📊 GEX Levels Chart")


fig = go.Figure()


# Option GEX bars

fig.add_trace(
    go.Bar(
        x=df["strike"],
        y=df["gex"],
        name="GEX"
    )
)


# Call Wall

fig.add_vline(
    x=result["call_wall"],
    line_width=2,
    line_dash="dash",
    annotation_text="Call Wall"
)


# Put Wall

fig.add_vline(
    x=result["put_wall"],
    line_width=2,
    line_dash="dash",
    annotation_text="Put Wall"
)


# Gamma Flip

fig.add_vline(
    x=result["gamma_flip"],
    line_width=3,
    line_dash="solid",
    annotation_text="Gamma Flip"
)


# Max Pain

fig.add_vline(
    x=result["max_pain"],
    line_width=2,
    line_dash="dot",
    annotation_text="Max Pain"
)


fig.update_layout(
    xaxis_title="Strike Price",
    yaxis_title="Gamma Exposure",
    height=600,
    hovermode="x unified"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------------------------
# OPTIONS DATA
# --------------------------------------------------

st.subheader("📋 Options Chain")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
