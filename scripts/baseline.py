"""First-hour baseline: trivial model + LightGBM under the same CV, then a
submission from LightGBM fit on all training data.

    uv run python scripts/baseline.py
"""

from lightgbm import LGBMClassifier, LGBMRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor

from qrt.config import CFG
from qrt.cv import make_splits
from qrt.data import feature_cols, load_test, load_train
from qrt.experiment import run_cv
from qrt.submit import write_submission

train, test = load_train(), load_test()
if CFG.time_col:
    train = train.sort_values(CFG.time_col).reset_index(drop=True)
feats = feature_cols(train)
X, y = train[feats], train[CFG.target_col]
splits = make_splits(train)
print(f"{len(X)} rows, {len(feats)} features, {len(splits)} folds")

clf = CFG.task == "classification"
Dummy = DummyClassifier if clf else DummyRegressor
LGBM = LGBMClassifier if clf else LGBMRegressor
params = dict(
    n_estimators=300,
    learning_rate=0.03,
    num_leaves=15,
    subsample=0.8,
    subsample_freq=1,
    colsample_bytree=0.8,
    verbose=-1,
    random_state=0,
)

run_cv("dummy", lambda: Dummy(), X, y, splits, notes="floor to beat")
run_cv("lgbm_baseline", lambda: LGBM(**params), X, y, splits, notes=str(params))

model = LGBM(**params).fit(X, y)
write_submission(test[CFG.id_col], model.predict(test[feats]), "lgbm_baseline")
