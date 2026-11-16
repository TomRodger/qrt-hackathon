"""Generate QRT-style synthetic data in data/ so the pipeline can be dry-run
before the real data exists. Delete once real data is in place.

Shape: one row per (date, stock), lagged-return features, binary target =
sign of the next return. A weak signal is planted in RET_1 so a working
model should land a little above 50% accuracy, not at 100%.
"""

import numpy as np
import pandas as pd

from qrt.config import DATA

rng = np.random.default_rng(0)
n_dates, n_stocks, n_test_dates = 200, 50, 40


def make(dates: range, start_id: int) -> pd.DataFrame:
    rows = len(dates) * n_stocks
    df = pd.DataFrame(
        {
            "ID": np.arange(start_id, start_id + rows),
            "date": np.repeat(list(dates), n_stocks),
            "stock": np.tile(np.arange(n_stocks), len(dates)),
        }
    )
    for k in range(1, 6):
        df[f"RET_{k}"] = rng.normal(0, 0.02, rows)
        df[f"VOLUME_{k}"] = rng.lognormal(0, 0.5, rows)
    next_ret = -0.15 * df["RET_1"] + rng.normal(0, 0.02, rows)
    df["target"] = (next_ret > 0).astype(int)
    return df


DATA.mkdir(exist_ok=True)
train = make(range(n_dates), 0)
test = make(range(n_dates, n_dates + n_test_dates), len(train))
train.drop(columns="target").to_csv(DATA / "X_train.csv", index=False)
train[["ID", "target"]].to_csv(DATA / "y_train.csv", index=False)
test.drop(columns="target").to_csv(DATA / "X_test.csv", index=False)
print(f"train {train.shape}, test {test.shape} -> {DATA}")
