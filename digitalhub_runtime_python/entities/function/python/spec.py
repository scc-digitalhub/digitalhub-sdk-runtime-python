# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities.function._base.models import SourceValidator
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec, FunctionBaseValidator


class FunctionSpecPython(FunctionBaseSpec):
    """
    FunctionSpecPython specifications.
    """


class FunctionValidatorPython(FunctionBaseValidator[SourceValidator]):
    """
    FunctionValidatorPython validator.
    """
