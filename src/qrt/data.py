from pathlib import Path

import pandas as pd

from qrt.config import CFG, DATA, Config


def _read(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def load_train(cfg: Config = CFG) -> pd.DataFrame:
    df = _read(DATA / cfg.train_file)
    if cfg.y_train_file:
        y = _read(DATA / cfg.y_train_file)
        df = df.merge(y, on=cfg.id_col, how="inner", validate="one_to_one")
    return df


def load_test(cfg: Config = CFG) -> pd.DataFrame:
    return _read(DATA / cfg.test_file)


def feature_cols(df: pd.DataFrame, cfg: Config = CFG) -> list[str]:
    exclude = {cfg.id_col, cfg.target_col, cfg.time_col, *cfg.drop_cols}
    return [c for c in df.columns if c not in exclude]
