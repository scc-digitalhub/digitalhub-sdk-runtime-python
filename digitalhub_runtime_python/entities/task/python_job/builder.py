# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.plugins import Status, TaskBuilder, TaskSpecFunction

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.python_job.entity import TaskPythonJob


class TaskPythonJobBuilder(TaskBuilder, RuntimeEntityBuilderPython):
    """
    TaskPythonJobBuilder jober.
    """

    ENTITY_CLASS = TaskPythonJob
    ENTITY_SPEC_CLASS = TaskSpecFunction
    ENTITY_STATUS_CLASS = Status
    ENTITY_KIND = EntityKinds.TASK_PYTHON_JOB.value
