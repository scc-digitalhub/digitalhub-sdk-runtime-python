# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import Field

from digitalhub_runtime_python.entities.function._base.models import SourceValidator
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec, FunctionBaseValidator
from digitalhub_runtime_python.entities.function.openinference.models import TensorValidator


class FunctionSpecOpeninference(FunctionBaseSpec):
    """
    FunctionSpecOpeninference specifications.
    """

    def __init__(
        self,
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        python_version: str | None = None,
        requirements: list | None = None,
        model_name: str | None = None,
        inputs: list | None = None,
        outputs: list | None = None,
    ) -> None:
        super().__init__(
            source=source,
            image=image,
            base_image=base_image,
            python_version=python_version,
            requirements=requirements,
        )
        self.model_name = model_name
        self.inputs = inputs
        self.outputs = outputs


class FunctionValidatorOpeninference(FunctionBaseValidator[SourceValidator]):
    """
    FunctionValidatorOpeninference validator.
    """

    model_name: str | None = None
    "Model name to be used for the function execution"

    inputs: list[TensorValidator] = Field(default_factory=list)
    "Function inputs."

    outputs: list[TensorValidator] = Field(default_factory=list)
    "Function outputs."
