"""Command-line interface for the Super Investment Agent."""

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investment_agent import SuperInvestAgent
from investment_agent.config import get_settings
from investment_agent.goals.daily_target import analyze_daily_goal
from investment_agent.tools.market_data import screen_momentum_tickers

app = typer.Typer(
    name="invest-agent",
    help="Super Investment Agent — Expert multi-agent stock advisory system",
)
console = Console()


@app.command()
def analyze(
    ticker: str = typer.Argument(..., help="Stock ticker e.g. AAPL, NVDA"),
    daily_pnl: float = typer.Option(
        0.0, "--daily-pnl", help="Today's portfolio P&L %% (for circuit breaker)"
    ),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON"),
):
    """Run full expert agent analysis on a ticker."""
    agent = SuperInvestAgent()
    plan = agent.analyze(ticker, daily_pnl_pct=daily_pnl)

    if json_out:
        console.print_json(plan.model_dump_json(indent=2))
        return

    _print_plan(plan)


@app.command()
def goal():
    """Show daily $1000 profit goal feasibility and capital requirements."""
    status = analyze_daily_goal()
    table = Table(title="Daily Profit Goal Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Target (USD/day)", f"${status.target_usd:,.2f}")
    table.add_row("Your capital", f"${status.portfolio_capital_usd:,.2f}")
    table.add_row("Required daily return", f"{status.required_daily_return_pct}%")
    table.add_row("Capital @ 1%/day", f"${status.capital_needed_for_1pct_daily:,.0f}")
    table.add_row("Est. winning trades", str(status.estimated_trades_needed))
    table.add_row("Achievable?", "Yes" if status.achievable else "Challenging")
    console.print(table)
    for note in status.notes:
        console.print(f"  • {note}")


@app.command()
def scan(
    tickers: str = typer.Option(
        "AAPL,MSFT,NVDA,GOOGL,AMZN,META,TSLA,AMD,SPY,QQQ",
        "--tickers",
        help="Comma-separated watchlist",
    ),
    top: int = typer.Option(3, "--top", help="Show top N by confidence"),
):
    """Scan watchlist and rank by agent confidence."""
    symbols = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    agent = SuperInvestAgent()
    plans = agent.scan_watchlist(symbols)[:top]

    table = Table(title="Top Opportunities")
    table.add_column("Ticker")
    table.add_column("Signal")
    table.add_column("Confidence")
    table.add_column("Entry")
    table.add_column("Target")
    table.add_column("Stop")
    for p in plans:
        r = p.recommendation
        table.add_row(
            p.ticker,
            r.signal.value,
            f"{r.confidence:.0%}",
            str(r.entry_price),
            str(r.target_price),
            str(r.stop_loss),
        )
    console.print(table)


@app.command()
def momentum(
    tickers: str = typer.Option(
        "AAPL,MSFT,NVDA,GOOGL,AMZN,META,TSLA,AMD,SPY,QQQ,IWM",
        "--tickers",
    ),
):
    """Rank tickers by 20-day price momentum."""
    symbols = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    ranked = screen_momentum_tickers(symbols)
    table = Table(title="Momentum Rankings (20d)")
    table.add_column("Ticker")
    table.add_column("Momentum %")
    table.add_column("Price")
    for row in ranked:
        table.add_row(row["ticker"], f"{row['momentum_pct']:+.2f}%", f"${row['last_price']}")
    console.print(table)


@app.command()
def config():
    """Show current configuration."""
    s = get_settings()
    data = {
        "daily_profit_target_usd": s.daily_profit_target_usd,
        "portfolio_capital_usd": s.portfolio_capital_usd,
        "max_risk_per_trade_pct": s.max_risk_per_trade_pct,
        "max_daily_loss_pct": s.max_daily_loss_pct,
        "min_risk_reward_ratio": s.min_risk_reward_ratio,
        "llm_enabled": s.llm_enabled,
        "openai_model": s.openai_model,
    }
    console.print(Panel(json.dumps(data, indent=2), title="Agent Configuration"))


def _print_plan(plan) -> None:
    r = plan.recommendation
    console.print(
        Panel(
            f"[bold]{r.signal.value}[/bold] {plan.ticker}\n"
            f"Confidence: {r.confidence:.0%}\n"
            f"Entry: ${r.entry_price} | Target: ${r.target_price} | Stop: ${r.stop_loss}\n"
            f"Size: ${r.position_size_usd} ({r.position_size_shares} shares)\n"
            f"R:R {r.risk_reward_ratio}\n\n"
            f"{r.rationale}",
            title="Trade Recommendation",
            border_style="green" if r.signal.value == "BUY" else "yellow",
        )
    )

    if plan.expert_report:
        console.print(
            Panel(plan.expert_report.summary, title="Expert CIO (Chief Investment Officer)")
        )

    if plan.daily_goal:
        g = plan.daily_goal
        console.print(
            Panel(
                f"Daily target: ${g.target_usd:,.0f} | "
                f"Required return: {g.required_daily_return_pct}% | "
                f"Capital for 1%/day: ${g.capital_needed_for_1pct_daily:,.0f}",
                title="Daily Profit Goal",
            )
        )

    if r.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for w in r.warnings:
            console.print(f"  • {w}")

    console.print(f"\n[dim]{plan.disclaimer}[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
