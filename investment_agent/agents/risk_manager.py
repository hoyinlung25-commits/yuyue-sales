"""Risk Manager — circuit breakers and position limits."""

from investment_agent.agents.base import BaseAgent
from investment_agent.config import Settings
from investment_agent.models import AgentReport, Signal


class RiskManagerAgent(BaseAgent):
    agent_id = "risk_manager"
    role = "Chief Risk Officer"
    expertise_level = "Expert — Portfolio Risk & Drawdown Control"
    goal = "Protect capital with circuit breakers and position limits"

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()

    def run(self, context: dict) -> AgentReport:
        daily_pnl_pct: float = context.get("daily_pnl_pct", 0.0)
        proposed_signal: Signal = context.get("proposed_signal", Signal.HOLD)

        checks: list[str] = []
        approved = True

        if daily_pnl_pct <= -self.settings.max_daily_loss_pct:
            checks.append("BLOCKED: Daily loss limit breached — halt all trading")
            approved = False
            context["risk_approved"] = False
        else:
            checks.append(
                f"Daily P&L {daily_pnl_pct:+.2f}% — within {self.settings.max_daily_loss_pct}% limit"
            )

        checks.append(
            f"Max risk per trade: {self.settings.max_risk_per_trade_pct}% of "
            f"${self.settings.portfolio_capital_usd:,.0f}"
        )
        checks.append(
            f"Min risk/reward: {self.settings.min_risk_reward_ratio}:1 required"
        )

        if proposed_signal != Signal.HOLD and not approved:
            context["proposed_signal"] = Signal.HOLD

        context["risk_approved"] = approved

        status = "APPROVED" if approved else "BLOCKED"
        summary = f"Risk review: {status} for {proposed_signal.value}"

        return self._report(summary=summary, details={"checks": checks, "approved": approved})
