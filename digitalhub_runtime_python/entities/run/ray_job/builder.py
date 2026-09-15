# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.ray_job.entity import RunRayRunJob
from digitalhub_runtime_python.entities.run.ray_job.spec import RunSpecRayRunJob, RunValidatorRayRunJob
from digitalhub_runtime_python.entities.run.ray_job.status import RunStatusRayRunJob


class RunRayRunJobBuilder(RunBuilder, RuntimeEntityBuilderPython):
    """
    RunRayRunJobBuilder runner.
    """

    ENTITY_CLASS = RunRayRunJob
    ENTITY_SPEC_CLASS = RunSpecRayRunJob
    ENTITY_SPEC_VALIDATOR = RunValidatorRayRunJob
    ENTITY_STATUS_CLASS = RunStatusRayRunJob
    ENTITY_KIND = EntityKinds.RUN_RAY_JOB.value
