# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities.function._base.models import SourceValidator
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec, FunctionBaseValidator
from digitalhub_runtime_python.entities.function.guardrail.models import ProcessingMode


class FunctionSpecGuardrail(FunctionBaseSpec):
    """
    FunctionSpecGuardrail specifications.
    """

    def __init__(
        self,
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        python_version: str | None = None,
        requirements: list | None = None,
        processing_mode: str | None = None,
    ) -> None:
        super().__init__(
            source=source,
            image=image,
            base_image=base_image,
            python_version=python_version,
            requirements=requirements,
        )
        self.processing_mode = processing_mode


class FunctionValidatorGuardrail(FunctionBaseValidator[SourceValidator]):
    """
    FunctionValidatorGuardrail validator.
    """

    processing_mode: ProcessingMode
    """Processing mode"""
