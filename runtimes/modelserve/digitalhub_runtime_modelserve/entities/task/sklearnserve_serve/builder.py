from __future__ import annotations

from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.entity import TaskSklearnserveServe
from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.spec import (
    TaskSpecSklearnserveServe,
    TaskValidatorSklearnserveServe,
)
from digitalhub_runtime_modelserve.entities.task.sklearnserve_serve.status import TaskStatusSklearnserveServe

from digitalhub.entities.task._base.builder import TaskBuilder


class TaskSklearnserveServeBuilder(TaskBuilder):
    """
    TaskSklearnserveServe builder.
    """

    ENTITY_CLASS = TaskSklearnserveServe
    ENTITY_SPEC_CLASS = TaskSpecSklearnserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorSklearnserveServe
    ENTITY_STATUS_CLASS = TaskStatusSklearnserveServe