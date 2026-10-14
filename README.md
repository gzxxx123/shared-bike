# In-Class Group Exercise: Bike Rental Dashboard
Team：Ma Manxi, Gao Ya, Guan Zixuan, Zhang Zhiqian
Dataset: UCI Bike Sharing Dataset (Kaggle)
Dataset Source: https://www.kaggle.com/datasets/uciml/bike-sharing-dataset
Data files: day.csv, hour.csv
Time range: 2011-01-01 to 2012-12-31

## Step1 — Pick a Dataset and a Decision-Maker
- Dataset: Tabular CSV (day.csv ~731 rows, <25MB). Not teaching dataset (not Iris/Titanic). Synthetic real-world bike rental log. Each row = one day of bike rental records.
- Decision-maker: **Bike Fleet Operations Manager**
> Responsible for reallocating bikes between stations, scheduling maintenance, and preparing for demand fluctuations.

## Step2 — Justify the Dashboard
1. Who looks at it, and how often?
The Fleet Operations Manager views the dashboard every weekday morning at the start of work.

2. What decision does it support?
If the Fleet Operations Manager sees a sharp drop or spike in rental demand on this dashboard, they will reallocate bikes across city stations or schedule maintenance in low-demand periods.

3. What do they do today without it — and what does that cost them in time, money, or mistakes?
Without this dashboard, the manager manually pulls CSV reports every morning. Manual sorting takes 1–2 hours daily. Slow analysis may lead to poor bike allocation: too few bikes at busy stations (lost revenue) or idle bikes at quiet stations (wasted storage cost).

4. Why a dashboard rather than a weekly email, a report, or an alert?
Demand changes every day, so weekly reports are too slow. One-off alerts only catch extreme events. The dashboard lets the manager check overall trends and seasonality every morning for routine planning.

## Step3 — Decide What Matters
EDA findings: Rental counts vary strongly by season, weather and weekday.

### Selected Dashboard Elements
- 3 Headline KPIs: Total Bike Rentals, Avg Daily Rentals, Peak Daily Rentals (visible immediately on load)
- Two supporting charts: Daily rental time trend; Average rentals across weekdays.
- Filter: Season multi-select filter (only filter the manager needs to compare seasons).

### Two things we chose NOT to show, and why
1. `atemp` (feels-like temperature): Highly correlated with raw temperature column `temp`. It does not add new business insight, showing both would clutter the dashboard without changing decisions.
2. Windspeed scatter plot: Wind speed has weak correlation with rental volume. This interesting EDA finding rarely impacts bike reallocation decisions, so it is excluded.

### Data risk that can mislead viewers
There is an outlier date (2012-10-29, Hurricane Sandy) with extremely low rentals. This abnormal day will distort average calculations.
Dashboard handling: The trend chart keeps the data point, and we add a note in the repository README explaining this outlier as a one-time extreme weather event.

### Page order justification
1. Top: 3 headline KPIs — answer "Is anything abnormal with rental demand right now?"
2. Middle: 2 supporting charts to explain *why* rental volume changed (time trend + weekday pattern)
3. Bottom: Data metadata and refresh frequency note.
No raw data table is added because the manager does not need to inspect individual daily rows.

## Step4 — Decide the Refresh Frequency
1. How often should the data be refreshed?
Nightly refresh. Rental transactions finish at the end of each day. Real-time refresh is unnecessary and costly, because bike reallocation decisions are planned once per workday.

2. How often should someone review it?
Manager reviews every weekday morning. The data refreshes overnight, ready for morning review.

3. What should be tracked over time, and what triggers action?
Track daily total rental count. If daily rental volume drops **40% below the 30-day average**, the manager will investigate station stock and weather forecasts.

4. What does stale data cost?
If data is one day out of date: Manager makes bike reallocation decisions using yesterday’s outdated demand, leading to mismatched bike supply. If data is a week stale: Seasonal demand shifts are missed, creating large shortages or surplus bikes across the city.

