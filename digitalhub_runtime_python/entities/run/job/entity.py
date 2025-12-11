# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run._base.entity import RunPythonRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_python.entities.run.job.spec import RunSpecPythonRunJob
    from digitalhub_runtime_python.entities.run.job.status import RunStatusPythonRunJob


class RunPythonRunJob(RunPythonRun):
    """
    RunPythonRunJob class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecPythonRunJob,
        status: RunStatusPythonRunJob,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecPythonRunJob
        self.status: RunStatusPythonRunJob

    def add_output(self, name: str, value: str) -> None:
        """
        Add an output to the run job.

        Parameters
        ----------
        name : str
            The name of the output.
        value : str
            The value of the output.
        """
        if self.status.outputs is None:
            self.status.outputs = {}
        self.status.outputs[name] = value

    def set_status(self, status: dict) -> None:
        """
        Patch to merge outputs when updating status.

        Parameters
        ----------
        status : dict
            The status dictionary to update.
        """
        if self.status.outputs is None:
            self.status.outputs = {}
        if "outputs" in status:
            status["outputs"] = {
                **self.status.outputs,
                **status["outputs"],
            }
        return super().set_status(status)
