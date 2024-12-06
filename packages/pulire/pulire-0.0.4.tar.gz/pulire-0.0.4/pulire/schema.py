"""
PULIRE

Schema Class

The code is licensed under the MIT license.
"""

from copy import copy
from typing import List
from pandas import DataFrame, Series, to_numeric

from pulire.column import Column
from pulire.validator import validate_df, validate_series
from pulire.formatter import format_df, format_series


class Schema:
    """
    Pulire Schema
    """

    is_series_schema = False
    columns: List[Column]

    def __init__(self, columns: List[Column] | Column):
        self.is_series_schema = isinstance(columns, Column)
        self.columns = [columns] if isinstance(columns, Column) else columns

    @property
    def dtypes(self) -> dict | str:
        """
        Dictionary of the column's data types
        """
        return self.columns[0].dtype if self.is_series_schema else {col.name: col.dtype for col in self.columns}

    def fit(self, data: DataFrame | Series, fill=None) -> DataFrame:
        """
        Remove invalid data from a DataFrame, enforce data types and apply formatters
        """
        temp = copy(data)

        # Rename series
        if self.is_series_schema:
            temp.rename(self.columns[0].name, inplace=True)

        # Enforce data types
        if self.is_series_schema:
            if self.columns[0].dtype == "Int64":
                temp = to_numeric(temp).round(0)
            temp = temp.astype(self.columns[0].dtype, errors="ignore")
        else:
            for col, dtype in self.dtypes.items():
                if col in temp and dtype == "Int64":
                    temp[col] = to_numeric(temp[col]).round(0)
            temp = temp.astype(self.dtypes, errors="ignore")

        # Remove invalid data
        if self.is_series_schema:
            for validator in self.columns[0].validators:
                test = validate_series(validator, temp)
                temp.loc[~test] = fill
        else:
            for col in self.columns:
                if col.name in temp.columns:
                    for validator in col.validators:
                        test = validate_df(validator, temp, col.name)
                        temp.loc[~test, col.name] = fill

        # Apply formatters
        if self.is_series_schema:
            for formatter in self.columns[0].formatters:
                temp = format_series(formatter, temp)
        else:
            for col in self.columns:
                if col.name in temp.columns:
                    for formatter in col.formatters:
                        temp[col.name] = format_df(formatter, temp, col.name)

        return temp

    def validate(self, df: DataFrame) -> None:
        """
        Raise error when checks are failing
        """
        for col in self.columns:
            if col.name in df.columns:
                for validator in col.validators:
                    test = validate_df(validator, df, col.name)
                    if not test.all():
                        raise ValueError(f'Column "{col.name}" contains invalid data')

    def is_valid(self, df: DataFrame) -> bool:
        """
        Check if a DataFrame is valid
        """
        for col in self.columns:
            if col.name in df.columns:
                for validator in col.validators:
                    test = validate_df(validator, df, col.name)
                    if not test.all():
                        return False
        return True
