import streamlit as st
import pandas as pd

from src.data import load_data
from src.filters import render_filters, apply_filters
from src.charts import plot_response_hist, plot_borough_bar
from src.layouts import header_metrics, body_layout_tabs


def main() -> None:
    st.set_page_config(
        page_title="Spotify Music Analytics Dashboard",
        layout="wide",
    )

    st.title("Spotify Music Analytics Dashboard")
    st.caption("This is a dashboard curated from  Spotify Music Analytics Dataset, meant to illustrate trends in music and other features.")

    # ✅ Data loading (cached)
    df = load_data("./data/updatedspotify")

    # -------------------------
    # TODO (DEMO): Add a quick 'data sanity' check
    # - show row count
    # - show first 5 rows (optional)
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df.head(), use_container_width=True)
    # -------------------------
    # HINT: st.write / st.dataframe
    # st.write(...)
    # st.dataframe(...)

    # -------------------------
    # Filters (sidebar by default)
    # -------------------------
    # render_filters returns a dictionary of user selections
    selections = render_filters(df)

    # apply_filters returns a filtered dataframe based on selections
    df_f = apply_filters(df, selections)

    # -------------------------
    # TODO (DEMO): Explain Streamlit re-runs
    # - changing a widget reruns the script top-to-bottom
    # - df_f changes because selections changes
    st.info(
        "Streamlit reruns this script from top to bottom whenever a widget changes. "
        "Because selections change, df_f changes on every interaction."
    )
    # -------------------------

    # -------------------------
    # Header metrics
    # -------------------------
    # TODO (IN-CLASS): Replace placeholder metrics with real calculations
    def header_metrics(df):
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Requests", len(df))
        col2.metric("Unique Boroughs", df['borough'].nunique())
        col3.metric("Average Response Time", round(df['response_time_days'].mean(), 2))

    # -------------------------
    # Main body
    # -------------------------
    # Tabs layout by default (3 tabs)
    tab_choice = st.radio(
        "Choose a layout for the body (lab demo uses tabs; assignment can remix):",
        ["Tabs (3)", "Two Columns"],
        horizontal=True,
    )

    if tab_choice == "Tabs (3)":
        body_layout_tabs(df_f)
    else:
        # -------------------------
        # TODO (DEMO): Implement a 2-column layout
        # - left column: a chart
        # - right column: a table
        # -------------------------
        # HINT: st.columns(2)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Response Time Distribution")
            plot_response_hist(df_f)  # assumes this function exists in src/charts

        with col2:
            st.subheader("Filtered Rows")
            st.dataframe(df_f, use_container_width=True, height=420)

    # -------------------------
    # TODO (IN-CLASS): Add a footer with a short 'design note'
    # - 2–3 sentences: who is the audience + what questions can they answer?
    st.divider()
    st.caption(
        "Design Note: This dashboard is intended for NYC city analysts or researchers. "
        "It helps answer questions about 311 service requests, including trends in response times, "
        "distribution across boroughs, and patterns in complaint types."
    )
    # -------------------------


if __name__ == "__main__":
    main()
