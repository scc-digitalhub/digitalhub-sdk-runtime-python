# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecRayJob(TaskSpecFunction):
    """
    TaskSpecRayJob specifications.
    """
    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        replicas: int | None = None,
        min_replicas: int | None = None,
        max_replicas: int | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function=function,
            volumes=volumes,
            resources=resources,
            envs=envs,
            secrets=secrets,
            profile=profile,
            **kwargs,
        )
        self.replicas = replicas
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas

class TaskValidatorRayJob(TaskValidatorFunction):
    """
    TaskValidatorRayJob validator.
    """

    replicas: int | None = None
    """Number of replicas."""

    min_replicas: int | None = None
    """Minimum number of replicas."""

    max_replicas: int | None = None
    """Maximum number of replicas."""
