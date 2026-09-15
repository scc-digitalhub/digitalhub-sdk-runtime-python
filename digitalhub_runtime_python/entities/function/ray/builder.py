# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderRay
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function._base.builder import FunctionBaseBuilder
from digitalhub_runtime_python.entities.function.ray.entity import FunctionRay
from digitalhub_runtime_python.entities.function.ray.spec import FunctionSpecRay, FunctionValidatorRay
from digitalhub_runtime_python.entities.function.ray.status import FunctionStatusRay


class FunctionRayBuilder(FunctionBaseBuilder, RuntimeEntityBuilderRay):
    """
    Ray Python function builder.
    """

    ENTITY_CLASS = FunctionRay
    ENTITY_SPEC_CLASS = FunctionSpecRay
    ENTITY_SPEC_VALIDATOR = FunctionValidatorRay
    ENTITY_STATUS_CLASS = FunctionStatusRay
    ENTITY_KIND = EntityKinds.FUNCTION_RAY.value
