# SPDX-FileCopyrightText: 2024 Stephan Lukasczyk <stephan@pynguin.eu>
#
# SPDX-License-Identifier: EUPL-1.2
"""Contains tests for the `se2dataanalysis.tools` module."""

from __future__ import annotations

import hypothesis
import polars as pl

from hypothesis import strategies as st

from se2dataanalysis import tools


@hypothesis.given(
    st.floats(allow_nan=False),
    st.integers(min_value=1, max_value=2**20),
)
def test_relative_coverage_min_equals_max(coverage: float, count: int):
    """Checks for the relative coverage if min and max coverage are equal."""
    name = "foo"
    data = pl.DataFrame({"TargetModule": count * [name], "Coverage": count * [coverage]})
    expected = 1.0
    actual = tools.relative_coverage(coverage, name, data)
    assert actual == expected


def test_tex_macros_from_dicts():
    """Checks for the TeX macro extraction."""
    dict_1 = {"foo": "bar", "bar": 42}
    dict_2 = {"baz": 1.234}
    expected = "\\newcommand{\\foo}{bar}\n\\newcommand{\\bar}{42}\n\\newcommand{\\baz}{1.234}"
    actual = tools.tex_macros_from_dicts(dict_1, dict_2)
    assert actual == expected
