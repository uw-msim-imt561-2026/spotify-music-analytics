import streamlit as st
import pandas as pd

def render_kpis(filtered_df: pd.DataFrame, full_df: pd.DataFrame):
    col1, col2, col3 = st.columns(3)

    # KPI 1: Average Track Popularity
    if (
        not filtered_df.empty
        and "popularity" in filtered_df.columns
        and "popularity" in full_df.columns
    ):
        avg_pop = filtered_df["popularity"].mean()
        historical_avg = full_df["popularity"].mean()
        delta_pop = avg_pop - historical_avg
        delta_label = f"{delta_pop:.2f}"
    else:
        avg_pop = None
        delta_label = None

    with col1:
        st.metric(
            label="Average Track Popularity (vs overall dataset avg)",
            value=f"{avg_pop:.2f}" if avg_pop is not None else "N/A",
            delta=delta_label if delta_label is not None else "N/A",
            help="Green ▲ if above overall dataset average, Red ▼ if below"
        )

    # KPI 2: Total Streams (vs previous year)
    if (
        not filtered_df.empty
        and "stream_count" in filtered_df.columns
        and "release_year" in filtered_df.columns
    ):
        total_streams = filtered_df["stream_count"].sum()

        latest_year = filtered_df["release_year"].max()
        prev_year = latest_year - 1

        prev_streams = filtered_df[
            filtered_df["release_year"] == prev_year
        ]["stream_count"].sum()

        change_pct = (
            (total_streams - prev_streams) / prev_streams * 100
            if prev_streams > 0 else 0
        )
    else:
        total_streams = None
        change_pct = None

    with col2:
        st.metric(
            label="Total Streams (vs previous year)",
            value=f"{total_streams:,}" if total_streams is not None else "N/A",
            delta=f"{change_pct:.1f}%" if change_pct is not None else "N/A",
            help="Shows % change from previous year's total streams"
        )

    # KPI 3: Top Genre by Streams
    if (
        not filtered_df.empty
        and "genre" in filtered_df.columns
        and "stream_count" in filtered_df.columns
    ):
        genre_counts = filtered_df.groupby("genre")["stream_count"].sum()

        if not genre_counts.empty:
            top_genre = genre_counts.idxmax()
            top_genre_share = (
                genre_counts.max() / genre_counts.sum() * 100
            )
        else:
            top_genre, top_genre_share = "N/A", 0
    else:
        top_genre, top_genre_share = "N/A", 0

    with col3:
        st.metric(
            label="Top Genre by Streams (% share)",
            value=top_genre,
            delta=f"{top_genre_share:.1f}%" if top_genre != "N/A" else "N/A",
            help="Percentage share of total streams for this genre"
        )

    if filtered_df.empty:
        st.warning("No data matches the current filters. Please adjust filter selections.")