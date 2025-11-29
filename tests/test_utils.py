from unittest.mock import patch

import pandas as pd
import pytest
from prophet import Prophet

from stock_forecasting.utils import load_data, make_forecast, train_prophet_model


# Sample data for testing
@pytest.fixture
def sample_data():
    dates = pd.date_range(start="2023-01-01", periods=10)
    data = pd.DataFrame(
        {
            "Date": dates,
            "Open": [100 + i for i in range(10)],
            "Close": [100 + i + 1 for i in range(10)],
        }
    )
    return data


@patch("yfinance.download")
def test_load_data_success(mock_download, sample_data):
    # Mock yfinance response
    mock_df = sample_data.copy()
    mock_df.set_index("Date", inplace=True)
    # yfinance returns index as Date
    mock_download.return_value = mock_df

    df = load_data("AAPL", "2023-01-01", "2023-01-10")

    assert not df.empty
    assert "Date" in df.columns
    assert "Close" in df.columns
    assert len(df) == 10


@patch("yfinance.download")
def test_load_data_empty(mock_download):
    mock_download.return_value = pd.DataFrame()

    with pytest.raises(ValueError, match="No data found"):
        load_data("INVALID", "2023-01-01", "2023-01-10")


def test_train_prophet_model(sample_data):
    model = train_prophet_model(sample_data)
    assert isinstance(model, Prophet)


def test_make_forecast(sample_data):
    model = train_prophet_model(sample_data)
    forecast = make_forecast(model, period=5)

    assert isinstance(forecast, pd.DataFrame)
    assert "ds" in forecast.columns
    assert "yhat" in forecast.columns
    # 10 initial points + 5 future points = 15
    assert len(forecast) == 15
