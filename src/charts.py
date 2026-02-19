
import streamlit as st
import plotly.express as px
import pandas as pd


def render_popularity_by_key(df: pd.DataFrame):
    st.subheader("🎵 Popularity by Key")

    fig = px.bar(
        df,
        x="key",
        y="popularity",
        color="key",
        title="Popularity by Musical Key"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_avg_stream_by_label(df: pd.DataFrame):
    st.subheader("🏷 Average Stream Count by Label")

    grouped = df.groupby("label", as_index=False)["stream_count"].mean()

    fig = px.bar(
        grouped,
        x="label",
        y="stream_count",
        color="label",
        title="Average Stream Count by Label"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_popularity_distribution(df: pd.DataFrame):
    st.subheader("📈 Distribution of Track Popularity")

    fig = px.histogram(
        df,
        x="popularity",
        hover_data=["track_name"],
        nbins=20,
        title="Popularity Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_genres_over_time(df: pd.DataFrame):
    st.subheader("🌍 Genres Over Time")

    grouped = (
        df.groupby(["release_year", "genre"], as_index=False)
        ["track_name"]
        .count()
    )

    fig = px.line(
        grouped,
        x="release_year",
        y="track_name",
        color="genre",
        title="Genre Trends Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)
