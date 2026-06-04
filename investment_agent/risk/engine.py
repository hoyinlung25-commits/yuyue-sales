"""Risk management: position sizing, circuit breakers, daily loss limits."""

from investment_agent.config import Settings
from investment_agent.models import Signal, TradeRecommendation


class RiskEngine:
    """
    Production-style risk controls inspired by institutional trading systems:
    - 1–2% risk per trade (configurable)
    - 5% daily loss circuit breaker
    - Minimum risk/reward ratio gate
    """

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()

    def position_size(
        self,
        entry: float,
        stop_loss: float,
        signal: Signal,
    ) -> tuple[float, float, list[str]]:
        """
        Return (position_usd, shares, warnings) using fixed-fractional risk.
        Risk amount = capital * max_risk_per_trade_pct.
        """
        warnings: list[str] = []
        capital = self.settings.portfolio_capital_usd
        risk_pct = self.settings.max_risk_per_trade_pct / 100
        risk_amount = capital * risk_pct

        if signal == Signal.HOLD:
            return 0.0, 0.0, ["HOLD — no position opened"]

        risk_per_share = abs(entry - stop_loss)
        if risk_per_share <= 0:
            warnings.append("Invalid stop — using 2% default stop distance")
            risk_per_share = entry * 0.02

        shares = risk_amount / risk_per_share
        position_usd = shares * entry

        max_position = capital * 0.25
        if position_usd > max_position:
            position_usd = max_position
            shares = position_usd / entry
            warnings.append("Position capped at 25% of portfolio (concentration limit)")

        return round(position_usd, 2), round(shares, 4), warnings

    def validate_trade(
        self,
        entry: float,
        target: float,
        stop_loss: float,
        signal: Signal,
        daily_pnl_pct: float = 0.0,
    ) -> tuple[bool, list[str]]:
        """Gate trades through risk/reward and daily loss rules."""
        issues: list[str] = []

        if daily_pnl_pct <= -self.settings.max_daily_loss_pct:
            issues.append(
                f"Daily loss circuit breaker: down {abs(daily_pnl_pct):.1f}% "
                f"(limit {self.settings.max_daily_loss_pct}%). Halt trading."
            )
            return False, issues

        if signal == Signal.HOLD:
            return True, issues

        risk = abs(entry - stop_loss)
        reward = abs(target - entry)
        if risk <= 0:
            issues.append("Stop loss must differ from entry")
            return False, issues

        rr = reward / risk
        if rr < self.settings.min_risk_reward_ratio:
            issues.append(
                f"Risk/reward {rr:.2f} below minimum {self.settings.min_risk_reward_ratio}"
            )
            return False, issues

        return True, issues

    def enrich_recommendation(
        self,
        rec: TradeRecommendation,
        daily_pnl_pct: float = 0.0,
    ) -> TradeRecommendation:
        """Apply sizing and validation to a recommendation."""
        if rec.entry_price is None or rec.stop_loss is None:
            return rec

        entry = rec.entry_price
        stop = rec.stop_loss
        target = rec.target_price or (
            entry + (entry - stop) * self.settings.min_risk_reward_ratio
            if rec.signal == Signal.BUY
            else entry - (stop - entry) * self.settings.min_risk_reward_ratio
        )
        rec.target_price = round(target, 2)

        ok, issues = self.validate_trade(
            entry, target, stop, rec.signal, daily_pnl_pct
        )
        rec.warnings.extend(issues)

        if not ok:
            rec.signal = Signal.HOLD
            rec.rationale += " [Risk engine downgraded to HOLD]"
            return rec

        pos_usd, shares, size_warnings = self.position_size(entry, stop, rec.signal)
        rec.position_size_usd = pos_usd
        rec.position_size_shares = shares
        rec.warnings.extend(size_warnings)

        risk = abs(entry - stop)
        reward = abs(target - entry)
        rec.risk_reward_ratio = round(reward / risk, 2) if risk > 0 else None

        return rec
