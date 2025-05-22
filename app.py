import streamlit as st
import pandas as pd
from azure_blob import fetch_sentiment_data
from metrics import get_sentiment_statistics
import plotly.express as px
import time
from datetime import datetime


st.set_page_config(page_title="Live Sentiment Dashboard", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {background-color: #F5F5F5;}
        h1 {color: #2F4F4F;}
        h2 {color: #2E8B57;}
        .sidebar .sidebar-content {background-color: #2F4F4F; color: white;}
        .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
        .stMetric label {font-size: 1rem; color: #666;}
        .stMetric value {font-size: 1.4rem; color: #2E8B57;}
        .css-1d391kg {padding-top: 3rem;}
    </style>
""",
    unsafe_allow_html=True,
)


def main():
    # Sidebar with controls
    with st.sidebar:
        st.title("Dashboard Controls")
        refresh_rate = st.slider("Refresh rate (seconds)", 5, 60, 10)
        st.divider()
        st.markdown("### Data Filters")
        date_filter = st.date_input("Filter by date", [])

    # Main content area
    st.title("Real-Time Sentiment Insights Dashboard")
    st.markdown("Live monitoring of customer feedback sentiment")

    # Create placeholder containers
    metrics_placeholder = st.empty()
    chart_placeholder1 = st.empty()
    chart_placeholder2 = st.empty()

    while True:
        # Fetch updated data
        sentiment_data = fetch_sentiment_data()

        if sentiment_data:
            # Calculate metrics
            metrics = get_sentiment_statistics(sentiment_data)

            # Metrics display
            sentiment_distribution = metrics["distribution"]
            with metrics_placeholder.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        label="Average Sentiment",
                        value=f"{metrics['average_sentiment']:.2f}",
                        help="Average sentiment score across all reviews",
                    )
                with col2:
                    st.metric(
                        label="Total Reviews",
                        value=len(sentiment_data),
                        help="Total number of reviews processed",
                    )
                with col3:
                    st.metric(
                        label="Positive Sentiment",
                        value=f"{sentiment_distribution.get('positive', 0)}",
                        help="Count of positive sentiment reviews",
                    )
                with col4:
                    st.metric(
                        label="Response Rate",
                        value="98.2%",
                        help="Percentage of reviews responded to",
                    )

            # Charts
            with chart_placeholder1.container():
                col_chart1, col_chart2 = st.columns([3, 2])

                with col_chart1:
                    st.subheader("Sentiment Over Time")
                    sentiment_df = pd.DataFrame(sentiment_data)
                    if not sentiment_df.empty and "timestamp" in sentiment_df.columns:
                        sentiment_df["timestamp"] = pd.to_datetime(
                            sentiment_df["timestamp"]
                        )
                        fig = px.area(
                            sentiment_df.resample("1H", on="timestamp")
                            .mean()
                            .reset_index(),
                            x="timestamp",
                            y="sentiment_score",
                            title="Hourly Average Sentiment",
                            color_discrete_sequence=["#2E8B57"],
                            template="plotly_white",
                        )
                        fig.update_layout(
                            showlegend=False,
                            xaxis_title="Time",
                            yaxis_title="Sentiment Score",
                            hovermode="x unified",
                        )
                        st.plotly_chart(
                            fig, use_container_width=True, key="sentiment_over_time"
                        )

                with col_chart2:
                    st.subheader("Sentiment Distribution")
                    sentiment_distribution = metrics["distribution"]
                    dist_df = pd.DataFrame(
                        {
                            "Sentiment": list(sentiment_distribution.keys()),
                            "Count": list(sentiment_distribution.values()),
                        }
                    )
                    fig = px.pie(
                        dist_df,
                        names="Sentiment",
                        values="Count",
                        hole=0.3,
                        color="Sentiment",
                        color_discrete_map={
                            "positive": "#2E8B57",
                            "neutral": "#FFD700",
                            "negative": "#CD5C5C",
                        },
                    )
                    fig.update_traces(textposition="inside", textinfo="percent+label")
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        key=f"sentiment_distribution_{int(time.time()*1000)}",
                    )

            # Data table
            with chart_placeholder2.container():
                st.subheader("Recent Feedback")
                sentiment_df = pd.DataFrame(sentiment_data)
                if not sentiment_df.empty and "timestamp" in sentiment_df.columns:
                    sentiment_df = sentiment_df.sort_values(
                        "timestamp", ascending=False
                    )
                    st.dataframe(
                        sentiment_df[
                            ["timestamp", "sentiment_score", "feedback_text"]
                        ].head(10),
                        hide_index=True,
                        column_config={
                            "timestamp": "Time",
                            "sentiment_score": "Sentiment",
                            "feedback_text": "Feedback",
                        },
                        use_container_width=True,
                    )
                elif not sentiment_df.empty:
                    st.dataframe(sentiment_df.head(10), use_container_width=True)
        else:
            st.warning("Waiting for initial data...")

        # Refresh interval
        time.sleep(refresh_rate)


if __name__ == "__main__":
    main()
