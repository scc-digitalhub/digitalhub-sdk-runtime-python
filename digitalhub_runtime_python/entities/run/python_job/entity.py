# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.run._base.entity import LocalExecutionRunMixin

from digitalhub_runtime_python.entities.run._base.entity import RunBaseRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run._base.status import RunStatusBaseRun
    from digitalhub_runtime_python.entities.run.python_job.spec import RunSpecPythonRunJob


class RunPythonRunJob(LocalExecutionRunMixin, RunBaseRun):
    """
    RunPythonRunJob class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecPythonRunJob
        self.status: RunStatusBaseRun

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
