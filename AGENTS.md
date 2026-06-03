# AGENTS.md

Guidance for cloud agents working in this repository.

## Repository layout

`main` contains only a placeholder README. Runnable products live on feature branches:

| Product | Branch | Type |
|---------|--------|------|
| **Super Investment Agent** | `cursor/super-invest-agent-ec21` | Python CLI (primary dev target) |
| **Dozeify / Axo launch kit** | `cursor/axo-execution-guide-7cb9` | Static docs, SVG/PNG assets, one optional PNG export script |

There is no monorepo, Docker Compose, or long-running web server. The investment agent is a CLI that calls Yahoo Finance over the network.

## Cursor Cloud specific instructions

### Branch checkout

Before installing or running the investment agent, check out its branch:

```bash
git fetch origin cursor/super-invest-agent-ec21
git checkout cursor/super-invest-agent-ec21
```

The Axo branch needs no install step unless you run `scripts/export-day3-png.py` (requires `cairosvg` and `Pillow`, not pinned in the repo).

### PATH

`pip install --user` puts console scripts in `~/.local/bin`. Ensure it is on `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

The `invest-agent` entry point will not be found without this.

### Install and test (Super Investment Agent)

Requires **Python 3.11+** (3.12 on the VM). From repo root after checkout:

```bash
pip install -e ".[dev]"
cp .env.example .env   # optional; defaults work without OPENAI_API_KEY
pytest -q
```

There is no configured linter (ruff/mypy) in `pyproject.toml`; use `pytest` as the quality gate.

### Run the CLI

```bash
invest-agent goal
invest-agent analyze AAPL
invest-agent scan --tickers "AAPL,NVDA,MSFT" --top 3
invest-agent momentum
```

Live commands need **outbound network** access to Yahoo Finance. `OPENAI_API_KEY` in `.env` is optional (rule-based CIO fallback without it).

### Dozeify / Axo branch

Checkout `cursor/axo-execution-guide-7cb9` to read marketing docs and assets. No server or test suite. Optional PNG export:

```bash
pip install cairosvg Pillow
python scripts/export-day3-png.py
```
