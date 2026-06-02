"""
Super Invest Agent orchestrator.

Multi-phase workflow inspired by TradingAgents / LangGraph patterns:
  Analyst → Research → Trader → Risk → Expert CIO

Objective: Help invest in the stock market and track progress toward
a configurable daily profit target (default $1,000 USD).
"""

from investment_agent.agents import (
    ExpertAdvisorAgent,
    MarketAnalystAgent,
    ResearchTeamAgent,
    RiskManagerAgent,
    TraderAgent,
)
from investment_agent.config import Settings, get_settings
from investment_agent.goals.daily_target import analyze_daily_goal
from investment_agent.models import InvestmentPlan, Signal
from investment_agent.risk.engine import RiskEngine


class SuperInvestAgent:
    """
    Super Investment Agent with Expert-assigned specialist team.

    Phases:
      1. Market Analyst — technicals & fundamentals
      2. Research Team — bull/bear debate
      3. Trader — trade structure
      4. Risk Manager — circuit breakers
      5. Expert CIO — final synthesis
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self.market_analyst = MarketAnalystAgent()
        self.researcher = ResearchTeamAgent()
        self.trader = TraderAgent()
        self.risk_manager = RiskManagerAgent(self.settings)
        self.expert = ExpertAdvisorAgent(self.settings)
        self.risk_engine = RiskEngine(self.settings)

    def analyze(
        self,
        ticker: str,
        daily_pnl_pct: float = 0.0,
    ) -> InvestmentPlan:
        """Run full multi-agent pipeline for a single ticker."""
        context: dict = {"ticker": ticker.upper(), "daily_pnl_pct": daily_pnl_pct}

        market_report = self.market_analyst.run(context)
        research_report = self.researcher.run(context)

        proposed = Signal.BUY if context.get("research_thesis") == "BULL" else Signal.HOLD
        context["proposed_signal"] = proposed
        risk_report = self.risk_manager.run(context)

        trader_report = self.trader.run(context)
        rec = context["trade_recommendation"]
        rec = self.risk_engine.enrich_recommendation(rec, daily_pnl_pct)

        daily_goal = analyze_daily_goal(self.settings)

        plan = InvestmentPlan(
            ticker=ticker.upper(),
            recommendation=rec,
            market_report=market_report,
            research_report=research_report,
            risk_report=risk_report,
            expert_report=None,
            daily_goal=daily_goal,
        )

        context["investment_plan"] = plan
        expert_report = self.expert.run(context)
        plan.expert_report = expert_report

        return plan

    def scan_watchlist(
        self,
        tickers: list[str],
        daily_pnl_pct: float = 0.0,
    ) -> list[InvestmentPlan]:
        """Analyze multiple tickers and return plans sorted by confidence."""
        plans: list[InvestmentPlan] = []
        for symbol in tickers:
            try:
                plans.append(self.analyze(symbol, daily_pnl_pct))
            except Exception:
                continue
        plans.sort(key=lambda p: p.recommendation.confidence, reverse=True)
        return plans
