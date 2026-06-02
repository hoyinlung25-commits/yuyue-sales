"""Daily $1000 profit goal planner and feasibility analysis."""

from investment_agent.config import Settings
from investment_agent.models import DailyGoalStatus


def analyze_daily_goal(settings: Settings | None = None) -> DailyGoalStatus:
    """
    Map the $1000/day objective to required returns and capital.
    Educates the user on realistic capital needs — not a guarantee of returns.
    """
    s = settings or Settings()
    target = s.daily_profit_target_usd
    capital = s.portfolio_capital_usd
    required_pct = s.required_daily_return_pct

    notes: list[str] = []
    achievable = False

    if required_pct <= 0.5:
        achievable = True
        notes.append(
            f"Target requires ~{required_pct:.2f}% daily return — aggressive but within "
            "professional day-trader ranges on a large account."
        )
    elif required_pct <= 1.0:
        achievable = True
        notes.append(
            f"Target requires ~{required_pct:.2f}% daily — typical for skilled intraday "
            "traders with disciplined risk (1% risk/trade, 55%+ win rate)."
        )
    elif required_pct <= 2.0:
        notes.append(
            f"Target requires ~{required_pct:.2f}% daily — very aggressive. Consider "
            "increasing capital or adjusting the daily target."
        )
    else:
        notes.append(
            f"Target requires ~{required_pct:.2f}% daily — unrealistic for sustained "
            "equity trading without extreme leverage and risk."
        )

    capital_for_1pct = target / 0.01
    capital_for_05pct = target / 0.005

    notes.append(
        f"Capital needed for $1,000/day at 1% daily return: ${capital_for_1pct:,.0f}"
    )
    notes.append(
        f"Capital needed for $1,000/day at 0.5% daily return: ${capital_for_05pct:,.0f}"
    )

    trades_needed = _estimate_trades(required_pct, s.max_risk_per_trade_pct)
    notes.append(
        "Use max 5% daily loss limit and 1% risk per trade (3-5-7 rule variant)."
    )

    return DailyGoalStatus(
        target_usd=target,
        portfolio_capital_usd=capital,
        required_daily_return_pct=round(required_pct, 3),
        estimated_trades_needed=trades_needed,
        capital_needed_for_1pct_daily=round(capital_for_1pct, 2),
        achievable=achievable,
        notes=notes,
    )


def _estimate_trades(required_daily_pct: float, risk_per_trade_pct: float) -> int:
    """Rough estimate of winning trades if each winner captures ~2R."""
    if risk_per_trade_pct <= 0:
        return 0
    avg_win_pct = risk_per_trade_pct * 2
    if avg_win_pct <= 0:
        return 0
    return max(1, int(required_daily_pct / avg_win_pct) + 1)
