# test if yfinance is returning empty data drame
import yfinance as yf
ticker = yf.Ticker("GOOGL")
print(ticker.history(period="1d"))
