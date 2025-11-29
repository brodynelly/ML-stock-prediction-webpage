from datetime import date

import pandas as pd
import streamlit as st
from plotly import graph_objs as go
from prophet.plot import plot_plotly

from stock_forecasting.utils import load_data, make_forecast, train_prophet_model

# -------------------------------
# 1. App Configuration
# -------------------------------
st.set_page_config(page_title="AI Stock Forecasting", layout="centered")
st.title("AI Stock Forecasting App")

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

stocks = ("AAPL", "GOOG", "MSFT", "GME")
selected_stock = st.selectbox("Select a stock for prediction", stocks)

n_years = st.slider("Years of prediction", 1, 4)
period = n_years * 365

# -------------------------------
# 2. Cache‑Clear Control
# -------------------------------
if st.button("Clear cached stock data"):
    st.cache_data.clear()
    st.rerun()


# -------------------------------
# 3. Data Loader
# -------------------------------
@st.cache_data(show_spinner=False)
def get_data(ticker: str) -> pd.DataFrame:
    return load_data(ticker, START, TODAY)


# Attempt to load
try:
    data = get_data(selected_stock)
    st.success(
        f"Loaded {len(data)} rows: {data['Date'].min().date()} → "
        f"{data['Date'].max().date()}"
    )
except Exception as e:
    st.error(f"Data load failed: {e}")
    st.write("Try clearing the cache and reloading the app.")
    st.stop()

# -------------------------------
# 4. Raw Data Preview & Date Range
# -------------------------------
st.subheader("🔍 Raw Data Preview")
st.write(data.tail())

st.markdown(
    f"**Date Range:** {data['Date'].min().date()} → {data['Date'].max().date()}"
)


# -------------------------------
# 5. Plot Historical Prices
# -------------------------------
def plot_historical(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Open"], name="Open"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Close"))
    fig.update_layout(
        title=f"Historical Prices: {selected_stock}",
        xaxis_rangeslider_visible=True,
        xaxis=dict(range=[START, TODAY]),
    )
    st.plotly_chart(fig, use_container_width=True)


plot_historical(data)

# -------------------------------
# 6. Prepare & Fit Prophet
# -------------------------------
st.subheader("Forecasting Model")

model = train_prophet_model(data)

# -------------------------------
# 7. Generate & Display Forecast
# -------------------------------
forecast = make_forecast(model, period)

st.subheader("Forecasted Values")
st.write(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail())

st.subheader(
    f"{selected_stock} Forecast Plot ({n_years} year{'s' if n_years > 1 else ''})"
)
fig_forecast = plot_plotly(model, forecast)
st.plotly_chart(fig_forecast, use_container_width=True)

st.subheader("Forecast Components")
fig_components = model.plot_components(forecast)
st.write(fig_components)
