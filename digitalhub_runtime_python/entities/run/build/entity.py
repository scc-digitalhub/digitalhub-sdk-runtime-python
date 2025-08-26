# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run._base.entity import RunPythonRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_python.entities.run.build.spec import RunSpecPythonRunBuild
    from digitalhub_runtime_python.entities.run.build.status import RunStatusPythonRunBuild


class RunPythonRunBuild(RunPythonRun):
    """
    RunPythonRunBuild class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecPythonRunBuild,
        status: RunStatusPythonRunBuild,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecPythonRunBuild
        self.status: RunStatusPythonRunBuild
