"""Trader — converts analysis into actionable trade plans."""

from investment_agent.agents.base import BaseAgent
from investment_agent.models import AgentReport, Signal, TechnicalSnapshot, TradeRecommendation


class TraderAgent(BaseAgent):
    agent_id = "trader"
    role = "Senior Equity Trader"
    expertise_level = "Expert — Execution & Trade Structuring"
    goal = "Produce precise entry, target, and stop levels"

    def run(self, context: dict) -> AgentReport:
        ticker: str = context["ticker"]
        technicals: TechnicalSnapshot = context["technicals"]
        thesis: str = context.get("research_thesis", "NEUTRAL")
        risk_approved: bool = context.get("risk_approved", True)

        entry = technicals.last_close
        atr = technicals.atr_14 or entry * 0.02

        if thesis == "BULL" and technicals.trend in ("bullish", "neutral"):
            signal = Signal.BUY
            stop = round(entry - 1.5 * atr, 2)
            target = round(entry + 3 * atr, 2)
            rationale = (
                "Bullish research + supportive technicals. Long with ATR-based stop/target."
            )
        elif thesis == "BEAR" and technicals.trend == "bearish":
            signal = Signal.SELL
            stop = round(entry + 1.5 * atr, 2)
            target = round(entry - 3 * atr, 2)
            rationale = "Bearish thesis with confirming downtrend — reduce or short."
        else:
            signal = Signal.HOLD
            stop = round(entry - atr, 2)
            target = round(entry + atr, 2)
            rationale = "Mixed signals — wait for clearer edge before deploying capital."

        confidence = 0.55
        if technicals.trend == "bullish" and thesis == "BULL":
            confidence = 0.72
        elif technicals.trend == "bearish" and thesis == "BEAR":
            confidence = 0.68

        if not risk_approved:
            signal = Signal.HOLD
            rationale = "Risk officer blocked new positions for today."

        rec = TradeRecommendation(
            signal=signal,
            ticker=ticker,
            confidence=confidence,
            entry_price=entry,
            target_price=target,
            stop_loss=stop,
            rationale=rationale,
        )
        context["trade_recommendation"] = rec

        return self._report(
            summary=f"Trade plan: {signal.value} {ticker} @ ${entry}",
            details=rec.model_dump(),
        )
