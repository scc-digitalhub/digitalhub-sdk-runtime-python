# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderRay
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.ray_build.entity import RunRayRunBuild
from digitalhub_runtime_python.entities.run.ray_build.spec import RunSpecRayRunBuild, RunValidatorRayRunBuild
from digitalhub_runtime_python.entities.run.ray_build.status import RunStatusRayRunBuild


class RunRayRunBuildBuilder(RunBuilder, RuntimeEntityBuilderRay):
    """
    RunRayRunBuildBuilder runner.
    """

    ENTITY_CLASS = RunRayRunBuild
    ENTITY_SPEC_CLASS = RunSpecRayRunBuild
    ENTITY_SPEC_VALIDATOR = RunValidatorRayRunBuild
    ENTITY_STATUS_CLASS = RunStatusRayRunBuild
    ENTITY_KIND = EntityKinds.RUN_RAY_BUILD.value
