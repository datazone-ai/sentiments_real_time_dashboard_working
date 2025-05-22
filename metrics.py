def calculate_average_sentiment(sentiment_data):
    if not sentiment_data:
        return 0.0
    total_score = sum(data['confidence_scores']['positive'] - data['confidence_scores']['negative'] for data in sentiment_data)
    return total_score / len(sentiment_data)

def sentiment_distribution(sentiment_data):
    distribution = {'positive': 0, 'neutral': 0, 'negative': 0}
    for data in sentiment_data:
        sentiment = data['sentiment']
        if sentiment in distribution:
            distribution[sentiment] += 1
    return distribution

def get_sentiment_statistics(sentiment_data):
    average_sentiment = calculate_average_sentiment(sentiment_data)
    distribution = sentiment_distribution(sentiment_data)
    return {
        'average_sentiment': average_sentiment,
        'distribution': distribution
    }