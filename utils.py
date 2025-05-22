def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def format_sentiment_score(score):
    return f"{score:.2f}"

def calculate_average_sentiment(sentiment_scores):
    if not sentiment_scores:
        return 0
    return sum(sentiment_scores) / len(sentiment_scores)

def get_sentiment_distribution(sentiment_results):
    distribution = {
        "positive": 0,
        "neutral": 0,
        "negative": 0
    }
    for result in sentiment_results:
        distribution[result['sentiment']] += 1
    return distribution

def extract_relevant_data(sentiment_results):
    return [
        {
            "review": result["review"],
            "sentiment": result["sentiment"],
            "confidence_scores": result["confidence_scores"]
        }
        for result in sentiment_results
    ]