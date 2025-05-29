

async function analyzeStock() {
    const stockSymbol = document.getElementById('stockSymbol').value.toUpperCase();

    if (stockSymbol) {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ stockSymbol })
        });

        const data = await response.json();
        displayResults(data);
    }
}

function displayResults(data) {
const resultsDiv = document.getElementById('results');

// Generate bullet points for each news headline
const headlines = data.news_headlines.map(headline => `<li>${headline}</li>`).join('');

// Generate bullet points for trending stocks
const trendingStocks = data.trending_stocks.map(stock => `<li>${stock}</li>`).join('');

// Display stock insights
const stockInsights = `
<div class="insights">
    <h4>Stock Insights for ${data.symbol}:</h4>
    <p>Current Price: $${data.current_price}</p>
    <p>Market Cap: $${data.market_cap}</p>
    <p>52-Week High: $${data.high_52_week}</p>
    <p>52-Week Low: $${data.low_52_week}</p>
</div>
`;

// Update the resultsDiv with the stock analysis and predictions
resultsDiv.innerHTML = `
${stockInsights}
<h3>Sentiment Score: ${data.sentiment_score}</h3>
<p>${data.investment_advice}</p>
<div class="headlines">
    <h4>Top News Headlines:</h4>
    <ul class="headline-list">
        ${headlines}  <!-- Each headline as a bullet point -->
    </ul>
</div>
<div class="prediction">
    <h4>Hourly Prediction:</h4>
    <p>${data.hourly_prediction}</p>
</div>
<div class="prediction">
    <h4>Daily Prediction:</h4>
    <p>${data.daily_prediction}</p>
</div>
<div class="prediction">
    <h4>Weekly Prediction:</h4>
    <p>${data.weekly_prediction}</p>
</div>
<div class="trending">
    <h4>Trending Stocks:</h4>
    <ul class="headline-list">
        ${trendingStocks}  <!-- Each trending stock as a bullet point -->
    </ul>
</div>
`;
}