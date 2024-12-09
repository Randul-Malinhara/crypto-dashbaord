# cryptocurrency_dashboard.py

import requests
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Cryptocurrency News Dashboard"

# Function to fetch cryptocurrency news
def fetch_crypto_news():
    API_URL = "https://newsapi.org/v2/everything"
    API_KEY = "b12556176c584ae4b355c3ab4def76b5"  # Replace with your NewsAPI key
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

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
