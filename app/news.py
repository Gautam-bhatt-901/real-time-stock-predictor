import requests
from textblob import TextBlob
import numpy as np

NEWS_API_KEY = "ac847b6fdde44ef38c91715674a4b397"

def get_company_news(ticker):
    # Fetch recent news articles related to the given stock ticker
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error":"Failed to fetch news"}
    
    articles = response.json().get("articles", [])
    news_data = []

    for article in articles[:5]:  #get the top 5 news articles
        title = article["title"]
        description = article["description"] or ""
        url = article["url"]

        sentiment = analyze_sentiment(title + " " + description)

        news_data.append({
            "title": title,
            "description": description,
            "url": url,
            "sentiment": sentiment
        })
    return news_data

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using TextBlob.
    Returns 'Positive', 'Negative', or 'Neutral'.
    """
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

def fetch_news_sentiment(ticker):
    """
    Fetch recent news for the stock and return an aggregated sentiment score.
    """
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return 0  # Neutral sentiment if no news is available

    articles = response.json().get("articles", [])
    
    sentiments = []
    for article in articles[:5]:  # Only use top 5 articles
        text = article["title"] + " " + (article["description"] or "")
        analysis = TextBlob(text)
        sentiments.append(analysis.sentiment.polarity)

    return np.mean(sentiments) if sentiments else 0  # Average sentiment score