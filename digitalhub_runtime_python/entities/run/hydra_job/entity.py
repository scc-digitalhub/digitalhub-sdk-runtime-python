# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run._base.entity import RunBaseRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.hydra_job.spec import RunSpecHydraRunJob
    from digitalhub_runtime_python.entities.run.hydra_job.status import RunStatusHydraRunJob


class RunHydraRunJob(RunBaseRun):
    """
    RunHydraRunJob class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecHydraRunJob
        self.status: RunStatusHydraRunJob

    def local_execution(self) -> bool:
        """
        Check if run has local execution.

        Returns
        -------
        bool
            True if run has local execution, False otherwise.
        """
        return self.spec.local_execution

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
