"""
relationship_analysis.py

Module
------
Relationship Analysis

Purpose
-------
Analyze relationships across multiple tables by validating
referential integrity, relationship cardinality, and
feature-level associations.

Architecture
------------
RelationshipAnalyzer

├── inspect()
│
├── _analyze_relationships()
├── _analyze_cardinality()
├── _analyze_referential_integrity()
├── _analyze_numeric_correlations()
├── _analyze_categorical_associations()
├── _generate_findings()
└── _summary()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd


class RelationshipAnalyzer:

    def __init__(
        self,
        tables: Dict[str, pd.DataFrame],
        relationships: List[dict]
    ):

        self.tables = tables
        self.relationships = relationships

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def inspect(self):

        relationships = self._analyze_relationships()

        correlations = self._numeric_correlations()

        associations = self._categorical_associations()

        return {

            "relationships": relationships,

            "numeric_correlations": correlations,

            "categorical_associations": associations,

            "summary": self._summary(
                relationships
            )
        }

    # -------------------------------------------------
    # Relationship Analysis
    # -------------------------------------------------

    def _analyze_relationships(self):

        rows = []

        for rel in self.relationships:

            parent = self.tables[
                rel["parent_table"]
            ]

            child = self.tables[
                rel["child_table"]
            ]

            parent_key = rel["parent_key"]
            child_key = rel["child_key"]

            parent_values = set(
                parent[parent_key]
            )

            child_values = set(
                child[child_key]
            )

            orphan_records = len(
                child_values - parent_values
            )

            parent_duplicates = parent[
                parent_key
            ].duplicated().sum()

            child_duplicates = child[
                child_key
            ].duplicated().sum()

            if parent_duplicates == 0:

                if child_duplicates == 0:
                    cardinality = "One-to-One"

                else:
                    cardinality = "One-to-Many"

            else:
                cardinality = "Many-to-Many"

            rows.append({

                "parent_table":
                    rel["parent_table"],

                "child_table":
                    rel["child_table"],

                "parent_key":
                    parent_key,

                "child_key":
                    child_key,

                "cardinality":
                    cardinality,

                "orphan_records":
                    orphan_records,

                "referential_integrity":
                    orphan_records == 0
            })

        return pd.DataFrame(rows)

    # -------------------------------------------------
    # Numeric Correlation
    # -------------------------------------------------

    def _numeric_correlations(self):

        results = {}

        for table_name, df in self.tables.items():

            numeric = df.select_dtypes(
                include="number"
            )

            if numeric.shape[1] >= 2:

                results[table_name] = (
                    numeric
                    .corr(numeric_only=True)
                )

        return results

    # -------------------------------------------------
    # Categorical Association
    # -------------------------------------------------

    def _categorical_associations(self):

        results = {}

        for table_name, df in self.tables.items():

            categorical = df.select_dtypes(
                include=["object", "category"]
            )

            results[table_name] = {

                column:
                categorical[column]
                .value_counts()
                .head(5)
                .to_dict()

                for column in categorical.columns
            }

        return results

    # -------------------------------------------------
    # Summary
    # -------------------------------------------------

    def _summary(
        self,
        relationships
    ):

        return {

            "relationships":

                len(relationships),

            "valid_relationships":

                int(
                    relationships[
                        "referential_integrity"
                    ].sum()
                ),

            "invalid_relationships":

                int(
                    (
                        ~relationships[
                            "referential_integrity"
                        ]
                    ).sum()
                )
        }