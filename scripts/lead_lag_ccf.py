"""Lead-lag check: do QQQ changes line up with Data Analytics posting changes months later?

Saved from the Data Visualization page for the time-series modeling page (ARIMAX lag choice).
Run from the project root: py scripts/lead_lag_ccf.py

Result as of May 2026 data (Dec 2020 to May 2026, 65 monthly log changes):
same-month correlation about -0.02; peak about 0.33 when stocks lead by 6 months;
near 0.3 out to 10 months; rough significance band +/- 0.25.
On the modeling page, consider prewhitening (fit an ARIMA to QQQ changes, filter both
series with it) before reading the cross-correlations.
"""
import numpy as np
import pandas as pd

sectors = pd.read_csv("data/IndeedSectorJobPostings.csv", parse_dates=["dateString"])
sectors = sectors[sectors["sectorName"] == "Data & Analytics"]
sectors["month"] = sectors["dateString"].dt.to_period("M").dt.to_timestamp()
da = sectors.groupby("month")["value"].mean().loc[:"2026-05-01"]

qqq = (pd.read_csv("data/stocks_monthly.csv", parse_dates=["month"])
       .set_index("month").loc[:"2026-05-01", "QQQ"])

both = pd.concat([da, qqq], axis=1, keys=["Data Analytics", "QQQ"]).dropna()
changes = np.log(both).diff()

lags = range(0, 13)
ccf = pd.Series({k: changes["Data Analytics"].corr(changes["QQQ"].shift(k)) for k in lags},
                name="corr")
band = 2 / np.sqrt(changes.dropna().shape[0])

print(f"Levels correlation: {both['Data Analytics'].corr(both['QQQ']):.2f}")
print(f"Significance band: +/- {band:.2f}")
print("Correlation of DA change with QQQ change k months earlier:")
print(ccf.round(2).to_string())
