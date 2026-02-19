import streamlit as st
import pandas as pd


def render_kpis(df: pd.DataFrame) -> None:
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    avg_popularity = df["popularity"].mean()
    total_streams = df["stream_count"].sum()
    genre_count = df["genre"].nunique()

    with col1:
        st.metric(
            label="Average Popularity",
            value=f"{avg_popularity:.2f}"
        )

    with col2:
        st.metric(
            label="Total Streams",
            value=f"{total_streams:,}"
        )

    with col3:
        st.metric(
            label="Number of Genres",
            value=genre_count
        )
