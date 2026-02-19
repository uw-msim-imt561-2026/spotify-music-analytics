import pandas as pd
import streamlit as st


def render_filters(df: pd.DataFrame) -> pd.DataFrame:
    if "release_year" not in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        df["release_year"] = df["release_date"].dt.year

    st.sidebar.header("Filters")

    # --- Year slider ---
    min_year = int(df["release_year"].min())
    max_year = int(df["release_year"].max())

    selected_years = st.sidebar.slider(
        "Release Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )

    filtered_df = df[
        (df["release_year"] >= selected_years[0]) &
        (df["release_year"] <= selected_years[1])
    ]

    return filtered_df
