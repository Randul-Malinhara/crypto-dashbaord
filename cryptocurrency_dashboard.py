# cryptocurrency_dashboard.py

import os
import datetime
import logging
import requests
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from pycoingecko import CoinGeckoAPI
import plotly.express as px
import dash_bootstrap_components as dbc
from textblob import TextBlob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Cryptocurrency Dashboard"

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Secure API key management
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Fetch market data
def fetch_market_data():
    try:
        logging.info("Fetching market data...")
        data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1)
        df = pd.DataFrame(data)
        df = df[["id", "name", "current_price", "market_cap", "price_change_percentage_24h"]]
        return df
    except Exception as e:
        logging.error(f"Error fetching market data: {e}")
        return pd.DataFrame()

# Fetch cryptocurrency news
def fetch_crypto_news():
    API_URL = "https://newsapi.org/v2/everything"
    if not NEWS_API_KEY:
        logging.error("NEWS_API_KEY is not set.")
        return []
    params = {
        "q": "cryptocurrency",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
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
            logging.error(f"Error fetching news: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

# Analyze sentiment of news articles
def analyze_sentiment(articles):
    for article in articles:
        sentiment_score = TextBlob(article["title"]).sentiment.polarity
        article["sentiment"] = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    return articles

# App layout
app.layout = dbc.Container([
    html.H1("Cryptocurrency Dashboard", className="text-center my-4"),

    # Search bar for news
    dbc.Row([
        dbc.Col([html.H4("Search News"),
                 dcc.Input(id="search-bar", type="text", placeholder="Search news...", className="mb-3 form-control")], md=6),
        dbc.Col([html.H4("Select Cryptocurrency"),
                 dcc.Dropdown(id="crypto-dropdown",
                              options=[{"label": crypto.capitalize(), "value": crypto} for crypto in ["bitcoin", "ethereum", "dogecoin"]],
                              placeholder="Select a Cryptocurrency")], md=6)
    ]),

    dbc.Row([
        # News Section
        dbc.Col([
            html.H4("Latest News", className="mb-3"),
            html.Div(id="news-container")
        ], md=6),

        # Market Data Section
        dbc.Col([
            html.H4("Market Data", className="mb-3"),
            dcc.Graph(id="market-chart"),
            html.Div(id="market-table-container")
        ], md=6)
    ]),

    # Historical Data Section
    dbc.Row([
        dbc.Col([
            html.H4("Historical Data", className="mb-3"),
            dcc.Graph(id="historical-chart")
        ])
    ]),

    # Portfolio Tracker
    dbc.Row([
        dbc.Col([
            html.H4("Portfolio Tracker", className="mb-3"),
            html.Div(id="portfolio-value", className="text-info")
        ])
    ]),

    dcc.Interval(id='interval-component', interval=10*60*1000, n_intervals=0)  # 10-minute interval
], fluid=True)

# Callbacks
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
            html.Span(f" ({article['source']}, {datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')}, Sentiment: {article['sentiment']})")
        ]) for article in news
    ])

@app.callback(
    [Output("market-chart", "figure"), Output("market-table-container", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_market_data(n):
    df = fetch_market_data()
    if df.empty:
        return px.scatter(), html.Div("Error fetching market data.", className="text-danger")
    fig = px.bar(
        df, x="name", y="current_price", color="price_change_percentage_24h",
        labels={"current_price": "Price (USD)", "price_change_percentage_24h": "% Change (24h)"},
        title="Top Cryptocurrencies by Market Cap"
    )
    fig.update_layout(yaxis_title="Price (USD)", xaxis_title="Cryptocurrency")
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, className="mt-3")
    return fig, table

@app.callback(
    Output("historical-chart", "figure"),
    [Input("crypto-dropdown", "value")]
)
def update_historical_chart(crypto_id):
    if not crypto_id:
        return px.line()
    try:
        data = cg.get_coin_market_chart_by_id(id=crypto_id, vs_currency='usd', days='30')
        prices = data['prices']
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        fig = px.line(df, x="timestamp", y="price", title=f"{crypto_id.capitalize()} Price Trend (30 Days)")
        fig.update_layout(xaxis_title="Date", yaxis_title="Price (USD)")
        return fig
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        return px.line()

@app.callback(
    Output("portfolio-value", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_portfolio_value(n):
    user_portfolio = {"bitcoin": 2, "ethereum": 5, "dogecoin": 1000}  # Example holdings
    df = fetch_market_data()
    if df.empty:
        return "Error fetching market data."
    total_value = sum(df[df["id"] == crypto]["current_price"].values[0] * qty for crypto, qty in user_portfolio.items() if crypto in df["id"].values)
    return f"Total Portfolio Value: ${total_value:.2f}"

if __name__ == "__main__":
    app.run_server(debug=True)
