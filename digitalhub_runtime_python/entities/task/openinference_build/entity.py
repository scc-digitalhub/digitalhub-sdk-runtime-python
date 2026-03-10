# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.task.openinference_build.spec import TaskSpecOpeninferenceBuild
    from digitalhub_runtime_python.entities.task.openinference_build.status import TaskStatusOpeninferenceBuild


class TaskOpeninferenceBuild(Task):
    """
    TaskOpeninferenceBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: TaskSpecOpeninferenceBuild
        self.status: TaskStatusOpeninferenceBuild
