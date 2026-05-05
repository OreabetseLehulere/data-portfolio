import yfinance as yf
import pandas as pd
import sqlite3
import schedule
import time
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime

# --- Load credentials ---
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
conn = sqlite3.connect(
    str(Path(__file__).parent / "structure_alerts.db"),
    check_same_thread=False
)
conn.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        asset TEXT,
        structure TEXT,
        bos TEXT,
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
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    df = df[["High", "Low", "Close"]].copy()
    df_4h = df.resample("4h").agg({
        "High": "max",
        "Low": "min",
        "Close": "last"
    }).dropna()
    return df_4h

# --- Detect market structure + BOS ---
def detect_structure(df):
    highs = df["High"].values
    lows = df["Low"].values
    closes = df["Close"].values
    signals = []

    for i in range(2, len(df)):
        prev_high = highs[i-2]
        curr_high = highs[i-1]
        prev_low = lows[i-2]
        curr_low = lows[i-1]
        curr_close = closes[i-1]

        # --- Market Structure ---
        if curr_high > prev_high and curr_low > prev_low:
            structure = "🟢 HH + HL — Bullish Structure"
        elif curr_high < prev_high and curr_low < prev_low:
            structure = "🔴 LH + LL — Bearish Structure"
        elif curr_high > prev_high and curr_low < prev_low:
            structure = "⚪ HH + LL — Mixed/Expansion"
        elif curr_high < prev_high and curr_low > prev_low:
            structure = "⚪ LH + HL — Mixed/Contraction"
        else:
            structure = "⏳ No clear structure"

        # --- BOS Detection ---
        bos = ""
        swing_high = max(highs[max(0, i-5):i-1])
        swing_low = min(lows[max(0, i-5):i-1])

        if curr_close > swing_high:
            bos = "🚀 BULLISH BOS — Price broke above swing high!"
        elif curr_close < swing_low:
            bos = "💥 BEARISH BOS — Price broke below swing low!"

        signals.append({
            "structure": structure,
            "bos": bos
        })

    return signals[-1] if signals else {"structure": "No data", "bos": ""}

# --- Main monitoring function ---
def check_structure():
    print(f"\nChecking structure at {datetime.now().strftime('%H:%M:%S')}")

    for name, ticker in assets.items():
        try:
            df = get_4h_data(ticker)
            result = detect_structure(df)
            price = round(df["Close"].iloc[-1], 2)

            print(f"{name}: {result['structure']} | Price: {price}")
            if result['bos']:
                print(f"  ⚡ BOS: {result['bos']}")

            # Save to database
            conn.execute("""
                INSERT INTO alerts (timestamp, asset, structure, bos, price)
                VALUES (?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                result['structure'],
                result['bos'],
                price
            ))
            conn.commit()

            # Send Telegram alert
            bos_line = f"\n⚡ BOS: {result['bos']}" if result['bos'] else ""
            message = f"""
📊 {name} — 4H Structure Update
Structure: {result['structure']}
{bos_line}
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