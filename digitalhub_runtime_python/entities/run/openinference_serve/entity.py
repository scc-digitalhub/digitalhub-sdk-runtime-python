# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub_runtime_python.entities.run._base.entity import RunPythonRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run.openinference_serve.spec import RunSpecOpeninferenceRunServe
    from digitalhub_runtime_python.entities.run.openinference_serve.status import RunStatusOpeninferenceRunServe


class RunOpeninferenceRunServe(RunPythonRun):
    """
    RunOpeninferenceRunServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecOpeninferenceRunServe
        self.status: RunStatusOpeninferenceRunServe
