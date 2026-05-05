# JSE Stock Analyzer

Analyzes live Johannesburg Stock Exchange stock prices including
Naspers, Anglo American, Sasol, Standard Bank and MTN.

## Features
- Live JSE stock prices in ZAR
- 52 week high and low tracking
- Distance from 52 week high calculation
- Stock price comparison charts
- SQLite database storage
- Excel report export

## Technologies
Python, Pandas, Matplotlib, SQLite, yfinance

## How to Run
1. Install requirements: pip install pandas matplotlib yfinance openpyxl
2. Run: python jse_analyzer.py

## Stocks Tracked
| Company | Ticker |
|---|---|
| Naspers | NPN.JO |
| Anglo American | AGL.JO |
| Sasol | SOL.JO |
| Standard Bank | SBK.JO |
| MTN | MTN.JO |

## Output
- jse_prices.png
- jse_from_high.png
- jse_report.xlsx
- jse.db

## Author
Nkwe Oreabetse Lehulere
Aspiring Data Analyst | South Africa