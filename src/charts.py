import streamlit as st
import plotly.express as px
import pandas as pd

# Spotify brand colors
SPOTIFY_GREEN = "#1DB954"          # Main Spotify green
SPOTIFY_ALT_GREEN = "#1ED761"      # Alternate brighter green for contrast
MUSTARD_YELLOW = "#FFC857"         # For N/A or missing data

spotify_colors = [
    SPOTIFY_GREEN,           # Main green
    SPOTIFY_ALT_GREEN,       # Lighter green
    "#FF6B6B",               # Red/pink for contrast
    "#4D96FF",               # Blue for contrast
    "#FFA500",               # Orange
    "#9B59B6",               # Purple
]

def render_key_popularity_over_time(df: pd.DataFrame):
    st.subheader("🎹 Musical Key Share of Streams")
    st.subheader("Do Certain Musical Keys Correlate With Higher Popularity?")
    st.caption(
        "Musical key influences the tonal mood of a track (e.g., major keys often sound brighter, "
        "minor keys more somber). This chart explores whether certain keys are associated "
        "with higher average popularity scores."
    )

    if df.empty:
        st.warning("No data available for current filters.")
        return

    # Add legend/explanation for musical mode
    st.info(
        """
        **Understanding Musical Keys & Mode:**
        - **Major (mode=1)**: brighter, happier, energetic
        - **Minor (mode=0)**: emotional, dramatic, somber

        This chart shows average popularity of tracks by key and mode over time.
        """
    )

    # Group by year, key, and mode
    grouped = (
        df.groupby(["release_year", "key", "mode"], as_index=False)
        .agg(avg_popularity=("popularity", "mean"))
    )

    # Map mode to readable label
    grouped["mode_label"] = grouped["mode"].map({1: "Major (Brighter)", 0: "Minor (Emotional)"})
    grouped["key_mode"] = grouped["key"] + " - " + grouped["mode_label"]

    # Ensure keys are ordered
    key_order = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    grouped['key'] = pd.Categorical(grouped['key'], categories=key_order, ordered=True)

    # Decide chart type
    if grouped["release_year"].nunique() == 1:
        # Single year -> side-by-side bar chart
        pivot_df = grouped.pivot(index="key", columns="mode_label", values="avg_popularity").reset_index()
        fig = px.bar(
            pivot_df,
            x="key",
            y=["Major (Brighter)", "Minor (Emotional)"],
            barmode="group",
            color_discrete_map={
                "Major (Brighter)": SPOTIFY_GREEN,
                "Minor (Emotional)": "#FF6B6B",  # distinct for clarity
            },
            title=f"Average Track Popularity by Key & Mode ({grouped['release_year'].iloc[0]})"
        )
        fig.update_layout(
            xaxis_title="Musical Key",
            yaxis_title="Average Popularity",
            legend_title="Mode"
        )
    else:
        # Multiple years -> line chart
        fig = px.line(
            grouped,
            x="release_year",
            y="avg_popularity",
            color="mode_label",
            line_group="key",
            markers=True,
            title="Average Track Popularity by Key & Mode Over Time"
        )
        fig.update_layout(
            xaxis_title="Release Year",
            yaxis_title="Average Popularity",
            legend_title="Mode",
            xaxis=dict(dtick=1)
        )

    st.plotly_chart(fig, use_container_width=True)


def render_avg_stream_by_label(df: pd.DataFrame):
    st.subheader("🏷 Average Stream Count by Label")

    if df.empty:
        st.warning("No data available.")
        return

    grouped = df.groupby("label", as_index=False)["stream_count"].mean()

    fig = px.bar(
        grouped,
        x="label",
        y="stream_count",
        title="Average Stream Count by Label",
        color="label",
        color_discrete_sequence=spotify_colors  # branded green shades
    )

    fig.update_layout(
        xaxis_title="Label",
        yaxis_title="Average Streams"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_popularity_distribution(df: pd.DataFrame):
    st.subheader("📈 Distribution of Track Popularity")

    if df.empty:
        st.warning("No data available.")
        return

    fig = px.histogram(
        df,
        x="popularity",
        nbins=20,
        title="Track Popularity Distribution",
        color_discrete_sequence=[SPOTIFY_GREEN]
    )

    fig.update_layout(
        xaxis_title="Popularity Score",
        yaxis_title="Number of Tracks"
    )

    st.plotly_chart(fig, use_container_width=True)


def render_genres_over_time_by_country(df: pd.DataFrame):
    st.subheader("🌍 Genre Trends Over Time by Country")

    if df.empty:
        st.warning("No data available for current filters.")
        return

    grouped = (
        df.groupby(["release_year", "country", "genre"], as_index=False)
        .agg(total_streams=("stream_count", "sum"))
    )

    unique_years = grouped["release_year"].nunique()

    # If only 1 year selected → switch to bar chart
    if unique_years == 1:
        fig = px.bar(
            grouped,
            x="genre",
            y="total_streams",
            color="country",
            title="Genre Distribution (Single Year Selected)",
            color_discrete_sequence=spotify_colors
        )
    else:
        # Prevent 10+ country overload
        if df["country"].nunique() > 5:
            st.info("More than 5 countries selected. Showing top 5 by stream volume.")
            top_countries = (
                df.groupby("country")["stream_count"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .index
            )
            grouped = grouped[grouped["country"].isin(top_countries)]

        fig = px.line(
            grouped,
            x="release_year",
            y="total_streams",
            color="country",
            line_group="genre",
            markers=True,
            title="Genre Trends Over Time"
        )

    fig.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Total Streams"
    )

    st.plotly_chart(fig, use_container_width=True)