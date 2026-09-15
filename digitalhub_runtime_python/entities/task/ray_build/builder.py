# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderRay
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.ray_build.entity import TaskRayBuild
from digitalhub_runtime_python.entities.task.ray_build.spec import TaskSpecRayBuild, TaskValidatorRayBuild
from digitalhub_runtime_python.entities.task.ray_build.status import TaskStatusRayBuild


class TaskRayBuildBuilder(TaskBuilder, RuntimeEntityBuilderRay):
    """
    TaskRayBuild builder.
    """

    ENTITY_CLASS = TaskRayBuild
    ENTITY_SPEC_CLASS = TaskSpecRayBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorRayBuild
    ENTITY_STATUS_CLASS = TaskStatusRayBuild
    ENTITY_KIND = EntityKinds.TASK_RAY_BUILD.value
