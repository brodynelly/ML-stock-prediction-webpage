# Stock Forecasting App

A Streamlit application for forecasting stock prices using [Prophet](https://facebook.github.io/prophet/) and [yfinance](https://github.com/ranaroussi/yfinance).

## Features

- **Data Loading**: Fetches historical stock data (AAPL, GOOG, MSFT, GME) from Yahoo Finance.
- **Data Visualization**: Interactive plots of historical open and close prices using Plotly.
- **Forecasting**: Predicts future stock prices for up to 4 years using the Prophet model.
- **Caching**: Efficient data loading with Streamlit's caching mechanism.

## Stack

- **Python**: 3.10+
- **Streamlit**: Web application framework.
- **Prophet**: Time series forecasting.
- **yfinance**: Market data downloader.
- **Plotly**: Interactive graphing library.
- **Pandas**: Data manipulation and analysis.

## Setup

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/stock-forecasting.git
    cd stock-forecasting
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install the package in editable mode with development dependencies:
    ```bash
    pip install -e .[dev]
    ```

## Usage

Run the Streamlit app:

```bash
streamlit run src/stock_forecasting/app.py
```

Open your browser at `http://localhost:8501`.

## Development

### Running Tests

```bash
pytest
```

### Linting and Formatting

This project uses [Ruff](https://beta.ruff.rs/docs/) for linting and formatting.

```bash
ruff check .
ruff format .
```

### Type Checking

```bash
mypy src
```

## Architecture

The application is structured as follows:

- `src/stock_forecasting/`: Source code.
    - `app.py`: Main Streamlit application entry point.
    - `utils.py`: Utility functions for data loading, model training, and forecasting.
- `tests/`: Unit tests.

## License

MIT
