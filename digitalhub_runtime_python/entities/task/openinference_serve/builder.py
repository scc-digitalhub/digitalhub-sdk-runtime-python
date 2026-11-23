# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status
from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task._base.spec import TaskSpecServe
from digitalhub_runtime_python.entities.task.openinference_serve.entity import TaskOpeninferenceServe


class TaskOpeninferenceServeBuilder(TaskBuilder, RuntimeEntityBuilderOpeninference):
    """
    TaskOpeninferenceServeBuilder serveer.
    """

    ENTITY_CLASS = TaskOpeninferenceServe
    ENTITY_SPEC_CLASS = TaskSpecServe
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_OPENINFERENCE_SERVE.value
