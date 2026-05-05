import pandas as pd
import matplotlib.pyplot as plt

# Read your data
df = pd.read_csv("trades.csv")
df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
df["profit"] = df["profit"].fillna(0)

# --- Chart 1: Bar chart of profits per trade ---
plt.figure(figsize=(10, 5))
plt.bar(df["date"], df["profit"], color=["green" if x > 0 else "red" for x in df["profit"]])
plt.title("Profit Per Trade")
plt.xlabel("Date")
plt.ylabel("Profit (R)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("profit_chart.png")
plt.show()
print("Chart saved!")

# --- Chart 2: Cumulative profit over time ---
df["cumulative_profit"] = df["profit"].cumsum()

plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["cumulative_profit"], color="blue", marker="o", linewidth=2)
plt.fill_between(df["date"], df["cumulative_profit"], alpha=0.1, color="blue")
plt.title("Cumulative Profit Over Time")
plt.xlabel("Date")
plt.ylabel("Total Profit (R)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cumulative_chart.png")
plt.show()
print("Cumulative chart saved!")

# --- Chart 2: Cumulative profit over time ---
df["cumulative_profit"] = df["profit"].cumsum()

plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["cumulative_profit"], color="blue", marker="o", linewidth=2)
plt.fill_between(df["date"], df["cumulative_profit"], alpha=0.1, color="blue")
plt.title("Cumulative Profit Over Time")
plt.xlabel("Date")
plt.ylabel("Total Profit (R)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cumulative_chart.png")
plt.show()
print("Cumulative chart saved!")
df["profit"].cumsum()