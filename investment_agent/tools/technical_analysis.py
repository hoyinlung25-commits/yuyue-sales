"""Technical indicator analysis using pandas-ta."""

import pandas as pd

from investment_agent.models import TechnicalSnapshot


def _ensure_ohlcv_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
    out = df.copy()
    for low, proper in rename.items():
        if low in out.columns and proper not in out.columns:
            out[proper] = out[low]
    if "Close" not in out.columns:
        raise ValueError("DataFrame must contain close prices")
    return out


def analyze_technicals(ticker: str, df: pd.DataFrame) -> TechnicalSnapshot:
    """Compute RSI, MACD, SMAs, ATR and derive trend signals."""
    import pandas_ta as ta

    data = _ensure_ohlcv_columns(df)
    close = float(data["Close"].iloc[-1])

    work = data.copy()
    work.ta.rsi(length=14, append=True)
    work.ta.macd(fast=12, slow=26, signal=9, append=True)
    work.ta.sma(length=20, append=True)
    work.ta.sma(length=50, append=True)
    work.ta.atr(length=14, append=True)

    last = work.iloc[-1]
    rsi = _safe_float(last, "RSI_14")
    macd = _safe_float(last, "MACD_12_26_9")
    macd_sig = _safe_float(last, "MACDs_12_26_9")
    sma20 = _safe_float(last, "SMA_20")
    sma50 = _safe_float(last, "SMA_50")
    atr = _safe_float(last, "ATRr_14") or _safe_float(last, "ATR_14")

    signals: list[str] = []
    trend = "neutral"

    if rsi is not None:
        if rsi < 30:
            signals.append("RSI oversold — potential bounce")
        elif rsi > 70:
            signals.append("RSI overbought — caution on new longs")

    if macd is not None and macd_sig is not None:
        if macd > macd_sig:
            signals.append("MACD bullish crossover zone")
            trend = "bullish"
        else:
            signals.append("MACD bearish — momentum weakening")
            if trend != "bullish":
                trend = "bearish"

    if sma20 is not None and sma50 is not None:
        if close > sma20 > sma50:
            signals.append("Price above rising SMA stack — uptrend")
            trend = "bullish"
        elif close < sma20 < sma50:
            signals.append("Price below falling SMA stack — downtrend")
            trend = "bearish"

    if not signals:
        signals.append("No strong technical edge — wait for confirmation")

    return TechnicalSnapshot(
        ticker=ticker,
        last_close=round(close, 2),
        rsi_14=round(rsi, 2) if rsi is not None else None,
        macd=round(macd, 4) if macd is not None else None,
        macd_signal=round(macd_sig, 4) if macd_sig is not None else None,
        sma_20=round(sma20, 2) if sma20 is not None else None,
        sma_50=round(sma50, 2) if sma50 is not None else None,
        atr_14=round(atr, 2) if atr is not None else None,
        trend=trend,
        signals=signals,
    )


def _safe_float(row: pd.Series, col: str) -> float | None:
    if col not in row.index:
        return None
    val = row[col]
    if pd.isna(val):
        return None
    return float(val)
