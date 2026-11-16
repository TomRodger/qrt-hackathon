import numpy as np
import pandas as pd

from qrt.cv import walk_forward


def _times():
    return pd.Series(np.repeat(np.arange(30), 4))


def test_no_future_leakage():
    t = _times()
    for tr, va in walk_forward(t, n_splits=4):
        assert t.iloc[tr].max() < t.iloc[va].min()


def test_groups_never_split():
    t = _times()
    for tr, va in walk_forward(t, n_splits=4):
        assert not set(t.iloc[tr]) & set(t.iloc[va])


def test_gap_respected():
    t = _times()
    for tr, va in walk_forward(t, n_splits=4, gap=2):
        assert t.iloc[va].min() - t.iloc[tr].max() > 2
