# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Generic, TypeVar

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator
from pydantic import BaseModel

from digitalhub_runtime_python.entities.function._base.models import PythonVersion

_SourceValidatorT = TypeVar("_SourceValidatorT", bound=BaseModel)


class FunctionBaseSpec(FunctionSpec):
    """Base specification for runtime Python functions."""

    def __init__(
        self,
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        python_version: str | None = None,
        requirements: list | None = None,
    ) -> None:
        super().__init__()

        self.image = image
        self.base_image = base_image
        self.python_version = python_version
        self.requirements = requirements
        self.source = source


class FunctionBaseValidator(FunctionValidator, Generic[_SourceValidatorT]):
    """Base validator for runtime Python functions."""

    source: _SourceValidatorT
    """Source code validator."""

    python_version: PythonVersion | None = None
    """Python version."""

    image: str | None = None
    """Image where the function will be executed."""

    base_image: str | None = None
    """Base image used to build the function image."""

    requirements: list[str] | str | None = None
    """Requirements installed in the function image."""
