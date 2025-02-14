import yfinance as yf
import pandas as pd
import ta

def get_stock_data(ticker):
    """
    Fetch real-time data and historical stock prices for training the model.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period = "6mo")
        if hist.empty:
            return {"error":"No data available for the given ticker"}
        # Calculate daily returns
        hist["Return"] = hist["Close"].pct_change()
        # Compute technical indicators
        # Relative Strength Index(RSI)=A technical indicator that measures the speed and magnitude of price changes over a period of time
        hist["RSI"] = ta.momentum.RSIIndicator(hist["Close"], window=14).rsi()
        hist.fillna(0, inplace = True)

        return hist
    
    except Exception as e:
        return {"error": str(e)}
