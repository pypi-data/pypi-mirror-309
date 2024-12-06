"""
PULIRE

Validator Class

The code is licensed under the MIT license.
"""

from inspect import isfunction, signature
from typing import Callable, Union
from pandas import DataFrame, Series


class Validator:
    """
    Series Validator
    """

    func: Union[Callable, None] = None
    vectorized: bool = True
    skip_null: bool = False

    def __init__(self, func: Callable, vectorized: bool = True, skip_null=True):
        self.func = func
        self.vectorized = vectorized
        self.skip_null = skip_null

    def validate(
        self, series: Series, df: DataFrame, column: str
    ) -> Union[bool, Series]:
        """
        Run validator

        Returns a bool series:
        True -> Check passed
        False -> Check failed
        """
        arg_count = len((signature(self.func)).parameters)
        args = [series, df, column]
        if self.vectorized:
            return self.func(*args[0:arg_count])
        raise NotImplementedError("Pulire doesn't support non-vectorized checks, yet.")


def validate_df(validator: Validator, df: DataFrame, column: str) -> Series:
    """
    Validate a DataFrame's column using a validator
    """
    validator = validator() if isfunction(validator) else validator
    if validator.skip_null:
        result = Series(data=True, index=df.index, dtype=bool)
        result.update(
            validator.validate(
                df.loc[df[column].notnull()][column],
                df.loc[df[column].notnull()],
                column,
            )
        )
        return result.astype(bool)
    return validator.validate(df[column], df, column)


def validate_series(validator: Validator, series: Series) -> Series:
    """
    Validate a Series using a validator
    """
    validator = validator() if isfunction(validator) else validator
    if validator.skip_null:
        result = Series(data=True, index=series.index, dtype=bool)
        result.update(validator.validate(series.loc[series.notnull()], None, None))
        return result.astype(bool)
    return validator.validate(series, None, None)
