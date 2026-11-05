"""Aggregate daily Yahoo Finance closes to monthly averages for the Data Visualization page.

Reads the raw daily files from the parent DSAN/data folder (kept out of the repo) and
writes data/stocks_monthly.csv. Only complete months are kept.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / "data"

stocks = pd.read_csv(RAW / "all_stocks_wide.csv", parse_dates=["Date"])
qqq = pd.read_csv(RAW / "qqq_stock.csv")
qqq["Date"] = pd.to_datetime(qqq["Date"], format="%m/%d/%Y")

daily = stocks.merge(qqq, on="Date", how="inner").rename(columns={"AI": "C3.ai"})
daily["month"] = daily["Date"].dt.to_period("M").dt.to_timestamp()
monthly = daily.groupby("month")[["QQQ", "NVDA", "MSFT", "GOOGL", "C3.ai"]].mean().round(2)

# drop the final month if the daily data stops before its last trading week
last_day = daily["Date"].max()
if last_day < (last_day + pd.offsets.MonthEnd(0)) - pd.Timedelta(days=5):
    monthly = monthly.iloc[:-1]

monthly.to_csv(ROOT / "data" / "stocks_monthly.csv")
print(monthly.index.min().date(), monthly.index.max().date(), len(monthly), "months")
