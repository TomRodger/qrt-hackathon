# qrt-hackathon

## Setup
```bash
git clone https://github.com/TomRodger/qrt-hackathon && cd qrt-hackathon
uv sync
cp .env.example .env        # add your own API key, never commit it
```

macOS: LightGBM needs OpenMP. If importing it fails, run `brew install libomp`.

## Dry run (before real data)
```bash
uv run python scripts/make_fake_data.py
uv run python scripts/baseline.py
uv run pytest
```
LightGBM should beat the dummy model on fake data. Delete `data/*.csv` before
the real data goes in.

## When the brief drops
1. Put the data in `data/`, fill in the Problem section of `AGENTS.md`.
2. Set columns, task, metric and CV in `src/qrt/config.py`.
3. Run `scripts/baseline.py` and submit the result.
4. Iterate: one script per idea, compare in `results/log.csv`.

## Running agents in parallel
Two agents in one working tree will overwrite each other. Give each one a worktree:
```bash
git worktree add ../qrt-features -b features
git worktree add ../qrt-models -b models
```
