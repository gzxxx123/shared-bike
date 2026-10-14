import pandas as pd
import streamlit as st

# ---------- Load ----------
@st.cache_data
def load():
    day = pd.read_csv("day.csv", parse_dates=["dteday"])
    hour = pd.read_csv("hour.csv", parse_dates=["dteday"])
    return day, hour

day, hour = load()

SEASON = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
WEATHER = {1: "Clear / Cloudy", 2: "Mist / Cloudy", 3: "Light Rain / Snow", 4: "Heavy Rain / Snow"}
YR = {0: "2011", 1: "2012"}

# ---------- Title + caption (Step 5.1, 5.2) ----------
st.title("🚲 cycleWarning — Bike-Share Demand Monitor")
st.caption(
    "For the Bike-Share Fleet Operations Manager: decide where to rebalance bikes, "
    "how many drivers to deploy, and when to pause maintenance — every morning."
)

# ---------- Filters (Step 5.5) ----------
with st.sidebar:
    st.header("Filters")
    years = st.multiselect("Year", options=[0, 1], format_func=lambda y: YR[y], default=[0, 1])
    seasons = st.multiselect("Season", options=[1, 2, 3, 4], format_func=lambda s: SEASON[s], default=[1, 2, 3, 4])
    day_type = st.radio(
        "Day type",
        options=["All", "Working day", "Weekend / Holiday"],
        index=0,
    )

d = day[day.yr.isin(years) & day.season.isin(seasons)].copy()
if day_type == "Working day":
    d = d[d.workingday == 1]
elif day_type == "Weekend / Holiday":
    d = d[d.workingday == 0]

# ---------- Headline metrics (Step 5.3) ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total rides in view", f"{d.cnt.sum():,}")
col2.metric("Average rides / day", f"{d.cnt.mean():,.0f}")
col3.metric(
    "Member : Casual",
    f"{d.registered.sum() / d.cnt.sum() * 100:.0f}% : {d.casual.sum() / d.cnt.sum() * 100:.0f}%",
)

# ---------- Chart 1: daily trend with rolling line ----------
st.subheader("Daily rides, with 30-day rolling average")
trend = d.set_index("dteday").cnt
roll = trend.rolling(30).mean()
st.line_chart(pd.DataFrame({"Daily rides": trend, "30-day avg": roll}))
st.caption(
    "Note: the sharp drop on 2012-10-29 (22 rides) is Hurricane Sandy, not a demand collapse."
)

# ---------- Chart 2: hourly profile, weekday vs weekend ----------
st.subheader("Hourly demand profile: working day vs weekend")
h = hour[hour.yr.isin(years) & hour.season.isin(seasons)]
wk = h[h.workingday == 1].groupby("hr").cnt.mean()
we = h[h.workingday == 0].groupby("hr").cnt.mean()
st.line_chart(pd.DataFrame({"Working day": wk, "Weekend / Holiday": we}))
st.caption("Two commute peaks (8am, 5–6pm) on working days; a broad midday leisure peak on weekends.")

# ---------- Detail table (bottom, optional dig-in) ----------
with st.expander("Underlying daily detail (top 10 days)"):
    st.dataframe(
        d.sort_values("cnt", ascending=False)[
            ["dteday", "season", "weathersit", "workingday", "casual", "registered", "cnt"]
        ].assign(
            season=lambda x: x.season.map(SEASON),
            weathersit=lambda x: x.weathersit.map(WEATHER),
        ).head(10),
        use_container_width=True,
    )

# ---------- Data period + refresh line (Step 5.6) ----------
st.info(
    "Data: 2011-01-01 – 2012-12-31, Kaggle/UCI frozen snapshot. "
    "In production this would refresh nightly; the Operations Manager reviews it each weekday morning."
)
