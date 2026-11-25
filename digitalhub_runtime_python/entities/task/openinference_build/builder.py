# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import Status, TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderOpeninference
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task._base.spec import TaskSpecBuild
from digitalhub_runtime_python.entities.task.openinference_build.entity import TaskOpeninferenceBuild


class TaskOpeninferenceBuildBuilder(TaskBuilder, RuntimeEntityBuilderOpeninference):
    """
    TaskOpeninferenceBuild builder.
    """

    ENTITY_CLASS = TaskOpeninferenceBuild
    ENTITY_SPEC_CLASS = TaskSpecBuild
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_OPENINFERENCE_BUILD.value
