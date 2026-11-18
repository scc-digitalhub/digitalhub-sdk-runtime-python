# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function._base.builder import FunctionBaseBuilder
from digitalhub_runtime_python.entities.function._base.spec import FunctionBaseSpec
from digitalhub_runtime_python.entities.function.python.entity import FunctionPython


class FunctionPythonBuilder(FunctionBaseBuilder, RuntimeEntityBuilderPython):
    """
    FunctionPython builder.
    """

    ENTITY_CLASS = FunctionPython
    ENTITY_SPEC_CLASS = FunctionBaseSpec
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.FUNCTION_PYTHON.value
