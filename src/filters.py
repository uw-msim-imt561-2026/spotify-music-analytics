import streamlit as st
import pandas as pd

def render_filters(df: pd.DataFrame) -> pd.DataFrame:

    # Ensure release_year exists
    if "release_year" not in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        df["release_year"] = df["release_date"].dt.year

    st.sidebar.header("Dashboard Filters")

    # --- Key Dropdown ---
    keys_with_none = ["None"] + sorted(df["key"].dropna().unique())
    selected_key = st.sidebar.selectbox(
        "Select Musical Key",
        options=keys_with_none,
        index=0
    )


    # --- Stream Count Slider ---
    min_stream = int(df["stream_count"].min())
    max_stream = int(df["stream_count"].max())
    stream_range = st.sidebar.slider(
        "Stream Count Range",
        min_stream,
        max_stream,
        (min_stream, max_stream)
    )

    # --- Release Year Slider ---
    min_year = int(df["release_year"].min())
    max_year = int(df["release_year"].max())
    year_range = st.sidebar.slider(
        "Release Year Range",
        min_year,
        max_year,
        (min_year, max_year)
    )

    # --- Country Filter ---
    selected_country = st.sidebar.multiselect(
        "Select Country",
        options=sorted(df["country"].dropna().unique()),
        default=df["country"].unique()
    )

    # --- Apply filters ---
    filtered_df = df[
        (df["key"] == selected_key) &
        (df["stream_count"] >= stream_range[0]) &
        (df["stream_count"] <= stream_range[1]) &
        (df["release_year"] >= year_range[0]) &
        (df["release_year"] <= year_range[1]) &
        (df["country"].isin(selected_country))
    ]

    return filtered_df
