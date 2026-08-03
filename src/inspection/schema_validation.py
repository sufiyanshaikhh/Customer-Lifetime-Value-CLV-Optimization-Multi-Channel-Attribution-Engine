"""
schema_validation.py

Module: Schema Validation

Purpose
-------
Validate the structural schema of a pandas DataFrame by
checking column data types, semantic types, datetime
detection, and compatibility with an expected schema.

Architecture
------------
SchemaValidator

├── validate()
│
├── _validate_dtypes()
├── _identify_datetime_columns()
├── _infer_semantic_types()
├── _validate_expected_schema()
└── _schema_summary()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd
from pandas.api.types import (
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
)


class SchemaValidator:
    """
    Validate the schema of a pandas DataFrame.
    """

    def __init__(
        self,
        dataframe: pd.DataFrame,
        expected_schema: Optional[Dict[str, str]] = None,
    ):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        self.df = dataframe
        self.expected_schema = expected_schema or {}

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def validate(self) -> dict:

        return {
            "schema": self._schema_table(),
            "datetime_columns": self._identify_datetime_columns(),
            "expected_schema": self._validate_expected_schema(),
            "summary": self._schema_summary(),
        }

    # --------------------------------------------------
    # Schema table
    # --------------------------------------------------

    def _schema_table(self):

        rows = []

        for column in self.df.columns:

            dtype = str(self.df[column].dtype)

            rows.append(
                {
                    "column": column,
                    "dtype": dtype,
                    "semantic_type": self._infer_semantic_type(column),
                    "matches_expected_dtype": self._matches_expected_dtype(
                        column,
                        dtype,
                    ),
                }
            )

        return pd.DataFrame(rows)

    # --------------------------------------------------
    # Semantic inference
    # --------------------------------------------------

    def _infer_semantic_type(self, column: str) -> str:

        series = self.df[column]

        if is_datetime64_any_dtype(series):
            return "Datetime"

        if is_bool_dtype(series):
            return "Boolean"

        if is_numeric_dtype(series):
            return "Numeric"

        if is_string_dtype(series):
            return "Text"

        if is_object_dtype(series):
            return "Object"

        return "Unknown"

    # --------------------------------------------------
    # Datetime detection
    # --------------------------------------------------

    def _identify_datetime_columns(self):

        detected = []

        for column in self.df.columns:

            if is_datetime64_any_dtype(self.df[column]):
                detected.append(column)

        return detected

    # --------------------------------------------------
    # Expected schema validation
    # --------------------------------------------------

    def _validate_expected_schema(self):

        actual_columns = set(self.df.columns)
        expected_columns = set(self.expected_schema.keys())

        missing_columns = sorted(expected_columns - actual_columns)
        unexpected_columns = sorted(actual_columns - expected_columns)

        mismatched_dtypes = {}

        for column, expected_dtype in self.expected_schema.items():

            if column not in self.df.columns:
                continue

            actual_dtype = str(self.df[column].dtype)

            if actual_dtype != expected_dtype:

                mismatched_dtypes[column] = {
                    "expected": expected_dtype,
                    "actual": actual_dtype,
                }

        return {
            "missing_columns": missing_columns,
            "unexpected_columns": unexpected_columns,
            "dtype_mismatches": mismatched_dtypes,
            "schema_match": (
                len(missing_columns) == 0
                and len(unexpected_columns) == 0
                and len(mismatched_dtypes) == 0
            ),
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _matches_expected_dtype(
        self,
        column: str,
        actual_dtype: str,
    ) -> Optional[bool]:

        if column not in self.expected_schema:
            return None

        return actual_dtype == self.expected_schema[column]

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def _schema_summary(self):

        semantic_counts = (
            self._schema_table()["semantic_type"]
            .value_counts()
            .to_dict()
        )

        return {
            "total_columns": len(self.df.columns),
            "semantic_type_distribution": semantic_counts,
        }