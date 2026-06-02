"""Market Analyst — technical and price action expert."""

from investment_agent.agents.base import BaseAgent
from investment_agent.models import AgentReport, TechnicalSnapshot
from investment_agent.tools.market_data import fetch_ohlcv, fetch_quote_info
from investment_agent.tools.technical_analysis import analyze_technicals


class MarketAnalystAgent(BaseAgent):
    agent_id = "market_analyst"
    role = "Senior Market Analyst"
    expertise_level = "Expert — Technical Analysis & Price Action"
    goal = "Analyze charts, indicators, and price structure for trade setups"

    def run(self, context: dict) -> AgentReport:
        ticker: str = context["ticker"]
        df = context.get("ohlcv") or fetch_ohlcv(ticker)
        technicals: TechnicalSnapshot = context.get("technicals") or analyze_technicals(
            ticker, df
        )
        fundamentals = fetch_quote_info(ticker)

        context["ohlcv"] = df
        context["technicals"] = technicals
        context["fundamentals"] = fundamentals

        summary = (
            f"{ticker} @ ${technicals.last_close} | Trend: {technicals.trend.upper()} | "
            f"RSI: {technicals.rsi_14} | Key: {technicals.signals[0] if technicals.signals else 'N/A'}"
        )

        return self._report(
            summary=summary,
            details={
                "technicals": technicals.model_dump(),
                "fundamentals": fundamentals,
            },
        )
