# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function._base.builder import FunctionBaseBuilder
from digitalhub_runtime_python.entities.function.openinference.entity import FunctionOpeninference
from digitalhub_runtime_python.entities.function.openinference.spec import (
    FunctionSpecOpeninference,
    FunctionValidatorOpeninference,
)
from digitalhub_runtime_python.entities.function.openinference.status import FunctionStatusOpeninference


class FunctionOpeninferenceBuilder(FunctionBaseBuilder, RuntimeEntityBuilderOpeninference):
    """
    FunctionOpeninference builder.
    """

    ENTITY_CLASS = FunctionOpeninference
    ENTITY_SPEC_CLASS = FunctionSpecOpeninference
    ENTITY_SPEC_VALIDATOR = FunctionValidatorOpeninference
    ENTITY_STATUS_CLASS = FunctionStatusOpeninference
    ENTITY_KIND = EntityKinds.FUNCTION_OPENINFERENCE.value
