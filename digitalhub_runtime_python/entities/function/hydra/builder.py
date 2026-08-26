# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderHydra
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function._base.builder import FunctionBaseBuilder
from digitalhub_runtime_python.entities.function.hydra.entity import FunctionHydra
from digitalhub_runtime_python.entities.function.hydra.spec import FunctionSpecHydra, FunctionValidatorHydra
from digitalhub_runtime_python.entities.function.hydra.status import FunctionStatusHydra
from digitalhub_runtime_python.entities.function.hydra.utils import config_check, source_check


class FunctionHydraBuilder(FunctionBaseBuilder, RuntimeEntityBuilderHydra):
    """
    FunctionHydra builder.
    """

    ENTITY_CLASS = FunctionHydra
    ENTITY_SPEC_CLASS = FunctionSpecHydra
    ENTITY_SPEC_VALIDATOR = FunctionValidatorHydra
    ENTITY_STATUS_CLASS = FunctionStatusHydra
    ENTITY_KIND = EntityKinds.FUNCTION_HYDRA.value

    def _prepare_kwargs(self, kwargs: dict) -> dict:
        return config_check(**source_check(**kwargs))

    def _prepare_source(self, source: dict) -> dict:
        return source_check(source=source)["source"]
