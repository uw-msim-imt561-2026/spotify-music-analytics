import streamlit as st
import pandas as pd
from src.filters import render_filters
from src.layouts import render_kpis
from src.charts import (
    render_key_popularity_over_time,
    render_avg_stream_by_label,
    render_popularity_distribution,
    render_genres_over_time_by_country
)

@st.cache_data
def load_data():
    return pd.read_csv("data/updatedspotify.csv")



def main():
    st.set_page_config(page_title="Spotify Music Analytics", layout="wide")
    st.title("🎧 Spotify Music Analytics Dashboard")
    st.markdown(
        "_Dataset: [Spotify Music Analytics Dataset (2015–2025)](https://www.kaggle.com/datasets/rohiteng/spotify-music-analytics-dataset-20152025/data) — IMT 561 class project_")

    df = load_data()

    # Map numeric musical keys to actual key names
    num_to_key = {
        0: 'C', 1: 'C#/Db', 2: 'D', 3: 'D#/Eb',
        4: 'E', 5: 'F', 6: 'F#/Gb', 7: 'G',
        8: 'G#/Ab', 9: 'A', 10: 'A#/Bb', 11: 'B'
    }

    if "key" in df.columns:
        df["key"] = df["key"].map(num_to_key)
    filtered_df = render_filters(df)

    render_kpis(filtered_df, df)
    # Most intuitive visuals first
    render_popularity_distribution(filtered_df)
    render_avg_stream_by_label(filtered_df)
    # More complex visuals lower
    render_key_popularity_over_time(filtered_df)
    render_genres_over_time_by_country(filtered_df)

if __name__ == "__main__":
    main()
