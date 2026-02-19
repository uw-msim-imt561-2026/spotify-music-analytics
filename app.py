import streamlit as st
import pandas as pd

from src.filters import render_filters
from src.layouts import render_kpis
from src.charts import (
    render_popularity_by_key,
    render_avg_stream_by_label,
    render_popularity_distribution,
    render_genres_over_time
)


@st.cache_data
def load_data():
    return pd.read_csv("./data/updatedspotify.csv")


def main():
    st.set_page_config(
        page_title="Spotify Music Analytics",
        layout="wide"
    )

    st.title("🎧 Spotify Music Analytics Dashboard")

    df = load_data()

    filtered_df = render_filters(df)

    render_kpis(filtered_df)

    render_popularity_by_key(filtered_df)
    render_avg_stream_by_label(filtered_df)
    render_popularity_distribution(filtered_df)
    render_genres_over_time(filtered_df)


if __name__ == "__main__":
    main()
