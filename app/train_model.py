from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from .stock_data import get_stock_data
from .news import fetch_news_sentiment

def prepare_training_data(ticker):
    """
    Create a dataset combining historical stock trends and sentiment analysis.
    """
    stock_data = get_stock_data(ticker)
    if stock_data is None:
        return None, None
    
    # Get news sentiment
    stock_data["Sentiment"] = stock_data.index.to_series().apply(lambda x: fetch_news_sentiment(ticker))

    # Define the target variable (Buy = 1, Sell = 0)
    stock_data["Target"] = (stock_data["Return"] > 0).astype(int)

    # Select features
    X = stock_data[["Return", "RSI", "Sentiment"]]
    Y = stock_data["Target"]

    return X, Y

def train_stock_prediction_model(ticker):
    """
    Train and save a machine learning model for predicting buy/sell signals.
    """
    X, Y = prepare_training_data(ticker)
    
    if X is None or Y is None:
        print(f"No data available for {ticker}")
        return
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)

    # Feature Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    model = RandomForestClassifier(random_state = 42)
    model.fit(X_train, Y_train)
    
    y_pred = model.predict(X_test)

    joblib.dump(model, f"models/{ticker}_model.pkl")