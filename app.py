import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from textblob import TextBlob
from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

# Define sectors and their corresponding ETFs
SECTORS = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Financial': 'XLF',
    'Consumer Discretionary': 'XLY',
    'Consumer Staples': 'XLP',
    'Industrial': 'XLI',
    'Energy': 'XLE',
    'Materials': 'XLB',
    'Utilities': 'XLU',
    'Real Estate': 'XLRE',
    'Communication Services': 'XLC'
}

def get_sector_news(sector):
    """Fetch news articles for a specific sector"""
    query = f"{sector} sector financial news"
    news = newsapi.get_everything(
        q=query,
        language='en',
        sort_by='publishedAt',
        from_param=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    )
    return news['articles']

def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def get_sector_metrics(ticker):
    """Get key metrics for a sector ETF"""
    etf = yf.Ticker(ticker)
    info = etf.info
    
    return {
        'Beta': info.get('beta', 'N/A'),
        '52 Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
        '52 Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
        'Average Volume': info.get('averageVolume', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A')
    }

def get_historical_data(ticker):
    """Get historical data for a sector ETF"""
    etf = yf.Ticker(ticker)
    hist = etf.history(period='1y')
    return hist

def main():
    st.set_page_config(page_title="Financial Sector Sentiment Analysis", layout="wide")
    
    st.title("Financial Sector Sentiment Analysis & Risk Management")
    st.write("Analyze sentiment and risk metrics for different sectors in the USA")
    
    # Sidebar for sector selection
    st.sidebar.header("Select Sector")
    selected_sector = st.sidebar.selectbox("Choose a sector:", list(SECTORS.keys()))
    
    # Get sector data
    ticker = SECTORS[selected_sector]
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Sentiment Analysis", "Risk Metrics", "Historical Performance"])
    
    with tab1:
        st.header("News Sentiment Analysis")
        
        # Fetch and analyze news
        news_articles = get_sector_news(selected_sector)
        
        if news_articles:
            sentiments = []
            for article in news_articles:
                title = article.get('title', '')
                description = article.get('description', '')
                sentiment = analyze_sentiment(f"{title} {description}")
                sentiments.append(sentiment)
            
            avg_sentiment = np.mean(sentiments)
            
            # Display sentiment gauge
            fig = px.pie(values=[avg_sentiment + 1, 2 - (avg_sentiment + 1)], 
                        names=['Positive', 'Negative'],
                        hole=0.7,
                        title=f"Overall Sentiment for {selected_sector} Sector")
            st.plotly_chart(fig)
            
            # Display recent news
            st.subheader("Recent News")
            for article in news_articles[:5]:
                st.write(f"- [{article['title']}]({article['url']})")
        else:
            st.warning("No news articles found for this sector.")
    
    with tab2:
        st.header("Risk Metrics")
        
        # Get and display sector metrics
        metrics = get_sector_metrics(ticker)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Beta", metrics['Beta'])
            st.metric("52 Week High", f"${metrics['52 Week High']:,.2f}")
        with col2:
            st.metric("52 Week Low", f"${metrics['52 Week Low']:,.2f}")
            st.metric("Average Volume", f"{metrics['Average Volume']:,.0f}")
        with col3:
            st.metric("Market Cap", f"${metrics['Market Cap']:,.0f}")
        
        # Risk assessment
        st.subheader("Risk Assessment")
        beta = metrics['Beta']
        if isinstance(beta, (int, float)):
            if beta > 1.2:
                st.warning("High Risk: This sector shows high volatility compared to the market.")
            elif beta < 0.8:
                st.info("Low Risk: This sector shows lower volatility compared to the market.")
            else:
                st.success("Moderate Risk: This sector's volatility is in line with the market.")
    
    with tab3:
        st.header("Historical Performance")
        
        # Get and display historical data
        hist_data = get_historical_data(ticker)
        
        if not hist_data.empty:
            fig = px.line(hist_data, y='Close', 
                         title=f"{selected_sector} Sector ETF Performance")
            st.plotly_chart(fig)
            
            # Calculate and display key statistics
            returns = hist_data['Close'].pct_change()
            st.subheader("Performance Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Annual Return", f"{returns.mean() * 252 * 100:.2f}%")
            with col2:
                st.metric("Annual Volatility", f"{returns.std() * np.sqrt(252) * 100:.2f}%")
            with col3:
                st.metric("Sharpe Ratio", f"{returns.mean() / returns.std() * np.sqrt(252):.2f}")

if __name__ == "__main__":
    main() 
