# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.openinference_build.entity import RunOpeninferenceRunBuild
from digitalhub_runtime_python.entities.run.openinference_build.spec import (
    RunSpecOpeninferenceRunBuild,
    RunValidatorOpeninferenceRunBuild,
)
from digitalhub_runtime_python.entities.run.openinference_build.status import RunStatusOpeninferenceRunBuild


class RunOpeninferenceRunBuildBuilder(RunBuilder, RuntimeEntityBuilderOpeninference):
    """
    RunOpeninferenceRunBuildBuilder runner.
    """

    ENTITY_CLASS = RunOpeninferenceRunBuild
    ENTITY_SPEC_CLASS = RunSpecOpeninferenceRunBuild
    ENTITY_SPEC_VALIDATOR = RunValidatorOpeninferenceRunBuild
    ENTITY_STATUS_CLASS = RunStatusOpeninferenceRunBuild
    ENTITY_KIND = EntityKinds.RUN_OPENINFERENCE_BUILD.value
