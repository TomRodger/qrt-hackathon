"""Validation splits. Random KFold on time-series data leaks the future and
inflates scores, so anything with a time column gets a walk-forward split."""

from collections.abc import Iterator

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold

from qrt.config import CFG, Config

Split = tuple[np.ndarray, np.ndarray]


def walk_forward(times: pd.Series, n_splits: int, gap: int = 0) -> Iterator[Split]:
    """Expanding-window split over sorted unique time values.

    Unique times are cut into n_splits + 1 blocks. Fold k trains on blocks
    0..k (minus `gap` trailing time values) and validates on block k + 1.
    """
    uniq = np.sort(times.unique())
    blocks = np.array_split(uniq, n_splits + 1)
    t = times.to_numpy()
    for k in range(n_splits):
        val_times = blocks[k + 1]
        train_times = np.concatenate(blocks[: k + 1])
        if gap:
            train_times = train_times[:-gap]
        yield np.where(np.isin(t, train_times))[0], np.where(np.isin(t, val_times))[0]


def make_splits(df: pd.DataFrame, cfg: Config = CFG) -> list[Split]:
    if cfg.time_col:
        return list(walk_forward(df[cfg.time_col], cfg.n_splits, cfg.gap))
    if cfg.task == "classification":
        kf = StratifiedKFold(cfg.n_splits, shuffle=True, random_state=0)
        return list(kf.split(df, df[cfg.target_col]))
    return list(KFold(cfg.n_splits, shuffle=True, random_state=0).split(df))
