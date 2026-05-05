import sqlite3
import pandas as pd

# Create a database (this creates a file called trades.db)
conn = sqlite3.connect("trades.db")
cursor = conn.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY,
        date TEXT,
        instrument TEXT,
        direction TEXT,
        profit REAL
    )
""")

# Insert some data
cursor.executemany("""
    INSERT INTO trades (date, instrument, direction, profit)
    VALUES (?, ?, ?, ?)
""", [
    ("2026-05-01", "US30", "BUY", 2300),
    ("2026-05-02", "US30", "SELL", -800),
    ("2026-05-03", "NAS100", "BUY", 3100),
    ("2026-05-04", "US30", "BUY", 1500),
    ("2026-05-05", "NAS100", "SELL", -400),
])

conn.commit()
print("Database created and data inserted!")

# --- SQL QUERIES ---

# 1. Select all trades
print("\n--- All Trades ---")
df = pd.read_sql_query("SELECT * FROM trades", conn)
print(df)

# 2. Only winning trades
print("\n--- Winning Trades ---")
df_wins = pd.read_sql_query("SELECT * FROM trades WHERE profit > 0", conn)
print(df_wins)

# 3. Total profit per instrument
print("\n--- Profit by Instrument ---")
df_grouped = pd.read_sql_query("""
    SELECT instrument, 
           SUM(profit) as total_profit,
           COUNT(*) as total_trades
    FROM trades
    GROUP BY instrument
""", conn)
print(df_grouped)

conn.close()