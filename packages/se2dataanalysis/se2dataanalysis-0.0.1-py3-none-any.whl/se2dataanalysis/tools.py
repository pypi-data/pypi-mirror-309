# SPDX-FileCopyrightText: 2024 Stephan Lukasczyk <stephan@pynguin.eu>
#
# SPDX-License-Identifier: EUPL-1.2
"""Provides tools to manipulate, for example, data frames."""

from __future__ import annotations

import typing

import polars as pl

if typing.TYPE_CHECKING:
    from typing import Any


def relative_coverage(
    b: float,
    c: str,
    data: pl.DataFrame,
    *,
    coverage_column: str = "Coverage",
    module_column: str = "TargetModule",
) -> float:
    """Computes the relative coverage.

    The following description is taken from the original description of the relative coverage matric
    in Arcuri & Fraser, 2013:

    Given *b* the number of covered branches in a run for a class *c*, we used the following
    normalization to define a relative coverage *r*:
    r(b, c) = frac{b - min_c}{max_c - min_c} where min_c is the worst coverage obtained in *all* the
    (...) experiments for that class *c*, and max_c is the maximum obtained value.
    If min_c = max_c, then r = 1.

    Expects that `c` is a value in the `module_column` column of `data` and that the
    `coverage_column` column in `data` contains the respective coverage values.

    * A. Arcuri and G. Fraser. *Parameter tuning or default values? An empirical investigation in
      search-based software engineering.* Empirical Software Engineering, 18:594--623, 2013.

    Args:
        b: the number of covered branches in a run for a subject module `c`
        c: the name of the subject module
        data: the `DataFrame` containing the coverage data
        coverage_column: the column name in `data` containing the coverage values
        module_column: the column name in `data` containing the subject names

    Returns:
        the relative coverage for that subject module
    """
    base_query = (
        data.lazy()
        .filter(pl.col(module_column) == c)
        .select(coverage_column)
        .collect()
        .get_column(coverage_column)
    )
    max_c = base_query.max()
    min_c = base_query.min()
    if max_c == min_c:
        return 1.0
    return (b - min_c) / (max_c - min_c)


def tex_macros_from_dicts(*dicts: dict[str, Any]) -> str:
    """Extracts TeX macros from one or many dictionaries.

    The keys of the dictionaries will become the macro names.

    Args:
        *dicts: the dictionaries to process

    Returns:
        a string defining the TeX macros, one macro per line
    """
    return "\n".join([f"\\newcommand{{\\{k}}}{{{v}}}" for entry in dicts for k, v in entry.items()])
