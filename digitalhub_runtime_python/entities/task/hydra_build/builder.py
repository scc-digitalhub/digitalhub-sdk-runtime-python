# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderHydra
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.hydra_build.entity import TaskHydraBuild
from digitalhub_runtime_python.entities.task.hydra_build.spec import TaskSpecHydraBuild, TaskValidatorHydraBuild
from digitalhub_runtime_python.entities.task.hydra_build.status import TaskStatusHydraBuild


class TaskHydraBuildBuilder(TaskBuilder, RuntimeEntityBuilderHydra):
    """
    TaskHydraBuild builder.
    """

    ENTITY_CLASS = TaskHydraBuild
    ENTITY_SPEC_CLASS = TaskSpecHydraBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorHydraBuild
    ENTITY_STATUS_CLASS = TaskStatusHydraBuild
    ENTITY_KIND = EntityKinds.TASK_HYDRA_BUILD.value
