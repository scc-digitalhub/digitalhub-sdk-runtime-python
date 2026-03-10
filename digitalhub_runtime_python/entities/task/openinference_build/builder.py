# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.openinference_build.entity import TaskOpeninferenceBuild
from digitalhub_runtime_python.entities.task.openinference_build.spec import (
    TaskSpecOpeninferenceBuild,
    TaskValidatorOpeninferenceBuild,
)
from digitalhub_runtime_python.entities.task.openinference_build.status import TaskStatusOpeninferenceBuild


class TaskOpeninferenceBuildBuilder(TaskBuilder, RuntimeEntityBuilderOpeninference):
    """
    TaskOpeninferenceBuild builder.
    """

    ENTITY_CLASS = TaskOpeninferenceBuild
    ENTITY_SPEC_CLASS = TaskSpecOpeninferenceBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorOpeninferenceBuild
    ENTITY_STATUS_CLASS = TaskStatusOpeninferenceBuild
    ENTITY_KIND = EntityKinds.TASK_OPENINFERENCE_BUILD.value
