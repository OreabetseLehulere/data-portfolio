import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import sqlite3
from newsapi import NewsApiClient

# Your API key
from dotenv import load_dotenv
import os

# Load API key safely from .env file
load_dotenv(dotenv_path=".env")
api_key = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key=api_key)

# Download sentiment tool
nltk.download("vader_lexicon")

# Pull live financial headlines
print("Fetching live news...")
response = newsapi.get_everything(
    q="stock market OR Dow Jones OR nasdaq OR trading",
    language="en",
    sort_by="publishedAt",
    page_size=20
)

# Extract headlines
articles = response["articles"]
headlines = []
for article in articles:
    headlines.append({
        "date": article["publishedAt"][:10],
        "headline": article["title"],
        "source": article["source"]["name"]
    })

df = pd.DataFrame(headlines)
print(f"Pulled {len(df)} live headlines!")
print(df[["date", "headline"]])

# --- Run Sentiment Analysis on Live Headlines ---
sia = SentimentIntensityAnalyzer()

def get_sentiment(headline):
    score = sia.polarity_scores(headline)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

def get_score(headline):
    return sia.polarity_scores(headline)["compound"]

df["sentiment"] = df["headline"].apply(get_sentiment)
df["score"] = df["headline"].apply(get_score)

print("\n--- Live Sentiment Results ---")
print(df[["date", "headline", "sentiment", "score"]])

# --- Chart: Sentiment Distribution ---
sentiment_counts = df["sentiment"].value_counts()
plt.figure(figsize=(8, 5))
plt.bar(sentiment_counts.index, sentiment_counts.values,
        color=["green" if x == "Positive" else "red" if x == "Negative" else "gray" 
               for x in sentiment_counts.index])
plt.title("Live Market Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Headlines")
plt.tight_layout()
plt.savefig("live_sentiment.png")
plt.show()

# --- Export to Excel ---
df.to_excel("live_sentiment_report.xlsx", index=False)
print("\nLive report saved!")