# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import ServeRunMixin

from digitalhub_runtime_python.entities.run._base.entity import RunBaseRun

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run._base.status import RunStatusBaseRun
    from digitalhub_runtime_python.entities.run.python_serve.spec import RunSpecPythonRunServe


class RunPythonRunServe(ServeRunMixin, RunBaseRun):
    """
    RunPythonRunServe class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecPythonRunServe
        self.status: RunStatusBaseRun
