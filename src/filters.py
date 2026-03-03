import streamlit as st
import pandas as pd


def render_filters(df: pd.DataFrame) -> pd.DataFrame:

    if "release_year" not in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        df["release_year"] = df["release_date"].dt.year

    st.sidebar.header("Dashboard Filters")

    # --- Key Dropdown ---
    keys_with_all = ["All"] + sorted(df["key"].dropna().unique())
    selected_key = st.sidebar.selectbox(
        "Select Musical Key",
        options=keys_with_all,
        index=0
    )

    # --- Stream Count Slider ---
    min_stream = int(df["stream_count"].min())
    max_stream = int(df["stream_count"].max())

    stream_range = st.sidebar.slider(
        "Stream Count Range",
        min_value=min_stream,
        max_value=max_stream,
        value=(min_stream, max_stream),
        step=1000000
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

    # --- Country Filter with Select All ---
    country_options = sorted(df["country"].dropna().unique())
    select_all = st.sidebar.checkbox("Select All Countries", value=True)

    if select_all:
        selected_country = country_options
    else:
        selected_country = st.sidebar.multiselect(
            "Select Country",
            options=country_options
        )

    # --- Genre Filter with Select All ---
    all_genres = sorted(df["genre"].dropna().unique())
    genre_options = ["All"] + all_genres

    selected_genre = st.sidebar.multiselect(
        "Select Genre",
        options=genre_options,
        default=["All"]
    )

    if "All" in selected_genre:
        selected_genre = all_genres

    # --- Apply filters ---
    key_mask = (df["key"] == selected_key) if selected_key != "All" else True

    filtered_df = df[
        key_mask &
        (df["stream_count"] >= stream_range[0]) &
        (df["stream_count"] <= stream_range[1]) &
        (df["release_year"] >= year_range[0]) &
        (df["release_year"] <= year_range[1]) &
        (df["country"].isin(selected_country)) &
        (df["genre"].isin(selected_genre))
        ]

    return filtered_df