# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderGuardrail
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.guardrail_serve.entity import TaskGuardrailServe
from digitalhub_runtime_python.entities.task.guardrail_serve.spec import (
    TaskSpecGuardrailServe,
    TaskValidatorGuardrailServe,
)
from digitalhub_runtime_python.entities.task.guardrail_serve.status import TaskStatusGuardrailServe


class TaskGuardrailServeBuilder(TaskBuilder, RuntimeEntityBuilderGuardrail):
    """
    TaskGuardrailServeBuilder serveer.
    """

    ENTITY_CLASS = TaskGuardrailServe
    ENTITY_SPEC_CLASS = TaskSpecGuardrailServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorGuardrailServe
    ENTITY_STATUS_CLASS = TaskStatusGuardrailServe
    ENTITY_KIND = EntityKinds.TASK_GUARDRAIL_SERVE.value
