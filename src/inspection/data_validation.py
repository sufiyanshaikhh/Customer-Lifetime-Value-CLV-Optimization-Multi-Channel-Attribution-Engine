"""
data_validation.py

Module
------
Data Validation

Purpose
-------
Validate structural integrity and configurable business
rules for a pandas DataFrame.

The validator provides generic validation primitives.
Business-specific rules are supplied externally through
configuration.

Architecture
------------
DataValidator

├── validate()
│
├── _validate_primary_keys()
├── _validate_foreign_keys()
├── _validate_column_rules()
├── _validate_business_rules()
├── _collect_findings()
└── _validation_summary()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, Optional

import pandas as pd


class DataValidator:

    def __init__(
        self,
        dataframe: pd.DataFrame,
        primary_keys: Optional[Iterable[str]] = None,
        foreign_keys: Optional[Dict[str, pd.Series]] = None,
        validation_rules: Optional[Dict] = None,
    ):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe
        self.primary_keys = list(primary_keys or [])
        self.foreign_keys = foreign_keys or {}
        self.rules = validation_rules or {}

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def validate(self):

        pk = self._validate_primary_keys()
        fk = self._validate_foreign_keys()
        column = self._validate_column_rules()

        findings = (
            pk["findings"]
            + fk["findings"]
            + column["findings"]
        )

        return {
            "primary_keys": pk,
            "foreign_keys": fk,
            "column_rules": column,
            "summary": self._validation_summary(findings),
            "findings": findings,
        }

    # --------------------------------------------------
    # Primary Key Validation
    # --------------------------------------------------

    def _validate_primary_keys(self):

        findings = []

        if not self.primary_keys:
            return {
                "validated": False,
                "findings": findings,
            }

        duplicated = self.df.duplicated(
            subset=self.primary_keys
        ).sum()

        nulls = self.df[self.primary_keys].isna().sum().sum()

        if duplicated:

            findings.append({
                "severity": "ERROR",
                "category": "Primary Key",
                "message":
                    f"{duplicated} duplicate primary keys detected."
            })

        if nulls:

            findings.append({
                "severity": "ERROR",
                "category": "Primary Key",
                "message":
                    f"{nulls} null primary key values detected."
            })

        return {
            "validated": True,
            "duplicate_keys": int(duplicated),
            "null_keys": int(nulls),
            "findings": findings,
        }

    # --------------------------------------------------
    # Foreign Key Validation
    # --------------------------------------------------

    def _validate_foreign_keys(self):

        findings = []

        invalid = {}

        for column, reference in self.foreign_keys.items():

            if column not in self.df.columns:
                continue

            invalid_rows = (
                ~self.df[column].isin(reference)
            ).sum()

            invalid[column] = int(invalid_rows)

            if invalid_rows:

                findings.append({
                    "severity": "ERROR",
                    "category": "Foreign Key",
                    "message":
                        f"{column}: {invalid_rows} invalid references."
                })

        return {
            "validated": bool(self.foreign_keys),
            "invalid_references": invalid,
            "findings": findings,
        }

    # --------------------------------------------------
    # Column Rules
    # --------------------------------------------------

    def _validate_column_rules(self):

        findings = []

        for column, rule in self.rules.items():

            if column not in self.df.columns:
                continue

            series = self.df[column]

            # Nullable

            if rule.get("nullable") is False:

                count = series.isna().sum()

                if count:

                    findings.append({
                        "severity": "ERROR",
                        "category": column,
                        "message":
                            f"{count} null values."
                    })

            # Minimum

            if "min" in rule:

                invalid = (series < rule["min"]).sum()

                if invalid:

                    findings.append({
                        "severity": "ERROR",
                        "category": column,
                        "message":
                            f"{invalid} values below minimum."
                    })

            # Maximum

            if "max" in rule:

                invalid = (series > rule["max"]).sum()

                if invalid:

                    findings.append({
                        "severity": "ERROR",
                        "category": column,
                        "message":
                            f"{invalid} values above maximum."
                    })

            # Allowed Values

            if "allowed_values" in rule:

                invalid = (
                    ~series.isin(
                        rule["allowed_values"]
                    )
                ).sum()

                if invalid:

                    findings.append({
                        "severity": "ERROR",
                        "category": column,
                        "message":
                            f"{invalid} invalid categorical values."
                    })

            # Regex

            if "regex" in rule:

                invalid = (
                    ~series
                    .astype(str)
                    .str.match(
                        re.compile(rule["regex"])
                    )
                ).sum()

                if invalid:

                    findings.append({
                        "severity": "ERROR",
                        "category": column,
                        "message":
                            f"{invalid} regex violations."
                    })

        return {
            "validated": bool(self.rules),
            "findings": findings,
        }

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def _validation_summary(self, findings):

        return {

            "total_findings":
                len(findings),

            "errors":
                sum(
                    f["severity"] == "ERROR"
                    for f in findings
                ),

            "warnings":
                sum(
                    f["severity"] == "WARNING"
                    for f in findings
                ),

            "validation_passed":
                len(findings) == 0
        }