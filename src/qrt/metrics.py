"""Scoring functions. All take (y_true, y_pred) and higher is better.
Add the competition metric here as soon as it's known and set CFG.metric."""

import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import accuracy_score, roc_auc_score


def accuracy(y, p):
    return accuracy_score(y, p)


def weighted_accuracy(y, p):
    """Sign accuracy weighted by |y|. Common in QRT return-prediction challenges."""
    y, p = np.asarray(y), np.asarray(p)
    w = np.abs(y)
    return float(np.sum(w * (np.sign(y) == np.sign(p))) / np.sum(w))


def auc(y, p):
    return roc_auc_score(y, p)


def neg_rmse(y, p):
    return -float(np.sqrt(np.mean((np.asarray(y) - np.asarray(p)) ** 2)))


def spearman_ic(y, p):
    return float(spearmanr(y, p).statistic)


METRICS = {
    "accuracy": accuracy,
    "weighted_accuracy": weighted_accuracy,
    "auc": auc,
    "neg_rmse": neg_rmse,
    "spearman_ic": spearman_ic,
}
