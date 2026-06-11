# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

class Lang(Enum):
    """
    Source code language.
    """

    PYTHON = "python"


class SourceValidator(BaseModel):
    """
    Source code params.
    """

    model_config = ConfigDict(use_enum_values=True)

    source: str = None
    "Pointer to source code."

    handler: str = None
    "Function entrypoint."

    init_function: str = None
    """Handler for init function."""

    complete_function: str = None
    """Handler for complete function."""

    code: str = None
    "Source code (plain text)."

    base64: str = None
    "Source code (base64 encoded)."

    lang: Lang = Field(default=Lang.PYTHON.value)
    "Source code language (hint)."

class ConfigValidator(BaseModel):
    """
    Config params.
    """
    model_config = ConfigDict(use_enum_values=True)

    source: str = None
    "Pointer to source code."

    path: str = None
    "Config path."

    base64: str = None
    "Config (base64 encoded)."