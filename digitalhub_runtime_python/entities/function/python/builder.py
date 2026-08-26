# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function._base.builder import FunctionBaseBuilder
from digitalhub_runtime_python.entities.function.python.entity import FunctionPython
from digitalhub_runtime_python.entities.function.python.spec import FunctionSpecPython, FunctionValidatorPython
from digitalhub_runtime_python.entities.function.python.status import FunctionStatusPython


class FunctionPythonBuilder(FunctionBaseBuilder, RuntimeEntityBuilderPython):
    """
    FunctionPython builder.
    """

    ENTITY_CLASS = FunctionPython
    ENTITY_SPEC_CLASS = FunctionSpecPython
    ENTITY_SPEC_VALIDATOR = FunctionValidatorPython
    ENTITY_STATUS_CLASS = FunctionStatusPython
    ENTITY_KIND = EntityKinds.FUNCTION_PYTHON.value
