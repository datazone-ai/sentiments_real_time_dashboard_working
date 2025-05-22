from azure.storage.blob import BlobServiceClient
import streamlit as st
import json


def get_blob_service_client():
    blob_conn_str = st.secrets["BLOB_CONNECTION_STRING"]
    return BlobServiceClient.from_connection_string(blob_conn_str)


def fetch_sentiment_data(container_name="output"):
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    sentiment_data = []

    for blob in container_client.list_blobs():
        blob_data = container_client.download_blob(blob.name).readall()
        sentiment_result = json.loads(blob_data)
        sentiment_data.append(sentiment_result)

    return sentiment_data


def process_sentiment_data(sentiment_data):
    processed_data = {
        "reviews": [],
        "positive": 0,
        "neutral": 0,
        "negative": 0,
    }

    for result in sentiment_data:
        processed_data["reviews"].append(result["review"])
        sentiment = result["sentiment"]
        processed_data[sentiment] += 1

    return processed_data
