"""
descriptive_statistics.py

Module
------
Descriptive Statistics

Purpose
-------
Generate descriptive statistics for numeric and categorical
features in a pandas DataFrame.

Architecture
------------
DescriptiveStatistics

├── profile()
│
├── _numeric_statistics()
├── _categorical_statistics()
├── _numeric_summary()
├── _categorical_summary()
└── _dataset_summary()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class DescriptiveStatistics:

    def __init__(self, dataframe: pd.DataFrame):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def profile(self):

        return {
            "numeric": self._numeric_statistics(),
            "categorical": self._categorical_statistics(),
            "summary": self._dataset_summary(),
        }

    # -------------------------------------------------
    # Numeric Statistics
    # -------------------------------------------------

    def _numeric_statistics(self):

        numeric = self.df.select_dtypes(
            include=["number"]
        )

        rows = []

        for column in numeric.columns:

            s = numeric[column]

            q1 = s.quantile(0.25)
            q2 = s.quantile(0.50)
            q3 = s.quantile(0.75)

            std = s.std()

            rows.append({

                "column": column,

                "dtype": str(s.dtype),

                "count": int(s.count()),

                "missing": int(s.isna().sum()),

                "unique": int(s.nunique()),

                "mean": s.mean(),

                "median": s.median(),

                "mode":
                    s.mode().iloc[0]
                    if not s.mode().empty
                    else np.nan,

                "minimum": s.min(),

                "maximum": s.max(),

                "range": s.max() - s.min(),

                "variance": s.var(),

                "std_dev": std,

                "coefficient_variation":
                    std / s.mean()
                    if s.mean() not in [0, np.nan]
                    else np.nan,

                "q1": q1,

                "q2": q2,

                "q3": q3,

                "iqr": q3 - q1,

                "skewness": s.skew(),

                "kurtosis": s.kurt(),
            })

        return pd.DataFrame(rows)

    # -------------------------------------------------
    # Categorical Statistics
    # -------------------------------------------------

    def _categorical_statistics(self):

        categorical = self.df.select_dtypes(
            include=["object", "string", "category", "bool"]
        )

        rows = []

        total_rows = len(self.df)

        for column in categorical.columns:

            s = categorical[column]

            mode = s.mode()

            top = (
                s.value_counts(dropna=False)
                .head(5)
                .to_dict()
            )

            rows.append({

                "column": column,

                "dtype": str(s.dtype),

                "count": int(s.count()),

                "missing": int(s.isna().sum()),

                "unique": int(s.nunique(dropna=True)),

                "cardinality":
                    round(
                        s.nunique(dropna=True)
                        / total_rows,
                        4
                    ) if total_rows else 0,

                "most_frequent":
                    mode.iloc[0]
                    if not mode.empty
                    else np.nan,

                "frequency":
                    int(
                        s.value_counts(dropna=False)
                        .iloc[0]
                    )
                    if not s.empty
                    else 0,

                "top_categories": top
            })

        return pd.DataFrame(rows)

    # -------------------------------------------------
    # Dataset Summary
    # -------------------------------------------------

    def _dataset_summary(self):

        numeric = self.df.select_dtypes(
            include=["number"]
        ).shape[1]

        categorical = self.df.select_dtypes(
            include=["object", "string", "category"]
        ).shape[1]

        boolean = self.df.select_dtypes(
            include=["bool"]
        ).shape[1]

        return {

            "total_columns": self.df.shape[1],

            "numeric_columns": numeric,

            "categorical_columns": categorical,

            "boolean_columns": boolean,
        }