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


# Load options data
df = pd.read_csv("data/options_chain.csv")


# Calculate GEX
result = calculate_gex(df)
df["gex"] = df["gamma"] * df["oi"]

# Key levels
st.subheader("🎯 Key GEX Levels")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔴 Call Wall", result["call_wall"])
col2.metric("🟢 Put Wall", result["put_wall"])
col3.metric("🟡 Gamma Flip", result["gamma_flip"])
col4.metric("🔵 Max Pain", result["max_pain"])


st.divider()


# Sigma levels
st.subheader("📐 Sigma Levels")
st.subheader("📐 Automatic GEX Levels")

levels = []

for level in result["sigma_levels"]:
    levels.append({
        "Price": level["price"],
        "Label": level["label"],
        "Type": level["type"]
    })

levels.append({
    "Price": result["call_wall"],
    "Label": "Call Wall",
    "Type": "res"
})

levels.append({
    "Price": result["put_wall"],
    "Label": "Put Wall",
    "Type": "sup"
})

levels.append({
    "Price": result["gamma_flip"],
    "Label": "Gamma Flip",
    "Type": "flip"
})

levels.append({
    "Price": result["max_pain"],
    "Label": "Max Pain",
    "Type": "mpain"
})

levels_df = pd.DataFrame(levels)

levels_df = levels_df.sort_values(
    "Price",
    ascending=False
)

st.dataframe(
    levels_df,
    use_container_width=True,
    hide_index=True
)

)

gamma_flip = result["gamma_flip"]

sigma_values = [
    3,
    2.5,
    2,
    1.5,
    1,
    0.5,
    -0.5,
    -1,
    -1.5,
    -2,
    -2.5,
    -3
]

sigma_data = []

for sigma in sigma_values:

    price = round(
        gamma_flip + (sigma_size * sigma),
        1
    )

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


# GEX Chart
st.subheader("📊 GEX Chart")

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df["strike"],
        y=df["gex"],
        name="GEX"
    )
)


fig.add_vline(
    x=result["call_wall"],
    line_width=2,
    line_dash="dash",
    annotation_text="Call Wall"
)

fig.add_vline(
    x=result["put_wall"],
    line_width=2,
    line_dash="dash",
    annotation_text="Put Wall"
)

fig.add_vline(
    x=result["gamma_flip"],
    line_width=3,
    annotation_text="Gamma Flip"
)

fig.add_vline(
    x=result["max_pain"],
    line_width=2,
    line_dash="dot",
    annotation_text="Max Pain"
)


fig.update_layout(
    xaxis_title="Strike Price",
    yaxis_title="GEX",
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Options Chain
st.subheader("📋 Options Chain")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
