# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.spec import Spec

from digitalhub_runtime_python.entities.function._base.models import PythonSourceCode, PythonVersion


class FunctionBaseSpec(Spec):
    """Base specification for runtime Python functions."""

    source: PythonSourceCode
    """Source code."""

    python_version: PythonVersion | None = None
    """Python version."""

    image: str | None = None
    """Image where the function will be executed."""

    base_image: str | None = None
    """Base image used to build the function image."""

    requirements: list[str] | str | None = None
    """Requirements installed in the function image."""
