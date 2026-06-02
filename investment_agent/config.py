"""Application configuration and daily profit goal settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    daily_profit_target_usd: float = Field(
        default=1000.0, alias="DAILY_PROFIT_TARGET_USD"
    )
    portfolio_capital_usd: float = Field(
        default=100_000.0, alias="PORTFOLIO_CAPITAL_USD"
    )
    max_risk_per_trade_pct: float = Field(
        default=1.0, alias="MAX_RISK_PER_TRADE_PCT"
    )
    max_daily_loss_pct: float = Field(default=5.0, alias="MAX_DAILY_LOSS_PCT")
    min_risk_reward_ratio: float = Field(default=1.5, alias="MIN_RISK_REWARD_RATIO")

    @property
    def llm_enabled(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.strip())

    @property
    def required_daily_return_pct(self) -> float:
        if self.portfolio_capital_usd <= 0:
            return 0.0
        return (self.daily_profit_target_usd / self.portfolio_capital_usd) * 100


def get_settings() -> Settings:
    return Settings()
