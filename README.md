# Cryptocurrency News Dashboard

This project is a Python-based interactive dashboard that fetches and displays the latest cryptocurrency news. Built using the Dash framework, it provides real-time updates to help users stay informed about trends in the cryptocurrency world.

## Features

- **News Fetching**: Fetches cryptocurrency news articles using the NewsAPI.
- **Dynamic Updates**: The dashboard refreshes every 10 minutes to display the latest news.
- **Interactive UI**: Displays news articles as clickable links, with publication date and source.

## Requirements

Ensure you have Python installed (version 3.7 or later), along with the following libraries:

- `requests`
- `dash`
- `pandas`
- `plotly`

Install the required libraries using:
```bash
pip install requests dash pandas plotly
```

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/crypto-news-dashboard.git
   cd crypto-news-dashboard
   ```

2. **Set Up API Key**:
   - Obtain an API key from [NewsAPI](https://newsapi.org/).
   - Replace `YOUR_NEWSAPI_KEY` in `cryptocurrency_dashboard.py` with your API key.

3. **Run the Dashboard**:
   ```bash
   python cryptocurrency_dashboard.py
   ```

4. **Access the Dashboard**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8050/
   ```

## File Structure

```
crypto-news-dashboard/
├── cryptocurrency_dashboard.py  # Main application script
├── README.md                     # Project documentation
```

## Example Output

The dashboard will display:
- Titles of the latest cryptocurrency news articles.
- Publication source and date.
- Clickable links to read the full articles.

## Future Enhancements

- Add sentiment analysis of news articles.
- Include cryptocurrency price trends alongside the news.
- Provide user customization options for news filters.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

For any issues or questions, feel free to contact me at `bhdrmalinhara#gmail.com`.
