import streamlit as st
import plotly.express as px
import pandas as pd

def render_key_popularity_over_time(df: pd.DataFrame):
    st.subheader("🎹 Key Popularity Trends Over Time")

    if df.empty:
        st.warning("No data available for current filters.")
        return

    # Group by year and key
    grouped = (
        df.groupby(["release_year", "key"], as_index=False)
        .agg(avg_popularity=("popularity", "mean"))
    )

    # Ensure keys are ordered
    key_order = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    grouped['key'] = pd.Categorical(grouped['key'], categories=key_order, ordered=True)

    fig = px.line(
        grouped,
        x="release_year",
        y="avg_popularity",
        color="key",
        markers=True,  # adds points for each year
        title="Average Track Popularity by Key Over Time"
    )

    fig.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Average Popularity",
        legend_title="Musical Key",
        xaxis=dict(dtick=1)  # show every year
    )

    st.plotly_chart(fig, use_container_width=True)

def render_avg_stream_by_label(df: pd.DataFrame):
    st.subheader("🏷 Average Stream Count by Label")
    grouped = df.groupby("label", as_index=False)["stream_count"].mean()
    fig = px.bar(grouped, x="label", y="stream_count", color="label", title="Average Stream Count by Label")
    st.plotly_chart(fig, use_container_width=True)

def render_popularity_distribution(df: pd.DataFrame):
    st.subheader("📈 Distribution of Track Popularity")
    fig = px.histogram(df, x="popularity", nbins=20, hover_data=["track_name"], title="Track Popularity Distribution")
    st.plotly_chart(fig, use_container_width=True)

def render_genres_over_time_by_country(df: pd.DataFrame):
    st.subheader("🌍 Genre Trends Over Time by Country")

    if df.empty:
        st.warning("No data available for current filters.")
        return

    # Count number of tracks
    grouped = (
        df.groupby(["release_year", "country", "genre"], as_index=False)
        .agg(track_count=("track_name", "count"))
    )

    fig = px.line(
        grouped,
        x="release_year",
        y="track_count",
        color="genre",
        facet_col="country",
        title="Genre Trends Over Time by Country"
    )

    fig.update_layout(yaxis_title="Number of Tracks")

    st.plotly_chart(fig, use_container_width=True)
