# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderRay
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.ray_job.entity import TaskRayJob
from digitalhub_runtime_python.entities.task.ray_job.spec import TaskSpecRayJob, TaskValidatorRayJob
from digitalhub_runtime_python.entities.task.ray_job.status import TaskStatusRayJob


class TaskRayJobBuilder(TaskBuilder, RuntimeEntityBuilderRay):
    """
    TaskRayJobBuilder jober.
    """

    ENTITY_CLASS = TaskRayJob
    ENTITY_SPEC_CLASS = TaskSpecRayJob
    ENTITY_SPEC_VALIDATOR = TaskValidatorRayJob
    ENTITY_STATUS_CLASS = TaskStatusRayJob
    ENTITY_KIND = EntityKinds.TASK_RAY_JOB.value
