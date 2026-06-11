# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderHydra
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.hydra_build.entity import RunHydraRunBuild
from digitalhub_runtime_python.entities.run.hydra_build.spec import RunSpecHydraRunBuild, RunValidatorHydraRunBuild
from digitalhub_runtime_python.entities.run.hydra_build.status import RunStatusHydraRunBuild


class RunHydraRunBuildBuilder(RunBuilder, RuntimeEntityBuilderHydra):
    """
    RunHydraRunBuildBuilder runner.
    """

    ENTITY_CLASS = RunHydraRunBuild
    ENTITY_SPEC_CLASS = RunSpecHydraRunBuild
    ENTITY_SPEC_VALIDATOR = RunValidatorHydraRunBuild
    ENTITY_STATUS_CLASS = RunStatusHydraRunBuild
    ENTITY_KIND = EntityKinds.RUN_HYDRA_BUILD.value
