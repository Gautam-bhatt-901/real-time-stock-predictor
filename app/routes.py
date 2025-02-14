from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from .stock_data import get_stock_data
from .news import get_company_news
from .news import fetch_news_sentiment
import joblib
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('base.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/stock/<ticker>', methods=['GET'])
def stock_info(ticker):
    """
    API endpoint to get stock data for a specific ticker.
    Example: GET /stock/AAPL
    """
    data = get_stock_data(ticker.upper())
    return jsonify(data)

@main.route('/news/<ticker>', methods=['GET'])
def company_news(ticker):
    """
    API endpoint to fetch news and sentiment analysis for a given stock ticker.
    Example: GET /news/AAPL
    """
    news = get_company_news(ticker.upper())
    return jsonify(news)

@main.route("/predict", methods=["POST"])
@login_required
def predict_stock():
    """Predict Buy/Sell for a given stock based on price and sentiment."""
    data = request.json
    ticker = data.get("ticker", "").upper()

    stock_data = get_stock_data(ticker)
    if stock_data is None:
        return jsonify({"error": "Stock data not found"}), 404

    sentiment = fetch_news_sentiment(ticker)

    # Load the trained model
    model_path = f"models/{ticker}_model.pkl"
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        return jsonify({"error": "Model not trained for this stock"}), 404

    # Prepare input features
    latest_data = stock_data.iloc[-1][["Return", "RSI"]].values
    features = np.append(latest_data, sentiment).reshape(1, -1)

    # Predict Buy/Sell
    prediction = model.predict(features)[0]
    decision = "Buy" if prediction == 1 else "Sell"

    return jsonify({
        "ticker": ticker,
        "current_price": round(stock_data["Close"].iloc[-1], 2),
        "sentiment_score": sentiment,
        "prediction": decision
    })