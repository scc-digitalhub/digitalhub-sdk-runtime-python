# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator
from pydantic import Field

from digitalhub_runtime_python.entities.function.openinference.models import TensorValidator
from digitalhub_runtime_python.entities.function.python.models import PythonVersion, SourceValidator


class FunctionSpecOpeninference(FunctionSpec):
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
        super().__init__()

        self.image = image
        self.base_image = base_image
        self.python_version = python_version
        self.requirements = requirements
        self.source = source
        self.model_name = model_name
        self.inputs = inputs
        self.outputs = outputs


class FunctionValidatorOpeninference(FunctionValidator):
    """
    FunctionValidatorOpeninference validator.
    """

    source: SourceValidator
    """Source code validator"""

    python_version: PythonVersion
    "Python version"

    image: str | None = None
    "Image where the function will be executed"

    base_image: str | None = None
    "Base image used to build the image where the function will be executed"

    requirements: list[str] | None = None
    "Requirements list to be installed in the image where the function will be executed"

    model_name: str | None = None
    "Model name to be used for the function execution"

    inputs: list[TensorValidator] = Field(default_factory=list)
    "Function inputs."

    outputs: list[TensorValidator] = Field(default_factory=list)
    "Function outputs."
