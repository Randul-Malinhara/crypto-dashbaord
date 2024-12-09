# cryptocurrency_dashboard.py

import requests
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from pycoingecko import CoinGeckoAPI
import plotly.express as px
import dash_bootstrap_components as dbc

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

# Update callback
@app.callback(
    Output("news-container", "children"),
    [Input("interval-component", "n_intervals"), Input("search-bar", "value")]
)
def update_news(n, search_term):
    news = fetch_crypto_news()
    if not news:
        return html.Div("No news available.", className="text-danger")

    if search_term:
        news = [article for article in news if search_term.lower() in article["title"].lower()]

    return html.Ul([
        html.Li([
            html.A(article["title"], href=article["url"], target="_blank"),
            html.Span(f" ({article['source']}, {datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')})")
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
