"""Run CV for any sklearn-style model and log the result so every experiment
is comparable. results/log.csv is committed: it's the team's scoreboard."""

import subprocess
from collections.abc import Callable
from datetime import datetime

import numpy as np
import pandas as pd

from qrt.config import CFG, RESULTS, Config
from qrt.metrics import METRICS


def _commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "none"


def run_cv(
    name: str,
    make_model: Callable[[], object],
    X: pd.DataFrame,
    y: pd.Series,
    splits: list,
    cfg: Config = CFG,
    notes: str = "",
) -> tuple[np.ndarray, list[float]]:
    """Fit a fresh model per fold. Returns out-of-fold predictions and fold scores."""
    metric = METRICS[cfg.metric]
    oof = np.full(len(X), np.nan)
    scores = []
    for i, (tr, va) in enumerate(splits):
        model = make_model()
        model.fit(X.iloc[tr], y.iloc[tr])
        pred = model.predict(X.iloc[va])
        oof[va] = pred
        scores.append(metric(y.iloc[va], pred))
        print(f"  fold {i}: {scores[-1]:.5f}  (train {len(tr)}, val {len(va)})")
    mean, std = float(np.mean(scores)), float(np.std(scores))
    print(f"{name}: {cfg.metric} = {mean:.5f} ± {std:.5f}")
    log(name, mean, std, cfg, notes)
    return oof, scores


def log(name: str, mean: float, std: float, cfg: Config = CFG, notes: str = "") -> None:
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / "log.csv"
    row = pd.DataFrame(
        [
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "name": name,
                "metric": cfg.metric,
                "mean": round(mean, 6),
                "std": round(std, 6),
                "commit": _commit(),
                "notes": notes,
            }
        ]
    )
    row.to_csv(path, mode="a", header=not path.exists(), index=False)
