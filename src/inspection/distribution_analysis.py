"""
distribution_analysis.py

Module
------
Distribution Analysis

Purpose
-------
Analyze the statistical distribution of numeric variables
and identify potential outliers using distribution-based
methods.

Architecture
------------
DistributionAnalyzer

├── inspect()
│
├── _analyze_numeric_distributions()
├── _detect_outliers()
├── _distribution_summary()
└── _overall_summary()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class DistributionAnalyzer:

    def __init__(self, dataframe: pd.DataFrame):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def inspect(self):

        numeric = self.df.select_dtypes(include=["number"])

        return {
            "distribution": self._distribution_analysis(numeric),
            "outliers": self._outlier_analysis(numeric),
            "summary": self._summary(numeric),
        }

    # --------------------------------------------------
    # Distribution Analysis
    # --------------------------------------------------

    def _distribution_analysis(self, numeric):

        rows = []

        for column in numeric.columns:

            s = numeric[column].dropna()

            mean = s.mean()
            median = s.median()

            skewness = s.skew()
            kurtosis = s.kurt()

            rows.append({

                "column": column,

                "mean": mean,

                "median": median,

                "skewness": skewness,

                "kurtosis": kurtosis,

                "distribution_shape":
                    self._distribution_shape(skewness),

                "symmetry":
                    abs(skewness) < 0.5,

                "zero_percentage":
                    round(
                        (s.eq(0).sum() / len(s)) * 100,
                        2
                    ) if len(s) else 0,

                "negative_percentage":
                    round(
                        (s.lt(0).sum() / len(s)) * 100,
                        2
                    ) if len(s) else 0,
            })

        return pd.DataFrame(rows)

    # --------------------------------------------------
    # Outlier Analysis
    # --------------------------------------------------

    def _outlier_analysis(self, numeric):

        rows = []

        for column in numeric.columns:

            s = numeric[column].dropna()

            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)

            mask = (s < lower) | (s > upper)

            rows.append({

                "column": column,

                "lower_bound": lower,

                "upper_bound": upper,

                "outlier_count": int(mask.sum()),

                "outlier_percentage":
                    round(
                        mask.mean() * 100,
                        2
                    )
            })

        return pd.DataFrame(rows)

    # --------------------------------------------------
    # Distribution Shape
    # --------------------------------------------------

    @staticmethod
    def _distribution_shape(skewness):

        if pd.isna(skewness):
            return "Unknown"

        if skewness > 1:
            return "Highly Right Skewed"

        if skewness > 0.5:
            return "Moderately Right Skewed"

        if skewness < -1:
            return "Highly Left Skewed"

        if skewness < -0.5:
            return "Moderately Left Skewed"

        return "Approximately Symmetric"

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def _summary(self, numeric):

        distribution = self._distribution_analysis(numeric)
        outliers = self._outlier_analysis(numeric)

        return {

            "numeric_columns":
                len(numeric.columns),

            "features_with_outliers":
                int(
                    (outliers["outlier_count"] > 0).sum()
                ),

            "highly_skewed_features":
                int(
                    (
                        distribution["skewness"]
                        .abs() > 1
                    ).sum()
                ),

            "approximately_symmetric_features":
                int(
                    distribution["symmetry"].sum()
                )
        }