# Crypto Price Tracker

Tracks live cryptocurrency prices for Bitcoin, Ethereum and BNB.
Triggers alerts when prices cross custom thresholds.

## Features
- Live price fetching via CoinGecko API (no API key required)
- Customizable price alert levels
- 24 hour price change visualization
- Price history stored in SQLite database
- Excel report export

## Technologies
Python, Pandas, Matplotlib, SQLite, CoinGecko API

## How to Run
1. Install requirements: pip install pandas matplotlib pycoingecko openpyxl
2. Run: python crypto_tracker.py

## Customize Alerts
Edit the alerts dictionary in the script:
alerts = {
    "BITCOIN": {"min": 50000, "max": 100000},
    "ETHEREUM": {"min": 2000, "max": 5000},
    "BINANCECOIN": {"min": 300, "max": 700}
}

## Output
- crypto_chart.png
- crypto_report.xlsx
- crypto.db