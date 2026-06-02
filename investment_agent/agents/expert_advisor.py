"""Expert Advisor — lead agent with optional LLM synthesis."""

import json

from investment_agent.agents.base import BaseAgent
from investment_agent.config import Settings
from investment_agent.models import AgentReport, InvestmentPlan


class ExpertAdvisorAgent(BaseAgent):
    agent_id = "expert_advisor"
    role = "Chief Investment Officer (CIO)"
    expertise_level = "Expert — Portfolio Strategy & Daily Profit Optimization"
    goal = (
        "Orchestrate the team to help invest in stocks and progress toward "
        "the daily profit target with disciplined risk"
    )

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()

    def run(self, context: dict) -> AgentReport:
        plan: InvestmentPlan = context["investment_plan"]
        llm_summary = self._llm_synthesize(plan) if self.settings.llm_enabled else None

        action = plan.recommendation.signal.value
        target_daily = self.settings.daily_profit_target_usd

        summary = llm_summary or (
            f"CIO Decision: {action} {plan.ticker}. "
            f"Daily target ${target_daily:,.0f} requires "
            f"{plan.daily_goal.required_daily_return_pct if plan.daily_goal else 0}% "
            f"return on ${self.settings.portfolio_capital_usd:,.0f} capital. "
            f"Confidence {plan.recommendation.confidence:.0%}."
        )

        return self._report(
            summary=summary,
            details={
                "final_action": action,
                "daily_target_usd": target_daily,
                "llm_enhanced": llm_summary is not None,
            },
        )

    def _llm_synthesize(self, plan: InvestmentPlan) -> str | None:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.settings.openai_api_key)
            payload = {
                "ticker": plan.ticker,
                "recommendation": plan.recommendation.model_dump(),
                "daily_goal": plan.daily_goal.model_dump() if plan.daily_goal else {},
                "market": plan.market_report.summary if plan.market_report else "",
                "research": plan.research_report.summary if plan.research_report else "",
                "risk": plan.risk_report.summary if plan.risk_report else "",
            }
            response = client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an Expert CIO helping a client invest in US stocks "
                            "with a daily profit goal. Be concise, actionable, and always "
                            "mention risk. Never guarantee returns. Max 150 words."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Synthesize this investment plan:\n{json.dumps(payload, default=str)}",
                    },
                ],
                max_tokens=300,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception:
            return None
