# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderHydra
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.hydra_subtask.entity import TaskHydraSubtask
from digitalhub_runtime_python.entities.task.hydra_subtask.spec import TaskSpecHydraSubtask, TaskValidatorHydraSubtask
from digitalhub_runtime_python.entities.task.hydra_subtask.status import TaskStatusHydraSubtask


class TaskHydraSubtaskBuilder(TaskBuilder, RuntimeEntityBuilderHydra):
    """
    TaskHydraSubtaskBuilder jober.
    """

    ENTITY_CLASS = TaskHydraSubtask
    ENTITY_SPEC_CLASS = TaskSpecHydraSubtask
    ENTITY_SPEC_VALIDATOR = TaskValidatorHydraSubtask
    ENTITY_STATUS_CLASS = TaskStatusHydraSubtask
    ENTITY_KIND = EntityKinds.TASK_HYDRA_SUBTASK.value
