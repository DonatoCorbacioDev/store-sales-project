from __future__ import annotations

import pandas as pd

def add_error_columns(
    val_data: pd.DataFrame,
    y_pred,
    fold: int | None = None,
) -> pd.DataFrame:
    """
    Add prediction and error columns to a validation DataFrame.
    """
    df = val_data.copy()

    if fold is not None:
        df["fold"] = fold

    df["y_pred"] = y_pred
    df["error"] = df["sales"] - df["y_pred"]
    df["abs_error"] = df["error"].abs()
    df["squared_error"] = df["error"] ** 2

    return df


def add_analysis_labels(
    errors_df: pd.DataFrame,
    family_mapping: dict | None = None,
) -> pd.DataFrame:
    """
    Add readable labels and segment flags used for error analysis.
    """
    df = errors_df.copy()

    if family_mapping is not None:
        df["family_name"] = df["family"].map(family_mapping)

    df["promo_flag"] = (df["onpromotion"] > 0).astype(int)

    if "is_weekend" not in df.columns and "dayofweek" in df.columns:
        df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    return df


def summarize_errors(
    errors_df: pd.DataFrame,
    group_cols=None,
    sort_by: str = "mean_abs_error",
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Summarize prediction errors globally or by one/multiple grouping columns.
    """
    agg_dict = {
        "mean_abs_error": ("abs_error", "mean"),
        "median_abs_error": ("abs_error", "median"),
        "mean_error": ("error", "mean"),
        "max_abs_error": ("abs_error", "max"),
        "count": ("abs_error", "size"),
    }

    if "sales" in errors_df.columns:
        agg_dict["mean_sales"] = ("sales", "mean")

    if group_cols is None:
        return pd.DataFrame([{
            "mean_abs_error": errors_df["abs_error"].mean(),
            "median_abs_error": errors_df["abs_error"].median(),
            "mean_error": errors_df["error"].mean(),
            "max_abs_error": errors_df["abs_error"].max(),
            "n_predictions": len(errors_df),
        }])

    summary = (
        errors_df
        .groupby(group_cols)
        .agg(**agg_dict)
    )

    if sort_by in summary.columns:
        summary = summary.sort_values(sort_by, ascending=ascending)

    return summary


def add_sales_bins(
    errors_df: pd.DataFrame,
    q: int = 4,
    labels=None,
) -> pd.DataFrame:
    """
    Add quantile-based sales volume bins for segment-level error analysis.
    """
    df = errors_df.copy()

    if labels is None:
        labels = ["Low", "Medium-low", "Medium-high", "High"]

    df["sales_bin"] = pd.qcut(
        df["sales"].rank(method="first"),
        q=q,
        labels=labels,
    )

    return df


def get_worst_predictions(
    errors_df: pd.DataFrame,
    n: int = 20,
) -> pd.DataFrame:
    """
    Return the rows with the largest absolute errors.
    """
    return (
        errors_df
        .sort_values("abs_error", ascending=False)
        .head(n)
    )