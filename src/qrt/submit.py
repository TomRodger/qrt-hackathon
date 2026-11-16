from datetime import datetime
from pathlib import Path

import pandas as pd

from qrt.config import CFG, SUBMISSIONS, Config


def write_submission(ids, preds, name: str, cfg: Config = CFG) -> Path:
    """Write submissions/<name>_<time>.csv in ID,target format.
    Check the sample submission once the brief drops and adjust columns here."""
    SUBMISSIONS.mkdir(exist_ok=True)
    path = SUBMISSIONS / f"{name}_{datetime.now():%H%M%S}.csv"
    sub = pd.DataFrame({cfg.id_col: ids, cfg.target_col: preds})
    assert sub[cfg.target_col].notna().all(), "NaN in submission"
    sub.to_csv(path, index=False)
    print(f"wrote {path.relative_to(SUBMISSIONS.parent)} ({len(sub)} rows)")
    return path
