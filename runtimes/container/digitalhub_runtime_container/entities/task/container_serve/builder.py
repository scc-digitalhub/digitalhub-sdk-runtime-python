from __future__ import annotations

from digitalhub_runtime_container.entities.task.container_serve.entity import TaskContainerServe
from digitalhub_runtime_container.entities.task.container_serve.spec import (
    TaskSpecContainerServe,
    TaskValidatorContainerServe,
)
from digitalhub_runtime_container.entities.task.container_serve.status import TaskStatusContainerServe

from digitalhub.entities.task._base.builder import TaskBuilder


class TaskContainerServeBuilder(TaskBuilder):
    """
    TaskContainerServeBuilder serveer.
    """

    ENTITY_CLASS = TaskContainerServe
    ENTITY_SPEC_CLASS = TaskSpecContainerServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorContainerServe
    ENTITY_STATUS_CLASS = TaskStatusContainerServe