from __future__ import annotations

import pandas as pd

GROUP_COLS = ["store_nbr", "family"]
TARGET = "sales"


def add_baseline_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add baseline lag features for each (store_nbr, family) time series.

    Computes lag_1 and lag_7 on the target column 'sales', grouped by
    store and product family. NaN values generated at the start of each
    series must be dropped before training.

    Args:
        df: DataFrame sorted by (store_nbr, family, date) with a 'sales' column.

    Returns:
        Copy of the DataFrame with lag_1 and lag_7 columns added.
    """
    df = df.copy()
    df["lag_1"] = df.groupby(GROUP_COLS)[TARGET].shift(1)
    df["lag_7"] = df.groupby(GROUP_COLS)[TARGET].shift(7)
    return df


def add_advanced_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add advanced trend, variability, and promotion features.

    All features are computed with shift(1) to prevent data leakage:
    the value at day t only uses information available up to day t-1.

    Features added:
        - rolling_mean_7:  7-day rolling mean of sales
        - rolling_std_7:   7-day rolling standard deviation of sales
        - rolling_mean_14: 14-day rolling mean of sales
        - trend_1_7:       difference between lag_1 and lag_7 (short-term trend)
        - promo_last_7:    number of days on promotion in the last 7 days

    Requires add_baseline_features() to have been called first,
    as trend_1_7 depends on lag_1 and lag_7.

    Args:
        df: DataFrame with lag_1 and lag_7 already present, sorted by
            (store_nbr, family, date).

    Returns:
        Copy of the DataFrame with advanced features added.
    """
    df = df.copy()

    df["rolling_mean_7"] = (
        df.groupby(GROUP_COLS)[TARGET]
        .transform(lambda s: s.shift(1).rolling(7).mean())
    )

    df["rolling_std_7"] = (
        df.groupby(GROUP_COLS)[TARGET]
        .transform(lambda s: s.shift(1).rolling(7).std())
    )

    df["rolling_mean_14"] = (
        df.groupby(GROUP_COLS)[TARGET]
        .transform(lambda s: s.shift(1).rolling(14).mean())
    )

    df["trend_1_7"] = df["lag_1"] - df["lag_7"]

    df["promo_last_7"] = (
        df.groupby(GROUP_COLS)["onpromotion"]
        .transform(lambda s: s.shift(1).rolling(7).sum())
    )

    return df


def encode_family(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Encode the categorical 'family' column into integer codes.

    Categories are derived exclusively from the training set and applied
    to the test set as well, ensuring consistent encoding across splits.
    This prevents misalignment if the test set contains families in a
    different order.

    Args:
        train_df: Training DataFrame with 'family' as a string column.
        test_df:  Test DataFrame with 'family' as a string column.

    Returns:
        A tuple of three elements:
            - train_df: copy with 'family' encoded as integer
            - test_df:  copy with 'family' encoded as integer
            - family_mapping: dict mapping {integer_code: family_name},
              useful for interpreting predictions and feature importance
    """
    train_df = train_df.copy()
    test_df = test_df.copy()

    family_categories = sorted(train_df["family"].unique())

    train_df["family"] = pd.Categorical(
        train_df["family"], categories=family_categories
    )
    test_df["family"] = pd.Categorical(
        test_df["family"], categories=family_categories
    )

    family_mapping = dict(enumerate(family_categories))

    train_df["family"] = train_df["family"].cat.codes
    test_df["family"] = test_df["family"].cat.codes

    return train_df, test_df, family_mapping

def add_targeted_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add targeted promotion and high-sales spike features.

    These features are designed to improve model behavior on the critical
    segments identified during error analysis: promotions, high-sales periods,
    and demand spikes.

    Sales-based rolling features use shift(1) to avoid target leakage.
    """
    df = df.sort_values(["store_nbr", "family", "date"]).copy()

    # Promotion features
    df["is_promo"] = (df["onpromotion"] > 0).astype(int)
    df["promo_intensity"] = df["onpromotion"]

    df["promo_rolling_mean_7"] = (
        df.groupby(GROUP_COLS)["onpromotion"]
        .transform(lambda s: s.shift(1).rolling(7).mean())
    )

    df["promo_rolling_sum_14"] = (
        df.groupby(GROUP_COLS)["onpromotion"]
        .transform(lambda s: s.shift(1).rolling(14).sum())
    )

    # Demand spike / volatility features
    df["rolling_max_7"] = (
        df.groupby(GROUP_COLS)[TARGET]
        .transform(lambda s: s.shift(1).rolling(7).max())
    )

    df["rolling_max_14"] = (
        df.groupby(GROUP_COLS)[TARGET]
        .transform(lambda s: s.shift(1).rolling(14).max())
    )

    df["rolling_std_14"] = (
        df.groupby(GROUP_COLS)[TARGET]
        .transform(lambda s: s.shift(1).rolling(14).std())
    )

    df["sales_spike_ratio_7"] = df["lag_1"] / (df["rolling_mean_7"] + 1)

    return df