"""
data_quality.py

Module
------
Data Quality Inspection

Purpose
-------
Evaluate the overall quality of a pandas DataFrame by
profiling completeness, duplicates, uniqueness,
blank values and constant columns.

Architecture
------------
DataQualityInspector

├── inspect()
│
├── _missing_value_analysis()
├── _duplicate_analysis()
├── _uniqueness_analysis()
├── _blank_value_analysis()
├── _constant_column_analysis()
├── _completeness_analysis()
├── _quality_score()
└── _quality_summary()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd


class DataQualityInspector:

    def __init__(
        self,
        dataframe: pd.DataFrame,
        primary_keys: Optional[Iterable[str]] = None,
    ):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe
        self.primary_keys = list(primary_keys) if primary_keys else []

    # ---------------------------------------------------
    # Public API
    # ---------------------------------------------------

    def inspect(self):

        return {
            "missing_values": self._missing_value_analysis(),
            "duplicates": self._duplicate_analysis(),
            "uniqueness": self._uniqueness_analysis(),
            "blank_values": self._blank_value_analysis(),
            "constant_columns": self._constant_column_analysis(),
            "completeness": self._completeness_analysis(),
            "quality_score": self._quality_score(),
            "summary": self._quality_summary(),
        }

    # ---------------------------------------------------
    # Missing values
    # ---------------------------------------------------

    def _missing_value_analysis(self):

        missing = self.df.isna().sum()
        percent = (missing / len(self.df) * 100).round(2)

        return pd.DataFrame({
            "missing_count": missing,
            "missing_percent": percent
        })

    # ---------------------------------------------------
    # Duplicate rows
    # ---------------------------------------------------

    def _duplicate_analysis(self):

        duplicate_rows = int(self.df.duplicated().sum())

        results = {
            "duplicate_rows": duplicate_rows,
            "duplicate_percentage":
                round(duplicate_rows / len(self.df) * 100, 2)
                if len(self.df)
                else 0
        }

        if self.primary_keys:

            duplicate_keys = int(
                self.df.duplicated(subset=self.primary_keys).sum()
            )

            results["duplicate_primary_keys"] = duplicate_keys

        return results

    # ---------------------------------------------------
    # Uniqueness
    # ---------------------------------------------------

    def _uniqueness_analysis(self):

        rows = []

        total_rows = len(self.df)

        for column in self.df.columns:

            unique = self.df[column].nunique(dropna=True)

            rows.append({
                "column": column,
                "unique_values": unique,
                "cardinality":
                    round(unique / total_rows, 4)
                    if total_rows
                    else 0,
                "candidate_key":
                    unique == total_rows
            })

        return pd.DataFrame(rows)

    # ---------------------------------------------------
    # Blank strings
    # ---------------------------------------------------

    def _blank_value_analysis(self):

        blanks = {}

        object_columns = self.df.select_dtypes(
            include=["object", "string"]
        )

        for column in object_columns.columns:

            blanks[column] = int(
                object_columns[column]
                .astype(str)
                .str.strip()
                .eq("")
                .sum()
            )

        return blanks

    # ---------------------------------------------------
    # Constant columns
    # ---------------------------------------------------

    def _constant_column_analysis(self):

        constant = []

        for column in self.df.columns:

            if self.df[column].nunique(dropna=False) <= 1:

                constant.append(column)

        return constant

    # ---------------------------------------------------
    # Completeness
    # ---------------------------------------------------

    def _completeness_analysis(self):

        total_cells = self.df.size

        non_missing = self.df.count().sum()

        completeness = (
            non_missing / total_cells * 100
            if total_cells
            else 100
        )

        return {
            "total_cells": total_cells,
            "non_missing_cells": int(non_missing),
            "dataset_completeness":
                round(completeness, 2)
        }

    # ---------------------------------------------------
    # Quality score
    # ---------------------------------------------------

    def _quality_score(self):

        completeness = self._completeness_analysis()[
            "dataset_completeness"
        ]

        duplicate_penalty = self._duplicate_analysis()[
            "duplicate_percentage"
        ]

        score = max(
            0,
            round(completeness - duplicate_penalty, 2)
        )

        return score

    # ---------------------------------------------------
    # Summary
    # ---------------------------------------------------

    def _quality_summary(self):

        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "constant_columns":
                len(self._constant_column_analysis()),
            "quality_score":
                self._quality_score()
        }