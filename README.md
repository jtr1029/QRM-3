# Financial News Sentiment Analysis App

This Streamlit application provides financial news sentiment analysis and risk management tools for different sectors in the USA. The app helps users make informed investment decisions by analyzing news sentiment and providing risk management insights.

## Features

- Sector-specific news sentiment analysis
- Risk management tools and metrics
- Historical performance visualization
- Sector correlation analysis
- Risk assessment recommendations

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your NewsAPI key:
   - Sign up at [NewsAPI](https://newsapi.org/)
   - Create a `.env` file in the project root and add your API key:
     ```
     NEWS_API_KEY=your_api_key_here
     ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select a sector from the dropdown menu
2. View sentiment analysis and risk metrics
3. Explore historical performance
4. Get risk management recommendations

## Note

This application requires a NewsAPI key for fetching financial news. Make sure to obtain one from [NewsAPI](https://newsapi.org/). 
