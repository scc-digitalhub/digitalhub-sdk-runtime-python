# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.spec import RunSpec

from digitalhub_runtime_python.entities.function._base.models import PythonVersion
from digitalhub_runtime_python.entities.function.guardrail.models import ProcessingMode
from digitalhub_runtime_python.entities.function.openinference.models import TensorValidator


class RunSpecBaseRun(RunSpec):
    """RunSpecBaseRun specifications."""

    source: dict | None = None
    image: str | None = None
    base_image: str | None = None
    python_version: PythonVersion | None = None
    requirements: list[str] | str | None = None

    init_parameters: dict | None = None
    """Init function parameters."""


class RunSpecPython(RunSpecBaseRun):
    """Shared Python run specification."""

    inputs: dict | None = None
    parameters: dict | None = None


class RunSpecGuardrail(RunSpecBaseRun):
    """Shared guardrail run specification."""

    processing_mode: ProcessingMode | None = None


class RunSpecOpeninference(RunSpecBaseRun):
    """Shared OpenInference run specification."""

    model_name: str | None = None
    inputs: list[TensorValidator] | None = None
    outputs: list[TensorValidator] | None = None
