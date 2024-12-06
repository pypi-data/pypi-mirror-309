# SPDX-FileCopyrightText: 2024 Stephan Lukasczyk <stephan@pynguin.eu>
#
# SPDX-License-Identifier: EUPL-1.2
"""Provides functionality for statistics."""

from __future__ import annotations

import bisect
import typing

from scipy import stats

number: typing.TypeAlias = float | int  # noqa: PYI042 (Type alias should be CamelCase)


class EffectSize(typing.NamedTuple):
    """Wraps the result of the Vargha and Delaney effect-size computation.

    See `vd_a12` for details on the effect-size computation.

    Attributes:
        a12: the Vargha and Delaney effect size
        magnitude: the magnitude of the effect size
    """

    a12: float
    magnitude: str


def vd_a12(
    treatment: list[number],
    control: list[number],
    levels: tuple[float, float, float] | None = None,
) -> EffectSize:
    """Computes the Vargha and Delaney effect size statistics.

    The Vargha and Delaney effect size statistics Â_{12} computes the size of an effect between two
    data sets.  Our implementation applies an optimisation to minimise the accuracy errors due to
    the representation of `float` values, cf. the respective `blog post`_ by Marco Torchiano.  This
    implementation is based on a `GitHub Gist`_ by Jackson Pradolima, who transferred Torchiano's R
    code to Python.

    The implementation returns not only the effect-size value but also a string representation of
    its magnitude.  The level borders for the magnitudes (negligible, small, medium, or large) are
    taken from the work of Hess and Kromray.

    The length of both parameter lists shall be equivalent.

    * A. Vargha and H.D. Delaney. *A critique and improvement of the CL common language effect size
      statistics of McGraw and Wong.* Journal of Education and Behavioural Statistics,
      (25)2:101--132, 2000.
    * M.R. Hess and J.D. Kromrey. *Robust Confidence Intervals for Effect Sizes: A Comparative Study
      of Cohen's d and Cliff's Delta Under Non-normality and heterogenoious Variances.* Annual
      meeting of the American Educational Research Association (Vol. 1). Citeseer, 2004.

    Args:
        treatment: a list of numbers
        control: a list of numbers
        levels: the levels to distinguish between negligible, small, medium, or large effect sizes;
                default are the ones from Hess and Kromrey, 2004.

    Returns:
        a pair of the effect-size value and its magnitude, cf. `EffectSize`

    .. _blog post: https://mtorciano.wordpress.com/2014/05/19/effect-size-of-r-precision/
    .. _GitHub Gist: https://gist.github.com/jacksonpradolima/f9b19d65b7f16602c837024d5f8c8a65
    """

    def magnitude(value: float, levels: tuple[float, float, float] | None = None) -> str:
        # Use the effect-size levels from Hess and Kromrey, 2004, as default
        levels = (0.147, 0.33, 0.474) if levels is None else levels
        magnitudes = ["negligible", "small", "medium", "large"]
        scaled_value = (value - 0.5) * 2
        return magnitudes[bisect.bisect_left(levels, abs(scaled_value))]

    if len(treatment) == 0 and len(control) == 0:
        return EffectSize(a12=0.5, magnitude="negligible")
    if len(treatment) == 0:
        # The idea here is that we have no data for `treatment` but we do for `control`; maybe the
        # process generating `treatment` always failed.
        return EffectSize(a12=0.0, magnitude="large")
    if len(control) == 0:
        return EffectSize(a12=1.0, magnitude="large")

    m = len(treatment)
    n = len(control)
    r = stats.rankdata(treatment + control)
    r1 = sum(r[0:m])

    # Compute the measure A = (r1 / m - (m+1)/2)/n (formula 14 in Vargha and Delaney, 2000).  We
    # use an equivalent formula to avoid accuracy errors, see Torchiano's blog post linked in the
    # DocString for a discussion.
    effect_size = (2 * r1 - m * (m + 1)) / (2 * n * m)

    return EffectSize(a12=effect_size, magnitude=magnitude(effect_size, levels=levels))
