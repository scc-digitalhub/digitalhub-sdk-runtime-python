# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import Field

from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec
from digitalhub_runtime_python.entities.function.openinference.models import TensorValidator


class FunctionSpecOpeninference(FunctionBaseSpec):
    """
    FunctionSpecOpeninference specifications.
    """

    model_name: str | None = None
    "Model name to be used for the function execution"

    inputs: list[TensorValidator] = Field(default_factory=list)
    "Function inputs."

    outputs: list[TensorValidator] = Field(default_factory=list)
    "Function outputs."
