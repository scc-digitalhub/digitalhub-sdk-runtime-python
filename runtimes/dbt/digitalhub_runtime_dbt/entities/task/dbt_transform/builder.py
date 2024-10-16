from __future__ import annotations

from digitalhub_runtime_dbt.entities.task.dbt_transform.entity import TaskDbtTransform
from digitalhub_runtime_dbt.entities.task.dbt_transform.spec import TaskSpecDbtTransform, TaskValidatorDbtTransform
from digitalhub_runtime_dbt.entities.task.dbt_transform.status import TaskStatusDbtTransform

from digitalhub.entities.task._base.builder import TaskBuilder


class TaskDbtTransformBuilder(TaskBuilder):
    """
    TaskDbtTransformBuilder transformer.
    """

    ENTITY_CLASS = TaskDbtTransform
    ENTITY_SPEC_CLASS = TaskSpecDbtTransform
    ENTITY_SPEC_VALIDATOR = TaskValidatorDbtTransform
    ENTITY_STATUS_CLASS = TaskStatusDbtTransform