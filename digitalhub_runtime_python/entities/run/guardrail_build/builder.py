# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderGuardrail
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.guardrail_build.entity import RunGuardrailRunBuild
from digitalhub_runtime_python.entities.run.guardrail_build.spec import (
    RunSpecGuardrailRunBuild,
    RunValidatorGuardrailRunBuild,
)
from digitalhub_runtime_python.entities.run.guardrail_build.status import RunStatusGuardrailRunBuild


class RunGuardrailRunBuildBuilder(RunBuilder, RuntimeEntityBuilderGuardrail):
    """
    RunGuardrailRunBuildBuilder runner.
    """

    ENTITY_CLASS = RunGuardrailRunBuild
    ENTITY_SPEC_CLASS = RunSpecGuardrailRunBuild
    ENTITY_SPEC_VALIDATOR = RunValidatorGuardrailRunBuild
    ENTITY_STATUS_CLASS = RunStatusGuardrailRunBuild
    ENTITY_KIND = EntityKinds.RUN_GUARDRAIL_BUILD.value
