# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderHydra
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.run.hydra_job.entity import RunHydraRunJob
from digitalhub_runtime_python.entities.run.hydra_job.spec import RunSpecHydraRunJob, RunValidatorHydraRunJob
from digitalhub_runtime_python.entities.run.hydra_job.status import RunStatusHydraRunJob


class RunHydraRunJobBuilder(RunBuilder, RuntimeEntityBuilderHydra):
    """
    RunHydraRunJobBuilder runner.
    """

    ENTITY_CLASS = RunHydraRunJob
    ENTITY_SPEC_CLASS = RunSpecHydraRunJob
    ENTITY_SPEC_VALIDATOR = RunValidatorHydraRunJob
    ENTITY_STATUS_CLASS = RunStatusHydraRunJob
    ENTITY_KIND = EntityKinds.RUN_HYDRA_JOB.value
