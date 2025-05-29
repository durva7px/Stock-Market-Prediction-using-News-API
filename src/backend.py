from flask import Flask, request, jsonify
import requests
from textblob import TextBlob
import yfinance as yf
from datetime import datetime, timedelta
from flask_cors import CORS
import random
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('NES_API_KEY')
print(api_key)

app = Flask(__name__)
CORS(app)

def fetch_stock_news(stock_symbol, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock_symbol}&language=en&sortBy=publishedAt&pageSize=10&apiKey={api_key}'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['articles']
    else:
        print(f"Failed to fetch news: {response.status_code}")
        return []

def analyze_sentiment(articles):
    total_polarity = 0
    for article in articles:
        content = article['title'] + '. ' + article['description'] if article['description'] else article['title']
        blob = TextBlob(content)
        total_polarity += blob.sentiment.polarity

    avg_polarity = total_polarity / len(articles) if articles else 0
    return avg_polarity

def should_invest(sentiment_score):
    if sentiment_score > 0.5:
        return "Positive sentiment detected. It is a great time to invest!"
    elif sentiment_score > 0.1:
        return "Positive sentiment detected. It might be a good time to invest."
    elif sentiment_score <= 0.1:
        return "Neutral sentiment detected. Consider other factors before investing."
    else:
        return "Negative sentiment detected. It is a bad time to invest."

def predict_stock_movement(stock_symbol, sentiment_score):
    stock = yf.Ticker(stock_symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    historical_hourly_data = stock.history(interval="1h", start=start_date, end=end_date)
    historical_daily_data = stock.history(interval="1d", start=start_date, end=end_date)

    if historical_hourly_data.empty or historical_daily_data.empty:
        return (
            "Not enough historical data to make hourly prediction.",
            "Not enough historical data to make daily prediction.",
            "Not enough historical data to make weekly prediction."
        )

    recent_hour_close = historical_hourly_data['Close'].values[-1]  
    two_hours_ago_close = historical_hourly_data['Close'].values[-3]  

    recent_day_close = historical_daily_data['Close'].values[-1]  
    yesterday_close = historical_daily_data['Close'].values[-2] 

    week_ago_close = historical_daily_data['Close'].values[0]  

    hourly_prediction = ""
    daily_prediction = ""
    weekly_prediction = ""
    
    if sentiment_score > 0.1 and recent_hour_close > two_hours_ago_close:
        hourly_prediction = "Stock is likely to rise in the next few hours."
    elif sentiment_score < -0.1 and recent_hour_close < two_hours_ago_close:
        hourly_prediction = "Stock is likely to fall in the next few hours."
    else:
        hourly_prediction = "Neutral hourly trend. Expect minor fluctuations."
    

    if sentiment_score > 0.1 and recent_day_close > yesterday_close:
        daily_prediction = "Stock is likely to rise tomorrow."
    elif sentiment_score < -0.1 and recent_day_close < yesterday_close:
        daily_prediction = "Stock is likely to fall tomorrow."
    else:
        daily_prediction = "Neutral daily trend. Stock may fluctuate or stay stable tomorrow."

    if sentiment_score > 0.1 and recent_day_close > week_ago_close:
        weekly_prediction = "Stock is likely to rise this week."
    elif sentiment_score < -0.1 and recent_day_close < week_ago_close:
        weekly_prediction = "Stock is likely to fall this week."
    else:
        weekly_prediction = "Neutral weekly trend. Stock may remain stable or fluctuate slightly."
    
    print(hourly_prediction)
    print(daily_prediction)
    print(weekly_prediction)

    return hourly_prediction, daily_prediction, weekly_prediction

def get_stock_insights(stock_symbol):
    stock = yf.Ticker(stock_symbol)

    # Fetch current stock price using the history method
    history_data = stock.history(period="1d")
    if history_data.empty or 'Close' not in history_data:
        return {
            "current_price": "N/A",
            "market_cap": "N/A",
            "high_52_week": "N/A",
            "low_52_week": "N/A",
            "message": f"No price data available for '{stock_symbol}'. The symbol may be incorrect or data is temporarily unavailable."
        }

    current_price = round(history_data['Close'].iloc[0], 2)

    # Fetch additional stock info safely
    try:
        stock_info = stock.info
    except Exception as e:
        stock_info = {}
        print(f"Error fetching stock info for {stock_symbol}: {e}")

    insights = {
        "current_price": current_price,
        "market_cap": stock_info.get("marketCap", "N/A"),
        "high_52_week": stock_info.get("fiftyTwoWeekHigh", "N/A"),
        "low_52_week": stock_info.get("fiftyTwoWeekLow", "N/A"),
        "message": "Stock data fetched successfully."
    }

    return insights

# def get_stock_insights(stock_symbol):
#     stock = yf.Ticker(stock_symbol)
#     stock_info = stock.info
#     insights = {
#         "current_price": stock_info.get("regularMarketPrice"),
#         "market_cap": stock_info.get("marketCap"),
#         "high_52_week": stock_info.get("fiftyTwoWeekHigh"),
#         "low_52_week": stock_info.get("fiftyTwoWeekLow")
#     }
#     return insights

def get_trending_stocks():
    ts = ["AAPL", "TSLA", "GOOGL", "NVDA", "NKE", "DIS", "TSM"]
    
    trending_stocks = []
    for ticker in ts:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period='5d') 
        
        if stock_data.empty:
            continue  
        
        if stock_data['Close'][-1] > stock_data['Close'][0]:
            trending_stocks.append(ticker)
    
    return trending_stocks[:3]

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    stock_symbol = request.json['stockSymbol']
    api_key = "e42e1415bc8e4c4e9dea2415073ee37d"  
    articles = fetch_stock_news(stock_symbol, api_key)
    
    if not articles:
        return jsonify({"error": "No news found for the stock."})

    sentiment_score = analyze_sentiment(articles)
    investment_advice = should_invest(sentiment_score)
    hourly_prediction, daily_prediction, weekly_prediction = predict_stock_movement(stock_symbol, sentiment_score)

  
    headlines = [article['title'] for article in articles]


    stock_insights = get_stock_insights(stock_symbol)

   
    trending_stocks = get_trending_stocks()

    result = {
        "symbol": stock_symbol,
        "sentiment_score": sentiment_score,  
        "investment_advice": investment_advice,
        "hourly_prediction": hourly_prediction,
        "daily_prediction": daily_prediction,
        "weekly_prediction": weekly_prediction,
        "news_headlines": headlines,
        "current_price": stock_insights["current_price"],
        "market_cap": stock_insights["market_cap"],
        "high_52_week": stock_insights["high_52_week"],
        "low_52_week": stock_insights["low_52_week"],
        "trending_stocks": trending_stocks
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
