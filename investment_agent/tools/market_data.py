"""Market data fetchers via Yahoo Finance."""

from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


def fetch_ohlcv(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
) -> pd.DataFrame:
    """Download OHLCV history and normalize column names."""
    raw = yf.download(
        ticker,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=True,
    )
    if raw.empty:
        raise ValueError(f"No market data returned for {ticker}")

    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = [str(c[0]).lower() for c in raw.columns]
    else:
        raw.columns = [str(c).lower() for c in raw.columns]

    return raw.dropna(how="all")


def fetch_quote_info(ticker: str) -> dict:
    """Fundamental and quote metadata."""
    info = yf.Ticker(ticker).info or {}
    return {
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "beta": info.get("beta"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "avg_volume": info.get("averageVolume"),
        "dividend_yield": info.get("dividendYield"),
    }


def fetch_recent_news(ticker: str, limit: int = 5) -> list[dict]:
    """Recent headlines from Yahoo Finance."""
    try:
        items = yf.Ticker(ticker).news or []
    except Exception:
        return []

    headlines: list[dict] = []
    for item in items[:limit]:
        headlines.append(
            {
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "link": item.get("link", ""),
            }
        )
    return headlines


def screen_momentum_tickers(
    tickers: list[str],
    lookback_days: int = 20,
) -> list[dict]:
    """Rank tickers by recent momentum for watchlist building."""
    ranked: list[dict] = []
    end = datetime.utcnow()
    start = end - timedelta(days=lookback_days + 10)

    for symbol in tickers:
        try:
            df = yf.download(
                symbol,
                start=start.strftime("%Y-%m-%d"),
                end=end.strftime("%Y-%m-%d"),
                progress=False,
                auto_adjust=True,
            )
            if df.empty or len(df) < lookback_days:
                continue
            close = df["Close"] if "Close" in df.columns else df.iloc[:, 0]
            momentum = (close.iloc[-1] / close.iloc[-lookback_days] - 1) * 100
            ranked.append(
                {
                    "ticker": symbol,
                    "momentum_pct": round(float(momentum), 2),
                    "last_price": round(float(close.iloc[-1]), 2),
                }
            )
        except Exception:
            continue

    return sorted(ranked, key=lambda x: x["momentum_pct"], reverse=True)
