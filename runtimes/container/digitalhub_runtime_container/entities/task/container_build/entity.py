from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub_runtime_container.entities.task.container_build.spec import TaskSpecContainerBuild
    from digitalhub_runtime_container.entities.task.container_build.status import TaskStatusContainerBuild

    from digitalhub.entities._base.entity.metadata import Metadata


class TaskContainerBuild(Task):
    """
    TaskContainerBuild class.
    """

    def __init__(
        self,
        project: str,
        name: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecContainerBuild,
        status: TaskStatusContainerBuild,
        user: str | None = None,
    ) -> None:
        super().__init__(project, name, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecContainerBuild
        self.status: TaskStatusContainerBuild