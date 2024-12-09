# cryptocurrency_dashboard.py

import datetime
import requests
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from pycoingecko import CoinGeckoAPI
import plotly.express as px
import dash_bootstrap_components as dbc
from textblob import TextBlob

# Initialize Dash app
# Update app initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Cryptocurrency News Dashboard"

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Function to fetch cryptocurrency market data
def fetch_market_data():
    try:
        data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1)
        df = pd.DataFrame(data)
        df = df[["id", "name", "current_price", "market_cap", "price_change_percentage_24h"]]
        return df
    except Exception as e:
        print(f"Error fetching market data: {e}")
        return pd.DataFrame()



# Function to fetch cryptocurrency news
def fetch_crypto_news():
    API_URL = "https://newsapi.org/v2/everything"
    API_KEY = "API_KEY"  # Replace with your NewsAPI key
    params = {
        "q": "cryptocurrency",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [
                {
                    "title": article["title"],
                    "source": article["source"]["name"],
                    "publishedAt": article["publishedAt"],
                    "url": article["url"]
                }
                for article in articles
            ]
        else:
            print(f"Error fetching news: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
    
# Refactor app layout to use dbc.Container and dbc.Row
app.layout = dbc.Container([
    html.H1("Enhanced Cryptocurrency Dashboard", className="text-center my-4"),
    dbc.Row([
        dbc.Col([...], md=6),  # News section
        dbc.Col([...], md=6)   # Market data section
    ]),
    dcc.Interval(
        id='interval-component',
        interval=10*60*1000,  # Update every 10 minutes
        n_intervals=0
    )
], fluid=True)

# Update app layout
html.H4("Search for News"),
dcc.Input(id="search-bar", type="text", placeholder="Search news...", className="mb-3 form-control"),

# Function to analyze sentiment of news articles
def analyze_sentiment(articles):
    for article in articles:
        sentiment_score = TextBlob(article["title"]).sentiment.polarity
        article["sentiment"] = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    return articles

# Update news callback to include sentiment
@app.callback(
    Output("news-container", "children"),
    [Input("interval-component", "n_intervals"), Input("search-bar", "value")]
)

def update_news(n, search_term):
    news = fetch_crypto_news()
    news = analyze_sentiment(news)

    if not news:
        return html.Div("No news available.", className="text-danger")

    if search_term:
        news = [article for article in news if search_term.lower() in article["title"].lower()]

    return html.Ul([
        html.Li([
            html.A(article["title"], href=article["url"], target="_blank"),
            html.Span(f" ({article['source']}, {datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')}, Sentiment: {article['sentiment']})")
        ])
        for article in news
    ])


# Update app layout
dbc.Col([
    html.H4("Live Market Data", className="mb-3"),
    dcc.Graph(id="market-chart"),
    html.Div(id="market-table-container")
], md=6)

# Callback for market data
@app.callback(
    [Output("market-chart", "figure"), Output("market-table-container", "children")],
    [Input("interval-component", "n_intervals")]
)

# Function to fetch historical market data for a specific cryptocurrency
def fetch_historical_data(crypto_id):
    try:
        data = cg.get_coin_market_chart_by_id(id=crypto_id, vs_currency='usd', days='30')
        prices = data['prices']
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return pd.DataFrame()

# Add historical data visualization callback
@app.callback(
    Output("historical-chart", "figure"),
    [Input("crypto-dropdown", "value")]
)
def update_historical_chart(crypto_id):
    if not crypto_id:
        return px.line()
    
    df = fetch_historical_data(crypto_id)
    if df.empty:
        return px.line()

    fig = px.line(df, x="timestamp", y="price", title=f"{crypto_id} Price Trend (30 Days)")
    fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
    return fig

# Add layout for historical data
layout_historical = html.Div([
    html.H4("Historical Data", className="mb-3"),
    dcc.Dropdown(id="crypto-dropdown", options=[
        {"label": crypto.capitalize(), "value": crypto} for crypto in ["bitcoin", "ethereum", "dogecoin"]
    ], placeholder="Select a Cryptocurrency"),
    dcc.Graph(id="historical-chart")
])

# Add historical data section to the main layout
app.layout.children.append(layout_historical)

def update_market_data(n):
    df = fetch_market_data()
    if df.empty:
        return px.scatter(), html.Div("Error fetching market data.", className="text-danger")

    # Market Chart
    fig = px.bar(
    df, x="name", y="current_price", color="price_change_percentage_24h",
    labels={"current_price": "Price (USD)", "price_change_percentage_24h": "% Change (24h)"},
    title="Top Cryptocurrencies by Market Cap"
    )
    
    fig.update_layout(yaxis_title="Price (USD)", xaxis_title="Cryptocurrency")

    # Market Table
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, className="mt-3")

    return fig, table

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
