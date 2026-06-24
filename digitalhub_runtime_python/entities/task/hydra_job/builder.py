# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderHydra
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.hydra_job.entity import TaskHydraJob
from digitalhub_runtime_python.entities.task.hydra_job.spec import TaskSpecHydraJob, TaskValidatorHydraJob
from digitalhub_runtime_python.entities.task.hydra_job.status import TaskStatusHydraJob


class TaskHydraJobBuilder(TaskBuilder, RuntimeEntityBuilderHydra):
    """
    TaskHydraJobBuilder jober.
    """

    ENTITY_CLASS = TaskHydraJob
    ENTITY_SPEC_CLASS = TaskSpecHydraJob
    ENTITY_SPEC_VALIDATOR = TaskValidatorHydraJob
    ENTITY_STATUS_CLASS = TaskStatusHydraJob
    ENTITY_KIND = EntityKinds.TASK_HYDRA_JOB.value
