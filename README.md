# Cryptocurrency News Dashboard

This project is an advanced interactive dashboard to track cryptocurrency trends, portfolio performance, and related news. Built with the Dash framework, it provides real-time updates and customizable features to enhance user experience.

## Features

### Core Features:
- **Cryptocurrency News**:
  - Fetches the latest cryptocurrency-related news using NewsAPI.
  - Provides sentiment analysis (Positive, Negative, Neutral) for each news article.
  - Search functionality to filter news articles.

- **Market Data**:
  - Displays live market data (price, market cap, 24h change) for top cryptocurrencies.
  - Visualizes market trends using interactive bar charts.

- **Historical Data**:
  - Provides 30-day price trends for selected cryptocurrencies.
  - Interactive line charts to explore historical data.

- **Portfolio Tracker**:
  - Tracks the total value of a sample cryptocurrency portfolio.
  - Automatically updates portfolio value based on live prices.

### Additional Features:
- Secure API key management with `.env` file.
- Responsive design using Dash Bootstrap Components.
- Modular and scalable architecture.

## Requirements

Ensure you have Python (version 3.7 or later) installed, along with the following libraries:

- `dash`
- `dash-bootstrap-components`
- `plotly`
- `requests`
- `pandas`
- `pycoingecko`
- `textblob`
- `python-dotenv`

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/crypto-news-dashboard.git
cd crypto-news-dashboard
```

### 2. Set Up API Keys
- Obtain an API key from [NewsAPI](https://newsapi.org/).
- Create a `.env` file in the project root and add your API key:
  ```
  NEWS_API_KEY=your_api_key_here
  ```

### 3. Run the Application
```bash
python cryptocurrency_dashboard.py
```

### 4. Access the Dashboard
Open your browser and navigate to:
```
http://127.0.0.1:8050/
```

## File Structure

```
crypto-news-dashboard/
├── cryptocurrency_dashboard.py  # Main application script
├── test_cryptocurrency_dashboard.py  # Unit tests
├── README.md                     # Project documentation
├── requirements.txt              # List of dependencies
```

## Example Outputs

### Dashboard Layout:
- **Live Market Data:** Bar chart and table for top cryptocurrencies.
- **Latest News:** Sentiment-tagged news articles with clickable links.
- **Historical Data:** Interactive line charts for price trends.
- **Portfolio Tracker:** Live portfolio value calculation.

### News Example:
```
- Bitcoin hits a new all-time high! (Crypto News, Jan 01, 2025, Sentiment: Positive)
- Ethereum struggles as prices drop (Blockchain Today, Dec 31, 2024, Sentiment: Negative)
```

## Testing

Run the unit tests using:
```bash
pytest test_cryptocurrency_dashboard.py
```

## Future Enhancements
- Add user authentication for personalized portfolios.
- Include real-time data updates via WebSocket.
- Expand historical data options (e.g., customizable date ranges).
- Implement price alerts for user-selected cryptocurrencies.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---
For issues or questions, contact `bhdrmalinhara@gmail.com`. Happy tracking!
