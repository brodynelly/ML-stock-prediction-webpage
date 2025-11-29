import logging

import pandas as pd
import yfinance as yf
from prophet import Prophet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Loads stock data from yfinance for a given ticker and date range.

    Args:
        ticker: The stock ticker symbol.
        start_date: The start date in 'YYYY-MM-DD' format.
        end_date: The end date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: The loaded and cleaned data.
    """
    try:
        # Download data from yfinance
        df = yf.download(ticker, start_date, end_date, progress=False)

        if df.empty:
            raise ValueError(f"No data found for ticker {ticker}.")

        # Handle MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            logger.info("MultiIndex columns detected, flattening...")
            df.columns = [col[0] for col in df.columns]

        # Ensure a proper Date column
        df["Date"] = df.index
        df = df.reset_index(drop=True)

        # Clean and validate dates
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        # Clean and validate Close prices
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.dropna(subset=["Close"])

        # Final validation
        if df.empty:
            raise ValueError("After cleaning, no valid data remains.")

        return df

    except Exception as e:
        logger.error(f"Error in load_data: {str(e)}")
        raise ValueError(f"Failed to load data for {ticker}: {str(e)}")


def train_prophet_model(data: pd.DataFrame) -> Prophet:
    """
    Trains a Prophet model on the given data.

    Args:
        data: DataFrame containing 'Date' and 'Close' columns.

    Returns:
        Prophet: The trained Prophet model.
    """
    df_train = data[["Date", "Close"]].copy()
    df_train.columns = ["ds", "y"]
    df_train = df_train.dropna(subset=["ds", "y"])

    model = Prophet()
    model.fit(df_train)
    return model


def make_forecast(model: Prophet, period: int) -> pd.DataFrame:
    """
    Generates a forecast using the trained model.

    Args:
        model: The trained Prophet model.
        period: Number of days to forecast.

    Returns:
        pd.DataFrame: The forecast DataFrame.
    """
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)
    return forecast
