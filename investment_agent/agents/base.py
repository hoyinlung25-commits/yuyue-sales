"""Base agent with expert role metadata."""

from abc import ABC, abstractmethod

from investment_agent.models import AgentReport


class BaseAgent(ABC):
    agent_id: str
    role: str
    expertise_level: str = "Expert"
    goal: str = ""

    @abstractmethod
    def run(self, context: dict) -> AgentReport:
        pass

    def _report(self, summary: str, details: dict | None = None) -> AgentReport:
        return AgentReport(
            agent_id=self.agent_id,
            role=self.role,
            expertise_level=self.expertise_level,
            summary=summary,
            details=details or {},
        )
