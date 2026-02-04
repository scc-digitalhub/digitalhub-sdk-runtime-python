# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:

    from digitalhub_runtime_python.entities.task.serve.spec import TaskSpecPythonServe
    from digitalhub_runtime_python.entities.task.serve.status import TaskStatusPythonServe


class TaskPythonServe(Task):
    """
    TaskPythonServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: TaskSpecPythonServe
        self.status: TaskStatusPythonServe
