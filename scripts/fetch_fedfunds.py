"""Download the effective federal funds rate (FRED series FEDFUNDS, monthly, percent).

Public FRED data; no API key needed. Writes data/fedfunds_monthly.csv.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS&cosd=2019-01-01"

ff = pd.read_csv(URL)
ff.columns = ["month", "fedfunds"]
ff.to_csv(ROOT / "data" / "fedfunds_monthly.csv", index=False)
print(ff["month"].min(), ff["month"].max(), len(ff), "months")
