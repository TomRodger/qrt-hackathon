# QRT x CompSoc hackathon

Read by both Codex (AGENTS.md) and Claude Code (CLAUDE.md is a symlink to this file).
Keep it short and current. It's the brief every agent works from.

## Problem
<!-- Fill in when the brief drops -->
- Task:
- Data: files, rows, what one row is, time column
- Target:
- Metric: (add to `src/qrt/metrics.py`, set `CFG.metric`)
- Submission format:
- Deadline / submission limit:

## Layout
- `src/qrt/config.py`: column names, task type, metric, CV settings. Edit this first.
- `src/qrt/data.py`: loading, `feature_cols`
- `src/qrt/cv.py`: splits. Walk-forward by time when `CFG.time_col` is set.
- `src/qrt/metrics.py`: scoring, higher is better
- `src/qrt/experiment.py`: `run_cv` fits per fold and appends to `results/log.csv`
- `src/qrt/submit.py`: writes `submissions/`
- `scripts/`: runnable experiments, one file per idea
- `notebooks/`: EDA only. Anything worth keeping moves into `src/` or `scripts/`.

## Commands
- `uv sync`: install
- `uv run python scripts/baseline.py`: baseline CV + submission
- `uv run pytest`: tests
- `uv run ruff check --fix . && uv run ruff format .`: lint and format

## Rules
- Every model is scored with `run_cv` on `make_splits`. Don't hand-roll validation.
  If CV improves but the leaderboard doesn't, suspect leakage first.
- Never shuffle time-series rows across train/val. Features may only use
  information available at that row's time. No future data, no target in features.
- Data stays out of git (`data/` is ignored). So do `.env` and keys.
- No new dependencies without saying why.
- New idea = new script in `scripts/` (copy baseline.py). Don't break baseline.py.
- Small commits on your own branch, merge to main often. Commit messages: short
  subject under 72 chars, no AI attribution lines.
- Prefer simple and robust over clever. A working submission beats an unfinished model.
