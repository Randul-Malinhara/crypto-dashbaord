import pytest
import pandas as pd
from unittest.mock import patch
from cryptocurrency_dashboard import fetch_market_data, analyze_sentiment, update_portfolio_value

# Mock data for testing
mock_market_data = [
    {
        "id": "bitcoin",
        "name": "Bitcoin",
        "current_price": 50000,
        "market_cap": 1000000000,
        "price_change_percentage_24h": 5.0
    },
    {
        "id": "ethereum",
        "name": "Ethereum",
        "current_price": 4000,
        "market_cap": 500000000,
        "price_change_percentage_24h": -3.0
    }
]

mock_articles = [
    {"title": "Bitcoin hits a new all-time high!", "source": "Crypto News"},
    {"title": "Ethereum struggles as prices drop", "source": "Blockchain Today"},
    {"title": "Neutral article about cryptocurrency", "source": "General News"}
]

mock_portfolio = {
    "bitcoin": 2,
    "ethereum": 5,
    "dogecoin": 1000
}

# Test fetch_market_data
@patch("cryptocurrency_dashboard.cg.get_coins_markets")
def test_fetch_market_data(mock_get_coins_markets):
    mock_get_coins_markets.return_value = mock_market_data
    df = fetch_market_data()

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert list(df.columns) == ["id", "name", "current_price", "market_cap", "price_change_percentage_24h"]
    assert df.loc[0, "id"] == "bitcoin"
    assert df.loc[1, "current_price"] == 4000

# Test fetch_market_data with error handling
@patch("cryptocurrency_dashboard.cg.get_coins_markets")
def test_fetch_market_data_error(mock_get_coins_markets):
    mock_get_coins_markets.side_effect = Exception("API error")
    df = fetch_market_data()

    assert isinstance(df, pd.DataFrame)
    assert df.empty

# Test analyze_sentiment
def test_analyze_sentiment():
    analyzed_articles = analyze_sentiment(mock_articles)

    assert isinstance(analyzed_articles, list)
    assert len(analyzed_articles) == len(mock_articles)
    assert analyzed_articles[0]["sentiment"] == "Positive"
    assert analyzed_articles[1]["sentiment"] == "Negative"
    assert analyzed_articles[2]["sentiment"] == "Neutral"

# Test analyze_sentiment with empty input
def test_analyze_sentiment_empty():
    analyzed_articles = analyze_sentiment([])
    assert isinstance(analyzed_articles, list)
    assert len(analyzed_articles) == 0

# Test update_portfolio_value
@patch("cryptocurrency_dashboard.fetch_market_data")
def test_update_portfolio_value(mock_fetch_market_data):
    mock_fetch_market_data.return_value = pd.DataFrame(mock_market_data)
    total_value = update_portfolio_value(0)

    # Calculate expected value manually
    expected_value = 2 * 50000 + 5 * 4000  # Bitcoin and Ethereum only
    assert total_value == f"Total Portfolio Value: ${expected_value:.2f}"

# Test update_portfolio_value with empty data
@patch("cryptocurrency_dashboard.fetch_market_data")
def test_update_portfolio_value_empty(mock_fetch_market_data):
    mock_fetch_market_data.return_value = pd.DataFrame()
    total_value = update_portfolio_value(0)

    assert total_value == "Error fetching market data."
