import streamlit as st
import pandas as pd
from azure_blob import fetch_sentiment_data
from metrics import get_sentiment_statistics
import plotly.express as px


def main():
    st.title("Real-Time Sentiment Insights Dashboard")
    st.sidebar.header("Dashboard Controls")

    # Fetch sentiment data from Azure Blob Storage
    sentiment_data = fetch_sentiment_data()

    if sentiment_data is not None:
        # Calculate metrics
        metrics = get_sentiment_statistics(sentiment_data)

        # Display key metrics
        st.subheader("Key Metrics")
        st.metric(label="Average Sentiment Score", value=metrics["average_sentiment"])
        st.metric(label="Total Reviews", value=len(sentiment_data))

        # Sentiment distribution chart
        st.subheader("Sentiment Distribution")
        sentiment_distribution = metrics["distribution"]
        sentiment_df = pd.DataFrame(
            {
                "Sentiment": list(sentiment_distribution.keys()),
                "Count": list(sentiment_distribution.values()),
            }
        )
        fig = px.pie(
            sentiment_df,
            names="Sentiment",
            values="Count",
            title="Sentiment Distribution",
        )
        st.plotly_chart(fig)

        # Time series of sentiment scores (if applicable)
        if sentiment_data and "timestamp" in sentiment_data[0]:
            st.subheader("Sentiment Over Time")
            sentiment_df_full = pd.DataFrame(sentiment_data)
            if (
                "timestamp" in sentiment_df_full.columns
                and "sentiment_score" in sentiment_df_full.columns
            ):
                time_series_fig = px.line(
                    sentiment_df_full,
                    x="timestamp",
                    y="sentiment_score",
                    title="Sentiment Score Over Time",
                )
                st.plotly_chart(time_series_fig)
    else:
        st.warning("No sentiment data available.")


if __name__ == "__main__":
    main()
