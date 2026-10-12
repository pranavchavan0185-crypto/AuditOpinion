"""
engine/returns.py  --  Layer 3 (Engine)

Plain Python / pandas. No language model touches these numbers.

DEFINITIONS (see assumptions.md C1)
-----------------------------------
Event date      : the date the audited results (with the audit report) were published.
Entry price     : closing price on the event date (or the last trading day on or before it).
                  Results are often released after market hours, so the market's reaction
                  falls on the NEXT trading day, which is therefore inside the window.
Exit price      : closing price N MARKET trading days after the entry day (Nifty calendar).
Buy-and-hold return = Exit / Entry - 1
Abnormal return     = Stock return - Nifty 50 return over the SAME two dates.
"""
import pandas as pd


def _parse_dates(col):
    """Parse dates WITHOUT guessing day/month order for ISO dates.
    (Bug found by tests: dayfirst=True silently swapped month and day in 2024-06-05.)
    Accepts 2023-05-29 (ISO) or 29-MAY-2023 (NSE style); anything else is an error."""
    col = col.astype(str).str.strip()
    if col.str.match(r"^\d{4}-\d{2}-\d{2}$").all():
        return pd.to_datetime(col, format="%Y-%m-%d")
    try:
        return pd.to_datetime(col, format="%d-%b-%Y")
    except ValueError:
        return pd.to_datetime(col, format="%d-%m-%Y")


def load_prices(path):
    """Load a price CSV (Nifty or NSE stock download). Returns a Series of closing prices
    indexed by date, oldest first."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip().lower() for c in df.columns]
    date_col = [c for c in df.columns if c.startswith("date")][0]
    close_col = [c for c in df.columns if c in ("close", "close price", "closing price")][0]
    df[date_col] = _parse_dates(df[date_col])
    s = df.set_index(date_col)[close_col]
    s = pd.to_numeric(s.astype(str).str.replace(",", ""), errors="coerce").dropna()
    return s[~s.index.duplicated()].sort_index()


def entry_index(prices, event_date):
    """Position of the last trading day on or before the event date."""
    event_date = pd.Timestamp(event_date)
    pos = prices.index.searchsorted(event_date, side="right") - 1
    if pos < 0:
        raise ValueError("No price on or before the event date.")
    return pos


def window_return(prices, event_date, n_days):
    """Buy-and-hold return from the entry day to n_days trading days later.
    Returns (entry_date, exit_date, entry_price, exit_price, return)."""
    i = entry_index(prices, event_date)
    j = i + n_days
    if j >= len(prices):
        raise ValueError("Not enough price history after the event date for this window.")
    entry_p, exit_p = prices.iloc[i], prices.iloc[j]
    return prices.index[i], prices.index[j], entry_p, exit_p, exit_p / entry_p - 1


def benchmark_return_between(bench, d0, d1):
    """Benchmark return between two dates (uses the last close on or before each date)."""
    p0 = bench.asof(pd.Timestamp(d0))
    p1 = bench.asof(pd.Timestamp(d1))
    if pd.isna(p0) or pd.isna(p1):
        raise ValueError("Benchmark has no data for these dates.")
    return p1 / p0 - 1


def price_on_or_before(prices, date):
    """Last available close on or before `date`, plus how many calendar days old it is.
    A stock can miss trading days (suspension, series change); this makes that visible."""
    date = pd.Timestamp(date)
    pos = prices.index.searchsorted(date, side="right") - 1
    if pos < 0:
        raise ValueError("No stock price on or before " + str(date.date()))
    return prices.iloc[pos], (date - prices.index[pos]).days


def abnormal_return(stock, bench, event_date, n_days, max_stale_days=5):
    """Market-adjusted abnormal return = stock return - benchmark return (same two dates).

    The window is measured on the MARKET calendar (the benchmark's trading days), so every
    company is measured over the same period, even if its own series has gaps.
    Entry = last market day on or before event_date; Exit = n_days market days later.
    Stock prices are taken as the last close on or before each date. If that price is
    more than `max_stale_days` calendar days old, the function raises instead of guessing."""
    d0, d1, _, _, r_bench = window_return(bench, event_date, n_days)
    p0, stale0 = price_on_or_before(stock, d0)
    p1, stale1 = price_on_or_before(stock, d1)
    if stale0 > max_stale_days or stale1 > max_stale_days:
        raise ValueError(f"Stock price too stale at entry ({stale0}d) or exit ({stale1}d).")
    r_stock = p1 / p0 - 1
    return {"entry_date": d0, "exit_date": d1, "entry_price": p0, "exit_price": p1,
            "stock_return": r_stock, "bench_return": r_bench,
            "abnormal_return": r_stock - r_bench, "stale_days_entry": stale0, "stale_days_exit": stale1}
