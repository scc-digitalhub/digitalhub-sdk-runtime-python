# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.openinference_serve.entity import TaskOpeninferenceServe
from digitalhub_runtime_python.entities.task.openinference_serve.spec import (
    TaskSpecOpeninferenceServe,
    TaskValidatorOpeninferenceServe,
)
from digitalhub_runtime_python.entities.task.openinference_serve.status import TaskStatusOpeninferenceServe


class TaskOpeninferenceServeBuilder(TaskBuilder, RuntimeEntityBuilderOpeninference):
    """
    TaskOpeninferenceServeBuilder serveer.
    """

    ENTITY_CLASS = TaskOpeninferenceServe
    ENTITY_SPEC_CLASS = TaskSpecOpeninferenceServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorOpeninferenceServe
    ENTITY_STATUS_CLASS = TaskStatusOpeninferenceServe
    ENTITY_KIND = EntityKinds.TASK_OPENINFERENCE_SERVE.value
