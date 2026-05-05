import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import sqlite3

# --- Load Data from Your Databases ---

# Crypto data
conn = sqlite3.connect("crypto-price-tracker/crypto.db")
crypto_df = pd.read_sql_query("SELECT * FROM prices", conn)
conn.close()

# Sentiment data
conn = sqlite3.connect("financial-news-sentiment/sentiment.db")
sentiment_df = pd.read_sql_query("SELECT * FROM headlines", conn)
conn.close()

# --- Build Charts ---

# Chart 1: Crypto prices
crypto_chart = px.bar(
    crypto_df.groupby("coin")["price_usd"].last().reset_index(),
    x="coin",
    y="price_usd",
    color="coin",
    title="Live Crypto Prices (USD)"
)

# Chart 2: Sentiment distribution
sentiment_chart = px.pie(
    sentiment_df,
    names="sentiment",
    title="News Sentiment Distribution",
    color="sentiment",
    color_discrete_map={
        "Positive": "green",
        "Negative": "red",
        "Neutral": "gray"
    }
)

# Chart 3: Sentiment over time
sentiment_time = px.line(
    sentiment_df.groupby("timestamp")["score"].mean().reset_index(),
    x="timestamp",
    y="score",
    title="Sentiment Score Over Time"
)

# --- Build Dashboard ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data Analytics Dashboard",
            style={"textAlign": "center", "color": "#333"}),

    html.Div([
        dcc.Graph(figure=crypto_chart),
        dcc.Graph(figure=sentiment_chart),
        dcc.Graph(figure=sentiment_time),
    ])
])

if __name__ == "__main__":
    app.run(debug=True)