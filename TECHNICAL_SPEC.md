# Stock Tracker — Technical Specification

## Overview

A FastAPI backend that lets users track stock watchlists, manage a portfolio with P&L, and set price alerts that trigger email notifications. Data is persisted in SQLite. Live prices are fetched from yfinance with a 30-second in-memory cache. An RSI-based AI layer provides buy/sell/hold recommendations.

---

## Project Structure

```
Stockproj/
├── src/
│   ├── fetch/
│   │   └── scrape.py           # yfinance price fetching and historical data
│   └── main/
│       ├── api.py              # FastAPI app, endpoints, exception handlers, scheduler
│       ├── Back.py             # Business logic: pnL, alert_noti, cached_checker, retrieve_recommendation
│       ├── storage.py          # All SQLite reads and writes
│       ├── Exceptions.py       # Custom exception classes
│       ├── indicatorStock.py   # RSI calculation and buy/sell/hold recommendation
│       ├── watchlist.py        # Ticker input validation (checkTicker)
│       └── visual.py           # Candlestick charting (mplfinance, matplotlib)
├── tests/
│   └── test.py                 # pytest unit and mock tests
├── conftest.py                 # Makes project root discoverable by pytest
├── data/
│   └── store.db                # SQLite database
└── .env                        # EMAIL_ID, EMAIL_PASSWORD (not committed)
```

---

## Database Schema

**user**
| Column      | Type    | Notes                       |
|-------------|---------|-----------------------------|
| user_id     | INTEGER | Primary key, auto-increment |
| Name        | TEXT    |                             |
| time_joined | TEXT    |                             |
| email       | TEXT    | Added via ALTER TABLE       |

**watchlist**
| Column     | Type    | Notes                          |
|------------|---------|--------------------------------|
| ticker_id  | INTEGER | Primary key, auto-increment    |
| user_id    | INTEGER | Foreign key → user(user_id)    |
| Ticker     | TEXT    |                                |
| time_added | TEXT    |                                |

**transactions**
| Column         | Type      | Notes                          |
|----------------|-----------|--------------------------------|
| transaction_id | INTEGER   | Primary key, auto-increment    |
| user_id        | INTEGER   | Foreign key → user(user_id)    |
| ticker         | TEXT      |                                |
| Shares         | NUMBER    |                                |
| purchase_price | REAL      | Fetched from yfinance at buy   |
| created_date   | TIMESTAMP |                                |
| status         | TEXT      | 'Bought' or 'Sold'             |

**alerts**
| Column          | Type    | Notes                          |
|-----------------|---------|--------------------------------|
| alert_id        | INTEGER | Primary key, auto-increment    |
| user_id         | INTEGER | Foreign key → user(user_id)    |
| Ticker          | TEXT    |                                |
| threshold_price | REAL    |                                |
| status          | TEXT    | 'Activated' or 'passed'        |

---

## API Endpoints

### Users
| Method | Path          | Body / Params    | Returns               |
|--------|---------------|------------------|-----------------------|
| POST   | /users        | `{name, email}`  | `{name, user_id}`     |
| GET    | /users/{name} | path: name       | `{name, user_id}`     |
| GET    | /user/{name}  | path: name       | `{name, email}`       |

### Watchlist
| Method | Path                       | Body / Params    | Returns                                        |
|--------|----------------------------|------------------|------------------------------------------------|
| GET    | /watchlist/{name}          | path: name       | `{watchlist: [{Stock, Time-added}]}`           |
| POST   | /watchlist                 | `{name, Ticker}` | `{Ticker, Date-added}`                         |
| DELETE | /watchlist/{name}/{Ticker} | path: name, Ticker | `{Ticker, Date-Removed}`                     |

### Transactions
| Method | Path                           | Body / Params            | Returns                                                           |
|--------|--------------------------------|--------------------------|-------------------------------------------------------------------|
| GET    | /transactions/{name}           | path: name               | `{transactions: [{Ticker, shares, Bought Price, Current Price, PnL, Status}]}` |
| POST   | /transactions                  | `{name, Ticker, shares}` | `{transaction: {Name, Ticker, Shares, Status}}`                   |
| DELETE | /transactions/{name}/{ticker}  | path: name, ticker       | `{name, ticker}`                                                  |

### Alerts
| Method | Path                    | Body / Params                  | Returns                                          |
|--------|-------------------------|--------------------------------|--------------------------------------------------|
| GET    | /alerts/{Name}          | path: Name                     | `{alerts: [{name, Ticker, Threshold, Status}]}`  |
| POST   | /alerts                 | `{name, Ticker, threshold}`    | `{name, Ticker, threshold}`                      |
| DELETE | /alerts/{name}/{Ticker} | path: name, Ticker             | `{name, Ticker}`                                 |

### AI Recommendation
| Method | Path                     | Params             | Returns                                    |
|--------|--------------------------|--------------------|--------------------------------------------|
| GET    | /Review/{name}/{Ticker}  | path: name, Ticker | String: Buy / Hold / Sell recommendation   |

---

## Business Logic (Back.py)

### `cached_checker(ticker) → float`
- Checks the in-memory `cache` dict for the ticker
- Cache entry expires after 30 seconds (checked via timestamp diff)
- On miss: calls `currentP(ticker)` from scrape.py and stores `{price, timestamp}`
- On hit: returns stored price without a network call
- Logs cache hits (DEBUG) and fetches (INFO) to `status.log`

### `pnL(item) → [total_pnl, current_price]`
- `item` is a transaction row tuple: `[transaction_id, user_id, ticker, shares, purchase_price, created_date, status]`
- Fetches current price via `cached_checker`
- Returns `[total_pnl, current_price]` where `total_pnl = (shares × current_price) − (shares × purchase_price)`

### `alert_noti()`
- Called by APScheduler every 60 seconds
- Fetches all alerts with `status = 'Activated'` via `view_allalerts()`
- For each alert: fetches current price via `cached_checker`
- If `current_price > threshold`: sends email via Gmail SMTP (STARTTLS, port 587), then marks alert `'passed'` via `change_status()`
- Credentials loaded from `.env` via `python-dotenv`
- Logs email success/failure to `status.log`

### `retrieve_recommendation(Ticker) → str`
- Fetches 30 days of historical close prices via `take(Ticker, start_date)`
- Instantiates `stockalgo` and calls `.recommend()`
- Returns one of three strings (see RSI Layer below)

---

## RSI Layer (indicatorStock.py)

**Class `stockalgo`**

| Method | Description |
|--------|-------------|
| `__init__(df)` | Takes a pandas Series of close prices |
| `Rsi()` | Computes 14-period RSI using daily percent change, rolling mean of gains/losses; stores in `self.rsi` |
| `recommend()` | Reads latest RSI value, returns buy/hold/sell string |

**RSI thresholds:**
- `RSI > 70` → overbought → "The stock is overbought. Sell"
- `30 < RSI < 70` → neutral → "It is undetermined right now. Please hold the stock."
- `RSI ≤ 30` → oversold → "The stock is oversold. Buy"

---

## Input Validation (watchlist.py)

`checkTicker(name)` validates all ticker inputs before database operations:

| Condition              | Exception raised         |
|------------------------|--------------------------|
| Empty string or None   | `EmptyTickerError`       |
| Length > 5 characters  | `TooLongTickerError`     |
| Not all uppercase      | `InavlidTickerFormatError` |

---

## Exception Handling (api.py)

Global exception handlers registered with `@app.exception_handler()`:

| Exception               | HTTP Status     | Message                              |
|-------------------------|-----------------|--------------------------------------|
| `DuplicateTickerError`  | 409 Conflict    | "Ticker already exists."             |
| `TickerNotFoundError`   | 404 Not Found   | "Ticker not Found"                   |
| `EmptyTickerError`      | 422 Unprocessable | "Entered an empty string for ticker" |
| `TooLongTickerError`    | 422 Unprocessable | "Input is too long!"                 |
| `InavlidTickerFormatError` | 422 Unprocessable | "Invalid ticker"                  |
| `InvalidPeriodError`    | 400 Bad Request | "Period is too long"                 |
| `AlertDoesNotExist`     | 404 Not Found   | "Alert is not found"                 |
| `DuplicateAlertError`   | 409 Conflict    | "Alert already exists"               |
| `TransactionNotFoundError` | 404 Not Found | "This transaction has not been made" |

---

## Background Scheduler

- Library: APScheduler (`BackgroundScheduler`)
- Configured in the FastAPI `lifespan` context manager
- Job: `alert_noti`, interval: every 60 seconds
- Starts on server startup, shuts down on server shutdown
- Startup and shutdown events logged to `status.log`

---

## Logging

- Library: Python `logging`, configured in `api.py`
- Output file: `status.log`, encoding UTF-8, level DEBUG
- Each module creates its own logger via `logging.getLogger(__name__)`
- Key log events: server start/stop, cache hits/misses, email sent/failed

---

## Data Fetching (scrape.py)

| Function | Description |
|----------|-------------|
| `currentP(ticker)` | Returns current price via `yf.Ticker(ticker).info['currentPrice']` |
| `take(ticker, start)` | Downloads historical OHLCV data via `yf.download`, cleans nulls and duplicates |
| `clean(dat)` | Fills NaN with 0, removes duplicate rows |

---

## Testing (tests/test.py)

| Test | What it covers |
|------|----------------|
| `test_cachedcheck()` | `cached_checker('AAPL')` returns a positive number |
| `test_pnL()` | `pnL()` returns correct P&L against known inputs |
| `test_shares()` | `pnL()` raises `TypeError` when shares is a string |
| `test_alerts()` | `alert_noti()` triggers SMTP when price exceeds threshold (all external calls mocked) |

**Mocks used in `test_alerts`:**
- `src.main.Back.cached_checker` → returns `302.0`
- `src.main.Back.view_allalerts` → returns one fake alert with threshold `300.0`
- `src.main.Back.retrieve_profile` → returns fake user row with email at last index
- `src.main.Back.sm.SMTP` → asserts it was called (no real email sent)

---

## Known Issues

| Issue | Impact |
|-------|--------|
| No JWT authentication | Any caller can act as any user — all endpoints are open |
| `store.db` may be committed to GitHub | Exposes all user data publicly |
| `/Review` endpoint bug | `if Ticker in check_watchlist` — `check_watchlist` is a bool, not iterable; raises `TypeError` at runtime |
| `mVA()` in `stockalgo` is unused | `enumerate` returns tuples; adding them to `sum` would fail if called |
| `test_alerts` threshold mismatch | Fake alert status is `'activated'` (lowercase) but `view_allalerts` filters for `'Activated'` — mock bypasses this but real data would not trigger |

---

## Roadmap

| Phase | Items |
|-------|-------|
| **Now** | Fix `/Review` endpoint bug; add README |
| **High value** | JWT authentication, add `.gitignore` for `store.db` |
| **Week 5** | Expand AI layer (RSI already implemented) |
| **Week 6** | React frontend consuming these endpoints (optional) |
