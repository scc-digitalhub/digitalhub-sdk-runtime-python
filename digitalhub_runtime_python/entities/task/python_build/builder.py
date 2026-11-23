# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.entity.status import Status
from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task._base.spec import TaskSpecBuild
from digitalhub_runtime_python.entities.task.python_build.entity import TaskPythonBuild


class TaskPythonBuildBuilder(TaskBuilder, RuntimeEntityBuilderPython):
    """
    TaskPythonBuild builder.
    """

    ENTITY_CLASS = TaskPythonBuild
    ENTITY_SPEC_CLASS = TaskSpecBuild
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_PYTHON_BUILD.value
