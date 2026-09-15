# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run._base.entity import RunBaseBuildRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.ray_build.spec import RunSpecRayRunBuild
    from digitalhub_runtime_python.entities.run.ray_build.status import RunStatusRayRunBuild


class RunRayRunBuild(RunBaseBuildRun):
    """
    RunRayRunBuild class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecRayRunBuild
        self.status: RunStatusRayRunBuild
