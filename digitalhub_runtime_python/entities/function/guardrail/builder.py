# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderGuardrail
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function._base.builder import FunctionBaseBuilder
from digitalhub_runtime_python.entities.function.guardrail.entity import FunctionGuardrail
from digitalhub_runtime_python.entities.function.guardrail.spec import (
    FunctionSpecGuardrail,
)


class FunctionGuardrailBuilder(FunctionBaseBuilder, RuntimeEntityBuilderGuardrail):
    """
    FunctionGuardrail builder.
    """

    ENTITY_CLASS = FunctionGuardrail
    ENTITY_SPEC_CLASS = FunctionSpecGuardrail
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.FUNCTION_GUARDRAIL.value
