import schedule
import time
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlite3
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(dotenv_path=".env")
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
nltk.download("vader_lexicon", quiet=True)
sia = SentimentIntensityAnalyzer()

def analyze_news():
    print(f"\nFetching news at {datetime.now().strftime('%H:%M:%S')}")
    
    response = newsapi.get_everything(
        q="stock market OR Dow Jones OR nasdaq OR trading",
        language="en",
        sort_by="publishedAt",
        page_size=10
    )

    headlines = []
    for article in response["articles"]:
        score = sia.polarity_scores(article["title"])["compound"]
        headlines.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "headline": article["title"],
            "source": article["source"]["name"],
            "score": round(score, 4),
            "sentiment": "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"
        })

    df = pd.DataFrame(headlines)
    print(df[["headline", "sentiment", "score"]])

    conn = sqlite3.connect("financial-news-sentiment/sentiment.db")
    df.to_sql("headlines", conn, if_exists="append", index=False)
    conn.close()
    print("Sentiment data saved!")

# Run immediately
analyze_news()

# Then every 30 minutes
schedule.every(30).minutes.do(analyze_news)

print("\nNews automation running... Press Ctrl+C to stop")
while True:
    schedule.run_pending()
    time.sleep(1)