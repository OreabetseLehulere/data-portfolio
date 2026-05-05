import schedule
import time
from pycoingecko import CoinGeckoAPI
import pandas as pd
import sqlite3
from datetime import datetime

cg = CoinGeckoAPI()

def track_prices():
    print(f"\nRunning price check at {datetime.now().strftime('%H:%M:%S')}")
    
    coins = ["bitcoin", "ethereum", "binancecoin"]
    prices = cg.get_price(
        ids=coins,
        vs_currencies="usd",
        include_24hr_change=True
    )

    records = []
    for coin, data in prices.items():
        records.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "coin": coin.upper(),
            "price_usd": data["usd"],
            "change_24h": round(data["usd_24h_change"], 2)
        })

    df = pd.DataFrame(records)
    print(df[["coin", "price_usd", "change_24h"]])

    # Save to database
    conn = sqlite3.connect("crypto-price-tracker/crypto.db")
    df.to_sql("prices", conn, if_exists="append", index=False)
    conn.close()
    print("Prices saved!")

# Run immediately once
track_prices()

# Then run every 60 seconds
schedule.every(60).seconds.do(track_prices)

print("\nAutomation running... Press Ctrl+C to stop")
while True:
    schedule.run_pending()
    time.sleep(1)
    