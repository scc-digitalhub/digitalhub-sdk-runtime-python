# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.plugins import EntityIORunMixin, ResultsRunMixin, Run

if typing.TYPE_CHECKING:
    from digitalhub_runtime_python.entities.run._base.spec import RunSpecBaseRun
    from digitalhub_runtime_python.entities.run._base.status import RunStatusBaseRun


class RunBaseRun(EntityIORunMixin, ResultsRunMixin, Run):
    """
    RunPythonRun class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.spec: RunSpecBaseRun
        self.status: RunStatusBaseRun


class RunBaseBuildRun(RunBaseRun):
    """
    RunBaseBuildRun class.
    """

    @property
    def image(self) -> str | None:
        """
        Get run's image.

        Returns
        -------
        str | None
            The image.
        """
        return self.status.outputs.get("image")
