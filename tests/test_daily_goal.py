from investment_agent.config import Settings
from investment_agent.goals.daily_target import analyze_daily_goal


def test_daily_goal_capital_math():
    s = Settings(
        DAILY_PROFIT_TARGET_USD=1000,
        PORTFOLIO_CAPITAL_USD=100_000,
    )
    status = analyze_daily_goal(s)
    assert status.target_usd == 1000
    assert status.required_daily_return_pct == 1.0
    assert status.capital_needed_for_1pct_daily == 100_000


def test_daily_goal_high_target_notes():
    s = Settings(
        DAILY_PROFIT_TARGET_USD=1000,
        PORTFOLIO_CAPITAL_USD=10_000,
    )
    status = analyze_daily_goal(s)
    assert status.required_daily_return_pct == 10.0
    assert not status.achievable
