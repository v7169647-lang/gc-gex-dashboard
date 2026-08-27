import pandas as pd

def calculate_gex(df):
    df["gex"] = df["gamma"] * df["oi"]

    call_wall = df.loc[df["gex"].idxmax(), "strike"]
    put_wall = df.loc[df["gex"].idxmin(), "strike"]

    total_gex = df["gex"].sum()

    return {
        "call_wall": call_wall,
        "put_wall": put_wall,
        "total_gex": total_gex
    }
