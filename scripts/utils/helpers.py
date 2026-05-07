"""
scripts/utils/helpers.py
Shared helper functions used across teaching and research modules.
University of Liverpool | Computational Marketing Repository
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ── Reproducibility ──────────────────────────────────────────────────────────

def set_seed(seed: int = 42) -> None:
    """
    Fix all random seeds for reproducibility.

    Parameters:
        seed (int): Seed value. Default 42.
    """
    import random
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except ImportError:
        pass


# ── Plotting defaults ─────────────────────────────────────────────────────────

def set_plot_style() -> None:
    """
    Apply standard UoL Computational Marketing plot theme.
    Call once at the top of each notebook or script.
    """
    sns.set_theme(style="whitegrid", palette="colorblind")
    plt.rcParams.update({
        "figure.dpi": 150,
        "font.size": 12,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "figure.figsize": (9, 5),
    })


def save_figure(fig, name: str, subdir: str = "outputs/figures") -> Path:
    """
    Save a matplotlib figure to the standard outputs directory.

    Parameters:
        fig: matplotlib Figure object.
        name (str): Filename without extension (e.g. 'churn_roc_curve').
        subdir (str): Output subdirectory relative to repo root.

    Returns:
        Path: Full path to saved file.
    """
    out = Path(subdir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    fig.savefig(path, bbox_inches="tight")
    print(f"Saved: {path}")
    return path


# ── Data utilities ────────────────────────────────────────────────────────────

def load_raw(path: str) -> pd.DataFrame:
    """
    Load a raw dataset and print a brief inventory.

    Parameters:
        path (str): Path to CSV file.

    Returns:
        pd.DataFrame: Loaded dataframe.

    Notes:
        Raw data must never be modified. Use this function for loading only.
        Save transformed versions to /data/processed/.
    """
    df = pd.read_csv(path)
    print(f"Loaded: {path}")
    print(f"Shape:  {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Nulls:  {df.isnull().sum().sum():,} total missing values")
    return df


def describe_target(df: pd.DataFrame, col: str) -> None:
    """
    Print class distribution for a binary target variable.

    Parameters:
        df (pd.DataFrame): Dataframe containing the target.
        col (str): Target column name.

    Notes:
        Useful for surfacing class imbalance before modelling.
        Always check this before choosing evaluation metrics.
    """
    counts = df[col].value_counts()
    pct = df[col].value_counts(normalize=True) * 100
    summary = pd.DataFrame({"count": counts, "pct": pct.round(1)})
    print(f"\nTarget distribution — '{col}'")
    print(summary.to_string())


# ── Model evaluation ──────────────────────────────────────────────────────────

def evaluate_classifier(model, X_test, y_test, threshold: float = 0.5) -> dict:
    """
    Evaluate a binary classifier with marketing-relevant metrics.

    Parameters:
        model: Fitted sklearn-compatible classifier.
        X_test (pd.DataFrame): Test features.
        y_test (pd.Series): True binary labels.
        threshold (float): Decision threshold. Default 0.5.

    Returns:
        dict: AUC, precision, recall, F1, and lift at threshold.

    Notes:
        Lift = precision / base_rate. Directly relevant for campaign
        targeting: a lift of 2.0 means the model targets customers
        twice as likely to convert as a random selection.
    """
    from sklearn.metrics import (
        roc_auc_score, precision_score, recall_score, f1_score
    )

    proba = model.predict_proba(X_test)[:, 1]
    preds = (proba >= threshold).astype(int)
    base_rate = y_test.mean()

    precision = precision_score(y_test, preds, zero_division=0)
    lift = precision / base_rate if base_rate > 0 else float("nan")

    metrics = {
        "auc":       round(roc_auc_score(y_test, proba), 4),
        "precision": round(precision, 4),
        "recall":    round(recall_score(y_test, preds, zero_division=0), 4),
        "f1":        round(f1_score(y_test, preds, zero_division=0), 4),
        "lift":      round(lift, 4),
        "base_rate": round(base_rate, 4),
    }

    print("\nModel Evaluation")
    print("-" * 30)
    for k, v in metrics.items():
        print(f"  {k:<12} {v}")
    print(f"\n  Interpretation: At threshold={threshold}, the model identifies")
    print(f"  customers {lift:.1f}x more likely to convert than random selection.")

    return metrics
