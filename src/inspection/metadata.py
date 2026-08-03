"""
metadata.py

Module: Metadata Inspection

Purpose
-------
Provides structural metadata describing a dataset.

Architecture
------------
metadata.py

MetadataInspector
│
├── inspect()
│
├── _dataset_information()
├── _shape_information()
├── _memory_information()
├── _column_information()
├── _schema_information()
└── _sample_records()

Author: Sufiyan Shaikh
Version: 1.0
"""

from __future__ import annotations

import pandas as pd


class MetadataInspector:
    """
    Inspect structural metadata of a pandas DataFrame.
    """

    def __init__(self, dataframe: pd.DataFrame):

        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(
                "Input must be a pandas DataFrame."
            )

        self.df = dataframe

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def inspect(self) -> dict:
        """
        Execute metadata inspection.

        Returns
        -------
        dict
        """

        return {
            "dataset": self._dataset_information(),
            "memory": self._memory_information(),
            "columns": self._column_information(),
            "schema": self._schema_information(),
            "sample": self._sample_records(),
        }

    # --------------------------------------------------
    # Dataset
    # --------------------------------------------------

    def _dataset_information(self):

        rows, cols = self.df.shape

        return {
            "rows": rows,
            "columns": cols,
            "shape": (rows, cols),
        }

    # --------------------------------------------------
    # Memory
    # --------------------------------------------------

    def _memory_information(self):

        memory = self.df.memory_usage(deep=True).sum()

        return {
            "memory_bytes": int(memory),
            "memory_mb": round(memory / 1024**2, 2),
            "average_row_bytes": round(memory / len(self.df), 2)
            if len(self.df)
            else 0,
        }

    # --------------------------------------------------
    # Columns
    # --------------------------------------------------

    def _column_information(self):

        return {
            "column_count": len(self.df.columns),
            "column_names": list(self.df.columns),
        }

    # --------------------------------------------------
    # Schema
    # --------------------------------------------------

    def _schema_information(self):

        schema = []

        for idx, column in enumerate(self.df.columns):

            schema.append(
                {
                    "position": idx,
                    "column": column,
                    "dtype": str(self.df[column].dtype),
                }
            )

        return pd.DataFrame(schema)

    # --------------------------------------------------
    # Samples
    # --------------------------------------------------

    def _sample_records(self):

        return {
            "head": self.df.head(),
            "tail": self.df.tail(),
            "random": self.df.sample(
                min(5, len(self.df)),
                random_state=42,
            ),
        }