# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum
from typing import ClassVar

from digitalhub.entities._mixin.source.models import HandlerSourceCode
from pydantic import Field


class PythonVersion(Enum):
    """
    Python version supported.
    """

    PYTHON3_10 = "PYTHON3_10"
    PYTHON3_11 = "PYTHON3_11"
    PYTHON3_12 = "PYTHON3_12"
    PYTHON3_13 = "PYTHON3_13"
    PYTHON3_14 = "PYTHON3_14"


class Lang(Enum):
    """
    Source code language.
    """

    PYTHON = "python"


class PythonSourceCode(HandlerSourceCode):
    """Source code model for Python functions."""

    DEFAULT_LANG: ClassVar[str | None] = "python"
    REQUIRE_HANDLER: ClassVar[bool] = True
    lang: Lang = Field(default=Lang.PYTHON.value)
    init_function: str | None = None


SourceValidator = PythonSourceCode
