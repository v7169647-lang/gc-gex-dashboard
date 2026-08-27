import pandas as pd
import numpy as np


def calculate_gex(df):
    df = df.copy()

    df["gex"] = df["gamma"] * df["oi"]

    call_wall = df.loc[df["gex"].idxmax(), "strike"]
    put_wall = df.loc[df["gex"].idxmin(), "strike"]

    total_gex = df["gex"].sum()

    gamma_flip = calculate_gamma_flip(df)
    max_pain = calculate_max_pain(df)

    return {
        "call_wall": float(call_wall),
        "put_wall": float(put_wall),
        "gamma_flip": float(gamma_flip),
        "max_pain": float(max_pain),
        "total_gex": float(total_gex)
    }


def calculate_gamma_flip(df):
    temp = df.copy()
    temp = temp.sort_values("strike")

    temp["gex"] = temp["gamma"] * temp["oi"]
    temp["cum_gex"] = temp["gex"].cumsum()

    signs = np.sign(temp["cum_gex"])

    for i in range(1, len(temp)):
        if signs.iloc[i] != signs.iloc[i - 1]:
            return temp.iloc[i]["strike"]

    return temp["strike"].median()


def calculate_max_pain(df):
    strikes = sorted(df["strike"].unique())

    min_payout = None
    max_pain = None

    for price in strikes:

        total_payout = 0

        for _, row in df.iterrows():

            strike = row["strike"]
            oi = row["oi"]
            opt_type = row["type"]

            if opt_type == "C":
                payout = max(0, price - strike) * oi
            else:
                payout = max(0, strike - price) * oi

            total_payout += payout

        if min_payout is None or total_payout < min_payout:
            min_payout = total_payout
            max_pain = price

    return max_pain


def generate_sigma_levels(gamma_flip, sigma_size):
    levels = []

    sigmas = [
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

    for s in sigmas:
        price = round(
            gamma_flip + (sigma_size * s),
            1
        )

        levels.append({
            "price": price,
            "sigma": s
        })

    return levels
