"""Single place to describe the problem. Edit this when the brief drops."""

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SUBMISSIONS = ROOT / "submissions"
RESULTS = ROOT / "results"


@dataclass
class Config:
    # Files inside data/. If the target ships in its own file, set y_train_file.
    train_file: str = "X_train.csv"
    y_train_file: str | None = "y_train.csv"
    test_file: str = "X_test.csv"

    id_col: str = "ID"
    target_col: str = "target"
    # Column that orders/groups rows in time (date, day index, timestamp).
    # Rows sharing a value never get split across train/val. None = plain KFold.
    time_col: str | None = "date"

    task: str = "classification"  # "classification" or "regression"
    metric: str = "accuracy"  # key in qrt.metrics.METRICS
    n_splits: int = 5
    # Number of time groups dropped between train and val to stop leakage
    # from overlapping return windows. 0 if rows are independent.
    gap: int = 0

    drop_cols: list[str] = field(default_factory=list)


CFG = Config()
