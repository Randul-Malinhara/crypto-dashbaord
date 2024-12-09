# cryptocurrency_dashboard.py

import requests
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from pycoingecko import CoinGeckoAPI
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)
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

# Layout of the app
app.layout = html.Div([
    html.H1("Cryptocurrency News Dashboard", style={"textAlign": "center"}),
    html.Div("Stay updated with the latest cryptocurrency news."),

    dcc.Interval(
        id='interval-component',
        interval=10*60*1000,  # Update every 10 minutes
        n_intervals=0
    ),

    html.Div(id="news-container"),
])

# Callback to update news
@app.callback(
    Output("news-container", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_news(n):
    news = fetch_crypto_news()
    if not news:
        return html.Div("No news available.")

    return html.Ul([
        html.Li([
            html.A(article["title"], href=article["url"], target="_blank"),
            html.Span(f" ({article['source']}, {article['publishedAt'][:10]})")
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
