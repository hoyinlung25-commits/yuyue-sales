"""Bull/Bear research debate — fundamental and sentiment synthesis."""

from investment_agent.agents.base import BaseAgent
from investment_agent.models import AgentReport, TechnicalSnapshot
from investment_agent.tools.market_data import fetch_recent_news


class ResearchTeamAgent(BaseAgent):
    agent_id = "research_team"
    role = "Head of Equity Research"
    expertise_level = "Expert — Fundamental & Sentiment Analysis"
    goal = "Synthesize bull and bear cases into an investment thesis"

    def run(self, context: dict) -> AgentReport:
        ticker: str = context["ticker"]
        technicals: TechnicalSnapshot = context["technicals"]
        fundamentals: dict = context.get("fundamentals", {})
        news = fetch_recent_news(ticker)

        bull_points: list[str] = []
        bear_points: list[str] = []

        if technicals.trend == "bullish":
            bull_points.append("Technical trend supports long bias")
        elif technicals.trend == "bearish":
            bear_points.append("Technical trend favors caution or shorts")

        pe = fundamentals.get("pe_ratio")
        if pe is not None:
            if pe < 20:
                bull_points.append(f"Attractive P/E ({pe:.1f}) vs growth peers")
            elif pe > 40:
                bear_points.append(f"Elevated P/E ({pe:.1f}) — valuation risk")

        beta = fundamentals.get("beta")
        if beta is not None and beta > 1.3:
            bear_points.append(f"High beta ({beta:.2f}) — amplified drawdown risk")

        if news:
            bull_points.append(f"Active news flow ({len(news)} recent headlines)")
        else:
            bear_points.append("Limited recent news — lower catalyst visibility")

        if not bull_points:
            bull_points.append("No strong bullish catalyst identified")
        if not bear_points:
            bear_points.append("No critical bear case — monitor macro")

        thesis = "BULL" if len(bull_points) > len(bear_points) else "BEAR"
        if len(bull_points) == len(bear_points):
            thesis = "NEUTRAL"

        context["research_thesis"] = thesis
        context["bull_points"] = bull_points
        context["bear_points"] = bear_points

        summary = (
            f"Research verdict: {thesis} | Bull: {len(bull_points)} factors | "
            f"Bear: {len(bear_points)} factors"
        )

        return self._report(
            summary=summary,
            details={
                "thesis": thesis,
                "bull_case": bull_points,
                "bear_case": bear_points,
                "news": news[:3],
            },
        )
