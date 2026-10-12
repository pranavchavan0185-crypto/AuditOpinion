"""
Tests for engine/returns.py  (Rule 5: every engine ships with a hand-worked example)

HAND-WORKED EXAMPLE 1 (tiny, check it on paper)
    Day:          1     2     3     4     5
    Stock close: 100   102   101   105   110
    Index close: 1000  1010  1005  1020  1050
    Event on day 2, window n = 2 trading days.
        Entry = day 2, Exit = day 4
        Stock return = 105/102 - 1 = 0.029412
        Index return = 1020/1010 - 1 = 0.009901
        Abnormal     = 0.029412 - 0.009901 = 0.019511

HAND-WORKED EXAMPLE 2 (real data: Nifty 50, event date 29 May 2023)
    Open data/processed/nifty50_daily.csv and look up these rows yourself:
        29-May-2023 close = 18598.65         (entry)
        28-Nov-2023 close = 19889.70         (125 trading days later)
        31-May-2024 close = 22530.70         (250 trading days later)
    125-day return = 19889.70/18598.65 - 1 = 0.069416
    250-day return = 22530.70/18598.65 - 1 = 0.211416
"""
import os
import sys

import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.returns import abnormal_return, load_prices, window_return  # noqa: E402

DATES = pd.to_datetime(["2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06"])
STOCK = pd.Series([100, 102, 101, 105, 110], index=DATES, dtype=float)
INDEX = pd.Series([1000, 1010, 1005, 1020, 1050], index=DATES, dtype=float)


def test_buy_and_hold_hand_example():
    d0, d1, p0, p1, r = window_return(STOCK, "2023-01-03", 2)
    assert (p0, p1) == (102, 105)
    assert r == pytest.approx(105 / 102 - 1)
    assert r == pytest.approx(0.029412, abs=1e-6)


def test_abnormal_return_hand_example():
    out = abnormal_return(STOCK, INDEX, "2023-01-03", 2)
    assert out["bench_return"] == pytest.approx(0.009901, abs=1e-6)
    assert out["abnormal_return"] == pytest.approx(0.019511, abs=1e-6)


def test_event_on_non_trading_day_uses_previous_close():
    # 2023-01-08 is a Sunday: entry must be the Friday 2023-01-06 close, so no room for n=1.
    with pytest.raises(ValueError):
        window_return(STOCK, "2023-01-08", 1)
    # Event on 2023-01-01 (before any data) has no price on or before it.
    with pytest.raises(ValueError):
        window_return(STOCK, "2023-01-01", 1)


def test_not_enough_history_fails_loudly():
    with pytest.raises(ValueError):
        window_return(STOCK, "2023-01-05", 3)


def test_real_nifty_hand_checked_values():
    path = os.path.join(ROOT, "data", "processed", "nifty50_daily.csv")
    if not os.path.exists(path):
        pytest.skip("nifty50_daily.csv not present")
    nifty = load_prices(path)
    d0, d125, p0, p125, r125 = window_return(nifty, "2023-05-29", 125)
    assert p0 == pytest.approx(18598.65)
    assert p125 == pytest.approx(19889.70)
    assert r125 == pytest.approx(0.069416, abs=1e-6)
    _, d250, _, p250, r250 = window_return(nifty, "2023-05-29", 250)
    assert p250 == pytest.approx(22530.70)
    assert r250 == pytest.approx(0.211416, abs=1e-6)


def test_window_follows_market_calendar_when_stock_has_gaps():
    # Stock is missing day 3 (e.g. suspended). Window is still measured on the index calendar.
    stock_gap = STOCK.drop(DATES[2])                      # no price on 2023-01-04
    out = abnormal_return(stock_gap, INDEX, "2023-01-03", 2)   # entry day 2, exit day 4
    assert out["stock_return"] == pytest.approx(105 / 102 - 1)
    # exit date has a price; now make EXIT date the missing one -> uses last close, reports staleness
    stock_gap2 = STOCK.drop(DATES[3])                     # no price on 2023-01-05 (day 4)
    out2 = abnormal_return(stock_gap2, INDEX, "2023-01-03", 2)
    assert out2["exit_price"] == 101 and out2["stale_days_exit"] == 1


def test_too_stale_price_is_rejected():
    stock_old = STOCK.iloc[:1]                            # only day-1 price exists
    with pytest.raises(ValueError):
        abnormal_return(stock_old, INDEX, "2023-01-05", 1, max_stale_days=2)


def test_mohit_hand_checked_abnormal_return():
    """HAND-WORKED EXAMPLE 3: Mohit Industries (MOHITIND), event date 29 May 2023, 250 market days.
    Look these up yourself in data/processed/MOHITIND_prices.csv and nifty50_daily.csv:
        MOHITIND close 29-May-2023 = 15.45    close 31-May-2024 = 19.95
        Nifty    close 29-May-2023 = 18598.65 close 31-May-2024 = 22530.70
    Stock return = 19.95/15.45 - 1 = 0.291262   Nifty return = 22530.70/18598.65 - 1 = 0.211416
    Abnormal return = 0.291262 - 0.211416 = 0.079846  (about +7.98 percentage points)"""
    sp = os.path.join(ROOT, "data", "processed", "MOHITIND_prices.csv")
    npth = os.path.join(ROOT, "data", "processed", "nifty50_daily.csv")
    if not (os.path.exists(sp) and os.path.exists(npth)):
        pytest.skip("price files not present")
    out = abnormal_return(load_prices(sp), load_prices(npth), "2023-05-29", 250)
    assert str(out["exit_date"].date()) == "2024-05-31"
    assert out["entry_price"] == pytest.approx(15.45) and out["exit_price"] == pytest.approx(19.95)
    assert out["abnormal_return"] == pytest.approx(0.079846, abs=1e-6)
