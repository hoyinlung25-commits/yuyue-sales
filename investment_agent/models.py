"""Shared data models for agent state and recommendations."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class TradeRecommendation(BaseModel):
    signal: Signal
    ticker: str
    confidence: float = Field(ge=0.0, le=1.0)
    entry_price: float | None = None
    target_price: float | None = None
    stop_loss: float | None = None
    position_size_usd: float | None = None
    position_size_shares: float | None = None
    risk_reward_ratio: float | None = None
    time_horizon_days: int = 5
    rationale: str = ""
    warnings: list[str] = Field(default_factory=list)


class DailyGoalStatus(BaseModel):
    target_usd: float
    portfolio_capital_usd: float
    required_daily_return_pct: float
    estimated_trades_needed: int
    capital_needed_for_1pct_daily: float
    achievable: bool
    notes: list[str] = Field(default_factory=list)


class TechnicalSnapshot(BaseModel):
    ticker: str
    last_close: float
    rsi_14: float | None = None
    macd: float | None = None
    macd_signal: float | None = None
    sma_20: float | None = None
    sma_50: float | None = None
    atr_14: float | None = None
    trend: str = "neutral"
    signals: list[str] = Field(default_factory=list)


class AgentReport(BaseModel):
    agent_id: str
    role: str
    expertise_level: str
    summary: str
    details: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class InvestmentPlan(BaseModel):
    ticker: str
    recommendation: TradeRecommendation
    market_report: AgentReport | None = None
    research_report: AgentReport | None = None
    risk_report: AgentReport | None = None
    expert_report: AgentReport | None = None
    daily_goal: DailyGoalStatus | None = None
    disclaimer: str = (
        "This system provides educational analysis only. Not financial advice. "
        "Past performance does not guarantee future results. Trading involves risk of loss."
    )
