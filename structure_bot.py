import yfinance as yf
import pandas as pd
import sqlite3
import schedule
import time
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os
from datetime import datetime

# --- Load credentials ---
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Assets to monitor ---
assets = {
    "Bitcoin": "BTC-USD",
    "Gold": "GC=F",
    "US30": "YM=F"
}

# --- Database setup ---
conn = sqlite3.connect("structure_alerts.db", check_same_thread=False)
conn.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        asset TEXT,
        signal TEXT,
        price REAL
    )
""")
conn.commit()

# --- Send Telegram message ---
async def send_alert(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def notify(message):
    asyncio.run(send_alert(message))

# --- Fetch 4H candles ---
def get_4h_data(ticker):
    df = yf.download(ticker, period="5d", interval="1h", progress=False)
    # Flatten multi-level columns
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df[["High", "Low", "Close"]].copy()
    # Resample to 4H
    df_4h = df.resample("4h").agg({
        "High": "max",
        "Low": "min",
        "Close": "last"
    }).dropna()
    return df_4h

# --- Detect market structure ---
def detect_structure(df):
    signals = []
    highs = df["High"].values
    lows = df["Low"].values

    for i in range(2, len(df)):
        prev_high = highs[i-2]
        curr_high = highs[i-1]
        prev_low = lows[i-2]
        curr_low = lows[i-1]

        if curr_high > prev_high and curr_low > prev_low:
            signals.append("🟢 HH + HL — Bullish Structure")
        elif curr_high < prev_high and curr_low < prev_low:
            signals.append("🔴 LH + LL — Bearish Structure")
        elif curr_high > prev_high and curr_low < prev_low:
            signals.append("⚪ HH + LL — Mixed/Expansion")
        elif curr_high < prev_high and curr_low > prev_low:
            signals.append("⚪ LH + HL — Mixed/Contraction")
        else:
            signals.append("⏳ No clear structure")

    return signals[-1] if signals else "No data"

# --- Main monitoring function ---
def check_structure():
    print(f"\nChecking structure at {datetime.now().strftime('%H:%M:%S')}")
    
    for name, ticker in assets.items():
        try:
            df = get_4h_data(ticker)
            signal = detect_structure(df)
            price = round(df["Close"].iloc[-1], 2)

            print(f"{name}: {signal} | Price: {price}")

            # Save to database
            conn.execute("""
                INSERT INTO alerts (timestamp, asset, signal, price)
                VALUES (?, ?, ?, ?)
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, signal, price))
            conn.commit()

            # Send Telegram alert
            message = f"""
📊 *{name} — 4H Structure Update*
Signal: {signal}
Price: {price}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """
            notify(message)

        except Exception as e:
            print(f"Error checking {name}: {e}")

# --- Run immediately then every 4 hours ---
check_structure()
schedule.every(4).hours.do(check_structure)

print("\nBot running... Press Ctrl+C to stop")
while True:
    schedule.run_pending()
    time.sleep(1)