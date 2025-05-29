# 📈 Stock Market Prediction using News Sentiment Analysis 📰

This project predicts short-term stock price movement using **sentiment analysis** of real-time news headlines. It combines financial data from Yahoo Finance and news sentiment scoring to forecast hourly, daily, and weekly stock trends.

---

## 🚀 Features

- 🔍 **News-Based Sentiment Analysis**  
  Fetches and analyzes recent news articles related to a stock ticker.

- 📊 **Stock Movement Prediction**  
  Uses both stock price trends and sentiment to make predictions across three timeframes:  
  - Hourly
  - Daily
  - Weekly

- 📈 **Real-Time Market Data**  
  Uses Yahoo Finance (`yfinance`) for up-to-date historical stock prices.

- 🌐 **Flask API Backend**  
  Provides a REST API to analyze and return stock movement predictions.

---

## 🛠️ Tech Stack

- Python 3
- Flask
- yfinance
- NewsAPI
- TextBlob (for sentiment analysis)
- python-dotenv (for secure API key management)

---

## 🔧 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/durva7px/Stock-Market-Prediction-using-News-API.git
   cd Stock-Market-Prediction-using-News-API
   ```

2. **Create a Virtual Environment**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the requirements
    ```
    pip install -r requirements.txt
    ```
4. **Create a .env file**
    ```
    NEWS_API_KEY="your_newsapi_key_here"
    ```

5. **Run Flask Backend**
    ```
    python backend.py
    ```

### 🗝️ Note on API Key Usage 
This project requires an API key from NewsAPI to fetch news data for sentiment analysis. Each user must obtain their own API key by signing up on the NewsAPI website.

Here’s a short process to get your NewsAPI key:

1. **Go to [NewsAPI.org](https://newsapi.org/).**
2. **Sign up** for a free account using your email.
3. **Verify your email** if required.
4. **Log in** to your account dashboard.
5. **Find your API key** displayed on the dashboard or under the “API Keys” section.
6. **Copy the API key** and use it in your project for accessing news data.

✅ That’s it! You’re ready to make API requests with your key.

---

## 🔴 Troubleshooting
    - If you get errors about missing packages, double-check you activated the virtual environment.
    - Make sure your .env file has the correct API key.
    - For Windows users, if the activation script doesn’t run, try running your command prompt as Administrator.
---

## 🙌 Contributions
Pull requests are welcome! If you find a bug or want to improve the prediction logic, feel free to open an issue or submit a PR.

---

## 💡 Future Improvements
✔️ Integrate more advanced NLP models for sentiment analysis

✔️ Use machine learning for price prediction

✔️ Add frontend dashboard for visualization

---

## 👩‍💻 Developed by
[Durva Deshpande](https://github.com/durva7px)
[Yadhnika Wakde](https://example.com)
