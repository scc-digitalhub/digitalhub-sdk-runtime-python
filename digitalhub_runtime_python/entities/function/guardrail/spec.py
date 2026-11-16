# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec
from digitalhub_runtime_python.entities.function.guardrail.models import ProcessingMode


class FunctionSpecGuardrail(FunctionBaseSpec):
    """
    FunctionSpecGuardrail specifications.
    """

    processing_mode: ProcessingMode
    """Processing mode"""
