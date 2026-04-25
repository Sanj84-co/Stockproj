# Stock Tracker — Technical Specification

## Overview

A FastAPI backend that lets users track stock watchlists, manage a portfolio with P&L, and set price alerts that trigger email notifications. Data is persisted in SQLite. Live prices are fetched from yfinance with a 30-second in-memory cache.

---

## Architecture

```
Stockproj/
├── src/
│   ├── fetch/
│   │   └── scrape.py          # yfinance data fetching + cleaning
│   └── main/
│       ├── api.py             # FastAPI app, endpoints, exception handlers
│       ├── Back.py            # Business logic: pnL, alert_noti, cached_checker
│       ├── storage.py         # All SQLite reads/writes
│       ├── Exceptions.py      # Custom exception classes
│       ├── watchlist.py       # Ticker validation (checkTicker)
│       └── test.py            # pytest test suite
├── conftest.py                # Adds project root to Python path for pytest
├── store.db                   # SQLite database
├── status.log                 # Application log file
└── .env                       # EMAIL_ID, EMAIL_PASSWORD (not committed)
```

---

## Database Schema

### `user`
| Column      | Type    | Notes                  |
|-------------|---------|------------------------|
| user_id     | INTEGER | Primary key, autoincrement |
| Name        | TEXT    |                        |
| time_joined | TEXT    |                        |
| email       | TEXT    | Added via ALTER TABLE  |

### `watchlist`
| Column     | Type    | Notes                          |
|------------|---------|--------------------------------|
| ticker_id  | INTEGER | Primary key, autoincrement     |
| user_id    | INTEGER | FK → user.user_id              |
| Ticker     | TEXT    |                                |
| time_added | TEXT    |                                |

### `transactions`
| Column         | Type    | Notes                          |
|----------------|---------|--------------------------------|
| transaction_id | INTEGER | Primary key, autoincrement     |
| user_id        | INTEGER | FK → user.user_id              |
| ticker         | TEXT    |                                |
| Shares         | NUMBER  |                                |
| purchase_price | REAL    | Price at time of purchase      |
| created_date   | TIMESTAMP |                              |
| status         | TEXT    | `'Bought'` or `'Sold'`        |

### `alerts`
| Column          | Type    | Notes                          |
|-----------------|---------|--------------------------------|
| alert_id        | INTEGER | Primary key, autoincrement     |
| user_id         | INTEGER | FK → user.user_id              |
| Ticker          | TEXT    |                                |
| threshold_price | REAL    | Fires when price exceeds this  |
| status          | TEXT    | `'Activated'` or `'passed'`   |

---

## API Endpoints

### Users
| Method | Path          | Description                      | Body / Params         |
|--------|---------------|----------------------------------|-----------------------|
| POST   | `/users`      | Create a new user                | `{name, email}`       |
| GET    | `/users/{name}` | Get user_id by name            | path: `name`          |
| GET    | `/user/{name}` | Get user profile (name + email) | path: `name`          |

### Watchlist
| Method | Path                        | Description              | Body / Params        |
|--------|-----------------------------|--------------------------|----------------------|
| GET    | `/watchlist/{name}`         | View user's watchlist    | path: `name`         |
| POST   | `/watchlist`                | Add ticker to watchlist  | `{name, Ticker}`     |
| DELETE | `/watchlist/{name}/{Ticker}`| Remove ticker            | path: `name, Ticker` |

### Transactions
| Method | Path                          | Description                  | Body / Params               |
|--------|-------------------------------|------------------------------|-----------------------------|
| GET    | `/transactions/{name}`        | View portfolio + P&L         | path: `name`                |
| POST   | `/transactions`               | Buy shares (create position) | `{name, Ticker, shares}`    |
| DELETE | `/transactions/{name}/{ticker}` | Sell (mark as Sold)        | path: `name, ticker`        |

### Alerts
| Method | Path                        | Description           | Body / Params               |
|--------|-----------------------------|-----------------------|-----------------------------|
| GET    | `/alerts/{Name}`            | View user's alerts    | path: `Name`                |
| POST   | `/alerts`                   | Create price alert    | `{name, Ticker, threshold}` |
| DELETE | `/alerts/{name}/{Ticker}`   | Delete alert          | path: `name, Ticker`        |

---

## Core Modules

### `Back.py` — Business Logic

**`cached_checker(ticker)`**
- Checks in-memory `cache` dict for a price entry younger than 30 seconds
- If stale or missing, calls `currentP(ticker)` from yfinance and updates cache
- Returns current price as int or float
- Logs cache hits (DEBUG) and fresh fetches (INFO)

**`pnL(item)`**
- Takes a transaction row tuple: `[_, _, ticker, shares, bought_price, date, status]`
- Calls `cached_checker(ticker)` for current price
- Returns `[total_pnl, current_price]`
- Raises `TypeError` if shares or price is a non-numeric type

**`alert_noti()`**
- Called by APScheduler every 60 seconds
- Fetches all `'Activated'` alerts via `view_allalerts()`
- For each alert: checks current price against threshold
- If price > threshold: sends email via Gmail SMTP, calls `change_status()` to mark as `'passed'`
- Logs success (INFO) and email failures (ERROR)

### `storage.py` — Data Layer

All functions open a fresh `sqlite3.connect('store.db')` connection per call. Key functions:

| Function | Description |
|---|---|
| `get_id(name)` | Returns user_id for a given name |
| `create_user(name, email, time_joined)` | Inserts new user |
| `retrieve_profile(user_id)` | Returns full user row |
| `get_user(user_id)` | Returns all watchlist rows for a user |
| `add(user_id, ticker, time_add)` | Adds to watchlist; raises `DuplicateTickerError` |
| `remove(ticker, user_id)` | Deletes from watchlist; raises `TickerNotFoundError` |
| `add_transactions(user_id, ticker, shares)` | Inserts transaction at current price |
| `sell_transaction(user_id, transaction_id)` | Sets status to `'Sold'`; raises `TransactionNotFoundError` |
| `view_transactions(user_id)` | Returns all transaction rows |
| `get_transaction_id(user_id, ticker)` | Returns transaction_id for lookup |
| `add_alerts(user_id, ticker, threshold)` | Inserts alert; raises `DuplicateAlertError` |
| `remove_alerts(ticker, user_id)` | Deletes alert; raises `AlertDoesNotExist` |
| `view_alerts(user_id)` | Returns all alert rows for a user |
| `view_allalerts()` | Returns all `'Activated'` alerts (used by scheduler) |
| `change_status(user_id, ticker)` | Sets alert status to `'passed'` after it fires |

### `watchlist.py` — Validation

**`checkTicker(name)`** — validates ticker format before any DB write:
- Raises `EmptyTickerError` if empty or None
- Raises `TooLongTickerError` if length > 5
- Raises `InavlidTickerFormatError` if not all uppercase

### `scrape.py` — Data Fetching

| Function | Description |
|---|---|
| `currentP(ticker)` | Returns current price via `yf.Ticker.info['currentPrice']` |
| `take(strs, start)` | Downloads OHLCV history via `yf.download` |
| `clean(dat)` | Fills NaN with 0, drops duplicates |

---

## Exception Handling

Custom exceptions in `Exceptions.py` are caught app-wide by `@app.exception_handler()` decorators in `api.py`.

| Exception | HTTP Status | Meaning |
|---|---|---|
| `DuplicateTickerError` | 409 Conflict | Ticker already in watchlist |
| `TickerNotFoundError` | 404 Not Found | Ticker not in watchlist |
| `EmptyTickerError` | 422 Unprocessable | Empty string submitted |
| `TooLongTickerError` | 422 Unprocessable | Ticker > 5 chars |
| `InavlidTickerFormatError` | 422 Unprocessable | Not uppercase |
| `InvalidPeriodError` | 400 Bad Request | Invalid date range |
| `AlertDoesNotExist` | 404 Not Found | Alert not found |
| `DuplicateAlertError` | 409 Conflict | Alert already exists |
| `TransactionNotFoundError` | 404 Not Found | Transaction not found |

---

## Background Jobs

APScheduler `BackgroundScheduler` is started in the FastAPI `lifespan` context:

```python
scheduler.add_job(alert_noti, 'interval', seconds=60)
```

- Starts on server startup, shuts down on shutdown
- `alert_noti()` fires every 60 seconds
- Sends email via Gmail SMTP (TLS on port 587)
- Credentials loaded from `.env` via `python-dotenv`

---

## Caching

In-memory dict in `Back.py`:

```python
cache = {
    "AAPL": {"price": 182.50, "timestamp": datetime(...)},
    ...
}
```

- TTL: 30 seconds
- Cache is per-process (not shared across workers)
- Populated on first call to `cached_checker(ticker)`

---

## Logging

Configured in `api.py` with `basicConfig`:

```python
logging.basicConfig(filename='status.log', encoding='utf-8', level=logging.DEBUG)
```

Each module gets its own logger via `logging.getLogger(__name__)`. Logged events:
- Server startup / shutdown (INFO)
- Cache hits (DEBUG)
- Fresh price fetches (INFO)
- Alert emails sent (INFO)
- Email failures (ERROR)

---

## Testing

Test file: [src/main/test.py](src/main/test.py) — run with `pytest src/main/test.py` from project root.

`conftest.py` at project root adds Stockproj to `sys.path` so imports resolve.

| Test | What it checks |
|---|---|
| `test_cachedcheck()` | Price is a positive number (int or float) |
| `test_pnL()` | P&L calculation matches manual calculation |
| `test_shares()` | `pnL()` raises `TypeError` on non-numeric shares |

**Remaining tests to write:**
- `alert_noti()` with `unittest.mock.patch` to mock `cached_checker`, `smtplib.SMTP`, and `view_allalerts`

---

## Roadmap

| Phase | Items |
|---|---|
| **Now** | Finish mocking tests for `alert_noti`, write README |
| **Week 5** | RSI indicator, buy/sell recommendations, AI explanation on alert trigger |
| **Week 6 (optional)** | React frontend consuming these endpoints |
| **High value gaps** | JWT authentication, remove `store.db` from git history |
