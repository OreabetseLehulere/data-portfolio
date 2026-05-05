import yfinance as yf
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# JSE Stocks
stocks = {
    "Naspers": "NPN.JO",
    "Anglo American": "AGL.JO",
    "Sasol": "SOL.JO",
    "Standard Bank": "SBK.JO",
    "MTN": "MTN.JO"
}

# --- Pull Live Price Data ---
records = []
for name, ticker in stocks.items():
    stock = yf.Ticker(ticker)
    info = stock.fast_info
    records.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company": name,
        "ticker": ticker,
        "price": round(info.last_price, 2),
        "52w_high": round(info.year_high, 2),
"52w_low": round(info.year_low, 2),
    })

df = pd.DataFrame(records)
print("--- JSE Live Prices ---")
print(df)

# --- Calculate Distance From 52 Week High ---
df["from_high_%"] = round(
    ((df["price"] - df["52w_high"]) / df["52w_high"]) * 100, 2)

print("\n--- Distance From 52 Week High ---")
print(df[["company", "price", "52w_high", "from_high_%"]])

# --- Save to Database ---
conn = sqlite3.connect("jse.db")
df.to_sql("stocks", conn, if_exists="append", index=False)
print("\nData saved to database!")

# --- Chart 1: Current Prices ---
plt.figure(figsize=(10, 5))
plt.bar(df["company"], df["price"], color="steelblue")
plt.title("JSE Stock Prices (ZAR)")
plt.xlabel("Company")
plt.ylabel("Price (R)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("jse_prices.png")
plt.show()

# --- Chart 2: Distance From 52 Week High ---
plt.figure(figsize=(10, 5))
colors = ["green" if x > -10 else "red" for x in df["from_high_%"]]
plt.bar(df["company"], df["from_high_%"], color=colors)
plt.axhline(y=0, color="black", linewidth=0.8, linestyle="--")
plt.title("% Below 52 Week High")
plt.xlabel("Company")
plt.ylabel("% From High")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("jse_from_high.png")
plt.show()

# --- Export to Excel ---
df.to_excel("jse_report.xlsx", index=False)
print("JSE report saved!")
conn.close()