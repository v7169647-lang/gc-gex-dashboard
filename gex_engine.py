import pandas as pd
import numpy as np


def calculate_gex(df):
    df = df.copy()

    # GEX
    df["gex"] = df["gamma"] * df["oi"]

    # Call / Put walls
    call_data = df[df["type"].str.upper() == "C"]
    put_data = df[df["type"].str.upper() == "P"]

    if len(call_data) > 0:
        call_wall = call_data.loc[
            call_data["gex"].idxmax(), "strike"
        ]
    else:
        call_wall = df.loc[df["gex"].idxmax(), "strike"]

    if len(put_data) > 0:
        put_wall = put_data.loc[
            put_data["gex"].idxmin(), "strike"
        ]
    else:
        put_wall = df.loc[df["gex"].idxmin(), "strike"]

    total_gex = df["gex"].sum()

    # Gamma Flip
    gamma_flip = calculate_gamma_flip(df)

    # Max Pain
    max_pain = calculate_max_pain(df)

    # Sigma
    sigma_size = calculate_sigma_size(df, gamma_flip)

    sigma_levels = generate_sigma_levels(
        gamma_flip,
        sigma_size
    )

    return {
        "call_wall": float(call_wall),
        "put_wall": float(put_wall),
        "gamma_flip": float(gamma_flip),
        "max_pain": float(max_pain),
        "total_gex": float(total_gex),
        "sigma_size": float(sigma_size),
        "sigma_levels": sigma_levels
    }


def calculate_gamma_flip(df):
    temp = df.copy()
    temp = temp.sort_values("strike")

    temp["gex"] = temp["gamma"] * temp["oi"]
    temp["cum_gex"] = temp["gex"].cumsum()

    for i in range(1, len(temp)):

        previous = temp.iloc[i - 1]["cum_gex"]
        current = temp.iloc[i]["cum_gex"]

        if previous == 0:
            return temp.iloc[i - 1]["strike"]

        if (previous < 0 and current > 0) or \
           (previous > 0 and current < 0):

            return temp.iloc[i]["strike"]

    return temp["strike"].median()


def calculate_max_pain(df):
    strikes = sorted(df["strike"].unique())

    min_payout = float("inf")
    max_pain = strikes[0]

    for price in strikes:

        payout = 0

        for _, row in df.iterrows():

            strike = row["strike"]
            oi = row["oi"]
            option_type = str(row["type"]).upper()

            if option_type == "C":
                payout += max(price - strike, 0) * oi

            elif option_type == "P":
                payout += max(strike - price, 0) * oi

        if payout < min_payout:
            min_payout = payout
            max_pain = price

    return max_pain


def calculate_sigma_size(df, gamma_flip):
    """
    Automatically estimate 1σ distance
    from the strike distribution.
    """

    strikes = df["strike"].astype(float)

    distance = np.abs(strikes - gamma_flip)

    sigma = distance.median()

    if sigma <= 0:
        sigma = (strikes.max() - strikes.min()) / 12

    return round(sigma, 1)


def generate_sigma_levels(gamma_flip, sigma_size):

    levels = []

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

    for sigma in sigma_values:

        price = round(
            gamma_flip + sigma * sigma_size,
            1
        )

        if sigma > 0:
            label = f"+{sigma}σ"
            level_type = "opu"
        else:
            label = f"{sigma}σ"
            level_type = "opd"

        levels.append({
            "price": price,
            "label": label,
            "type": level_type
        })

    return levels
