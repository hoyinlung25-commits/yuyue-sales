from investment_agent.config import Settings
from investment_agent.models import Signal, TradeRecommendation
from investment_agent.risk.engine import RiskEngine


def test_position_sizing():
    engine = RiskEngine(Settings(PORTFOLIO_CAPITAL_USD=100_000, MAX_RISK_PER_TRADE_PCT=1.0))
    usd, shares, _ = engine.position_size(100.0, 98.0, Signal.BUY)
    assert usd > 0
    assert shares > 0


def test_risk_reward_rejection():
    engine = RiskEngine(Settings(MIN_RISK_REWARD_RATIO=2.0))
    ok, issues = engine.validate_trade(100, 101, 99, Signal.BUY)
    assert not ok
    assert issues
