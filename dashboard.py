import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from datetime import datetime

# --- Load Data ---
def load_crypto():
    try:
        conn = sqlite3.connect("crypto.db", check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM prices", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame({
            "coin": ["BITCOIN", "ETHEREUM", "BINANCECOIN"],
            "price_usd": [95000, 3200, 580],
            "change_24h": [2.5, -1.2, 0.8],
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * 3
        })

def load_sentiment():
    try:
        conn = sqlite3.connect("sentiment.db", check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM headlines", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame({
            "date": ["2026-05-05"] * 3,
            "headline": ["Markets rally", "Stocks drop", "Fed holds rates"],
            "sentiment": ["Positive", "Negative", "Neutral"],
            "score": [0.6, -0.5, 0.0]
        })

def load_jse():
    try:
        conn = sqlite3.connect("jse.db", check_same_thread=False)
        df = pd.read_sql_query("SELECT * FROM stocks", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame({
            "company": ["Naspers", "Anglo American", "Sasol", "Standard Bank", "MTN"],
            "price": [3200, 80000, 24000, 30000, 21000],
            "from_high_%": [-5.2, -12.3, -8.1, -3.4, -15.6]
        })

# --- App ---
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    # Header
    html.Div([
        html.H1("Financial Analytics Dashboard",
                style={"color": "white", "margin": "0", "padding": "20px"}),
        html.P(f"Auto-refreshes every 60 seconds",
               style={"color": "#aaa", "margin": "0", "paddingLeft": "20px"})
    ], style={"backgroundColor": "#1a1a2e", "marginBottom": "20px"}),

    # Auto refresh every 60 seconds
    dcc.Interval(id="refresh", interval=60*1000, n_intervals=0),

    # Row 1 — Crypto
    html.H2("Cryptocurrency", style={"paddingLeft": "20px", "color": "#333"}),
    html.Div([
        dcc.Graph(id="crypto-prices", style={"width": "50%"}),
        dcc.Graph(id="crypto-change", style={"width": "50%"}),
    ], style={"display": "flex"}),

    # Row 2 — Sentiment
    html.H2("Market Sentiment", style={"paddingLeft": "20px", "color": "#333"}),
    html.Div([
        dcc.Graph(id="sentiment-pie", style={"width": "50%"}),
        dcc.Graph(id="sentiment-trend", style={"width": "50%"}),
    ], style={"display": "flex"}),

    # Row 3 — JSE
    html.H2("JSE Stocks", style={"paddingLeft": "20px", "color": "#333"}),
    html.Div([
        dcc.Graph(id="jse-prices", style={"width": "50%"}),
        dcc.Graph(id="jse-high", style={"width": "50%"}),
    ], style={"display": "flex"}),

], style={"fontFamily": "Arial", "backgroundColor": "#f5f5f5"})


# --- Callbacks ---
@app.callback(
    [Output("crypto-prices", "figure"),
     Output("crypto-change", "figure"),
     Output("sentiment-pie", "figure"),
     Output("sentiment-trend", "figure"),
     Output("jse-prices", "figure"),
     Output("jse-high", "figure")],
    [Input("refresh", "n_intervals")]
)
def update_charts(n):
    crypto_df = load_crypto()
    sentiment_df = load_sentiment()
    jse_df = load_jse()

    # Crypto prices
    latest_crypto = crypto_df.groupby("coin").last().reset_index()
    fig1 = px.bar(latest_crypto, x="coin", y="price_usd",
                  color="coin", title="Crypto Prices (USD)")

    # Crypto 24h change
    fig2 = px.bar(latest_crypto, x="coin", y="change_24h",
                  color="change_24h", color_continuous_scale="RdYlGn",
                  title="24h Price Change (%)")

    # Sentiment pie
    fig3 = px.pie(sentiment_df, names="sentiment",
                  color="sentiment",
                  color_discrete_map={"Positive": "green",
                                      "Negative": "red",
                                      "Neutral": "gray"},
                  title="Sentiment Distribution")

    # Sentiment trend
    date_col = "timestamp" if "timestamp" in sentiment_df.columns else "date"
    trend = sentiment_df.groupby(date_col)["score"].mean().reset_index()
    fig4 = px.line(trend, x=date_col, y="score",
                   title="Sentiment Trend Over Time")
    fig4.add_hline(y=0, line_dash="dash", line_color="gray")

    # JSE prices
    latest_jse = jse_df.groupby("company").last().reset_index()
    fig5 = px.bar(latest_jse, x="company", y="price",
                  color="company", title="JSE Stock Prices (ZAR)")

    # JSE from high
    fig6 = px.bar(latest_jse, x="company", y="from_high_%",
                  color="from_high_%", color_continuous_scale="RdYlGn",
                  title="% Below 52 Week High")

    return fig1, fig2, fig3, fig4, fig5, fig6


if __name__ == "__main__":
    app.run(debug=True)