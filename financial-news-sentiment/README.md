# Financial News Sentiment Analyzer

Automatically pulls live financial news headlines and scores 
each one as Positive, Negative or Neutral using NLP.

## Features
- Live news fetching via NewsAPI
- Automated sentiment scoring with VADER
- Daily sentiment trend charts
- SQLite database storage
- Excel report export

## Technologies
Python, Pandas, NLTK, Matplotlib, SQLite, NewsAPI

## How to Run
1. Add your NewsAPI key to a .env file: NEWS_API_KEY=your_key
2. Install requirements: pip install pandas nltk matplotlib newsapi-python python-dotenv
3. Run: python sentiment_analyzer.py

## Output
- sentiment_distribution.png
- daily_sentiment.png
- live_sentiment_report.xlsx
- sentiment.db