"""
Formatter Class

The code is licensed under the MIT license.
"""

from inspect import isfunction, signature
from typing import Callable, Union
from pandas import DataFrame, Series


class Formatter:
    """
    Series Formatter
    """

    func: Union[Callable, None] = None

    def __init__(self, func: Callable, vectorized: bool = True, skip_null=True):
        self.func = func
        self.vectorized = vectorized
        self.skip_null = skip_null

    def format(self, series: Series, df: DataFrame, column: str) -> Series:
        """
        Format all values in a series
        """
        arg_count = len((signature(self.func)).parameters)
        args = [series, df, column]
        if self.vectorized:
            return self.func(*args[0:arg_count])
        raise NotImplementedError("Pulire doesn't support non-vectorized checks, yet.")


def format_df(formatter: Formatter, df: DataFrame, column: str) -> Series:
    """
    Format a DataFrame's column using a formatter
    """
    formatter = formatter() if isfunction(formatter) else formatter
    return formatter.format(df[column], df, column)


def format_series(formatter: Formatter, series: Series) -> Series:
    """
    Format a DataFrame's column using a formatter
    """
    formatter = formatter() if isfunction(formatter) else formatter
    return formatter.format(series, None, None)
