from pycoingecko import CoinGeckoAPI
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Connect to CoinGecko
cg = CoinGeckoAPI()

# --- Pull Live Prices ---
coins = ["bitcoin", "ethereum", "binancecoin"]
prices = cg.get_price(
    ids=coins,
    vs_currencies="usd",
    include_24hr_change=True
)

# --- Organize into DataFrame ---
records = []
for coin, data in prices.items():
    records.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "coin": coin.upper(),
        "price_usd": data["usd"],
        "change_24h": round(data["usd_24h_change"], 2)
    })

df = pd.DataFrame(records)
print("--- Live Prices ---")
print(df)

# --- Price Alerts ---
print("\n--- Price Alerts ---")
alerts = {
    "BITCOIN": {"min": 50000, "max": 100000},
    "ETHEREUM": {"min": 2000, "max": 5000},
    "BINANCECOIN": {"min": 300, "max": 700}
}

for _, row in df.iterrows():
    coin = row["coin"]
    price = row["price_usd"]
    if coin in alerts:
        if price < alerts[coin]["min"]:
            print(f"🔴 {coin} BELOW minimum! ${price:,}")
        elif price > alerts[coin]["max"]:
            print(f"🟢 {coin} ABOVE maximum! ${price:,}")
        else:
            print(f"⚪ {coin} within normal range at ${price:,}")

# --- Save to Database ---
conn = sqlite3.connect("crypto.db")
df.to_sql("prices", conn, if_exists="append", index=False)
print("\nPrices saved to database!")

# --- Chart ---
plt.figure(figsize=(10, 5))
colors = ["green" if x > 0 else "red" for x in df["change_24h"]]
plt.bar(df["coin"], df["change_24h"], color=colors)
plt.axhline(y=0, color="black", linewidth=0.8, linestyle="--")
plt.title("24 Hour Price Change (%)")
plt.xlabel("Coin")
plt.ylabel("Change (%)")
plt.tight_layout()
plt.savefig("crypto_chart.png")
plt.show()

# --- Export to Excel ---
df.to_excel("crypto_report.xlsx", index=False)
print("Report saved!")
conn.close()