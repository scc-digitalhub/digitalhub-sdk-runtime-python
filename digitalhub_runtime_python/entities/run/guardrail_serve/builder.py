# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderGuardrail
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run._base.status import RunStatusBaseRun
from digitalhub_runtime_python.entities.run.guardrail_serve.entity import RunGuardrailRunServe
from digitalhub_runtime_python.entities.run.guardrail_serve.spec import (
    RunSpecGuardrailRunServe,
)


class RunGuardrailRunServeBuilder(RunBuilder, RuntimeEntityBuilderGuardrail):
    """
    RunGuardrailRunServeBuilder runner.
    """

    ENTITY_CLASS = RunGuardrailRunServe
    ENTITY_SPEC_CLASS = RunSpecGuardrailRunServe
    ENTITY_STATUS_CLASS = RunStatusBaseRun
    ENTITY_KIND = EntityKinds.RUN_GUARDRAIL_SERVE.value
